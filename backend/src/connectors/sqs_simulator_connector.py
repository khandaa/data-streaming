"""
SQS Simulator Connector using Kafka as a backend.
This connector simulates AWS SQS functionality using Kafka topics.
"""
import json
import time
import logging
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime

from confluent_kafka import Consumer, Producer, KafkaError, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic

from backend.src.config.config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_SECURITY_PROTOCOL,
    KAFKA_SASL_MECHANISM,
    KAFKA_SASL_USERNAME,
    KAFKA_SASL_PASSWORD
)

logger = logging.getLogger(__name__)

class SQSSimulatorConnector:
    """
    Simulator connector class for AWS SQS using Kafka.
    
    This class simulates AWS SQS functionality using Kafka topics,
    providing the same interface as the SQSConnector class.
    """
    
    def __init__(self, queue_name: str = "sqs-queue-1", bootstrap_servers: Optional[str] = None):
        """
        Initialize the SQS simulator connector.
        
        Args:
            queue_name: Name of the simulated SQS queue (Kafka topic)
            bootstrap_servers: Kafka bootstrap servers. Defaults to value from config.
        """
        self.queue_name = queue_name
        self.bootstrap_servers = bootstrap_servers or KAFKA_BOOTSTRAP_SERVERS
        self.consumer_group = f"sqs-simulator-{uuid.uuid4().hex[:8]}"
        
        # Configure Kafka connection
        self.config = {
            'bootstrap.servers': self.bootstrap_servers,
            'client.id': 'sqs-simulator',
            'message.max.bytes': 1000000,  # 1MB max message size
        }
        
        # Add security configuration if provided
        if KAFKA_SECURITY_PROTOCOL:
            self.config['security.protocol'] = KAFKA_SECURITY_PROTOCOL
            
        if KAFKA_SASL_MECHANISM and KAFKA_SASL_USERNAME and KAFKA_SASL_PASSWORD:
            self.config['sasl.mechanisms'] = KAFKA_SASL_MECHANISM
            self.config['sasl.username'] = KAFKA_SASL_USERNAME
            self.config['sasl.password'] = KAFKA_SASL_PASSWORD
            
        # Consumer config
        self.consumer_config = self.config.copy()
        self.consumer_config.update({
            'group.id': self.consumer_group,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
            'session.timeout.ms': 10000,
        })
        
        # Connect to Kafka
        self._connect()
        
    def _connect(self):
        """
        Establish connection to Kafka.
        """
        try:
            logger.info(f"Connecting to Kafka at {self.bootstrap_servers}")
            self.producer = Producer(self.config)
            self.admin_client = AdminClient(self.config)
            logger.info("Connected to Kafka successfully")
            
            # Ensure the queue topic exists
            self.ensure_queue_exists(self.queue_name)
            
        except KafkaException as e:
            logger.error(f"Error connecting to Kafka: {e}")
            raise
            
    def ensure_queue_exists(self, queue_name: str):
        """
        Ensure that the SQS queue (Kafka topic) exists, create it if it doesn't.
        
        Args:
            queue_name: Queue name (Kafka topic)
        """
        try:
            # Get existing topics
            metadata = self.admin_client.list_topics(timeout=10)
            
            # Check if the topic exists
            if queue_name not in metadata.topics:
                logger.info(f"Queue (topic) {queue_name} does not exist, creating it")
                topic_list = [NewTopic(
                    queue_name, 
                    num_partitions=1,  # SQS-like behavior with single partition 
                    replication_factor=1
                )]
                
                # Create the topic
                self.admin_client.create_topics(topic_list)
                logger.info(f"Queue (topic) {queue_name} created successfully")
            else:
                logger.info(f"Queue (topic) {queue_name} already exists")
                
        except KafkaException as e:
            logger.warning(f"Error checking/creating queue (topic): {e}")
            # Continue anyway, the topic might be auto-created when sending messages

    def _delivery_report(self, err, msg):
        """
        Callback for message delivery reports.
        
        Args:
            err: Error (if any)
            msg: Message that was delivered
        """
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            topic = msg.topic()
            partition = msg.partition()
            offset = msg.offset()
            logger.debug(f"Message delivered to {topic}[{partition}] at offset {offset}")

    def receive_messages(self, max_messages: int = 10, wait_time: int = 20) -> List[Dict[str, Any]]:
        """
        Receive messages from the simulated SQS queue (Kafka topic).
        
        Args:
            max_messages: Maximum number of messages to receive (1-10)
            wait_time: Long polling wait time in seconds (0-20)
            
        Returns:
            List of messages, each as a dictionary
        """
        try:
            # Create a consumer instance for this poll
            consumer = Consumer(self.consumer_config)
            consumer.subscribe([self.queue_name])
            
            messages = []
            start_time = time.time()
            end_time = start_time + wait_time
            
            while len(messages) < max_messages and time.time() < end_time:
                # Poll for messages
                msg = consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.debug("Reached end of partition")
                    else:
                        logger.error(f"Error polling for messages: {msg.error()}")
                    continue
                
                try:
                    # Parse the message value
                    value_str = msg.value().decode('utf-8')
                    value_dict = json.loads(value_str)
                    
                    # Generate a unique receipt handle (needed for SQS interface)
                    receipt_handle = f"{msg.topic()}-{msg.partition()}-{msg.offset()}-{uuid.uuid4().hex}"
                    
                    # Add SQS-like metadata
                    message = {
                        'message_id': value_dict.get('message_id', str(uuid.uuid4())),
                        'receipt_handle': receipt_handle,
                        'body': value_dict.get('body', value_dict),
                        'attributes': {
                            'SentTimestamp': str(int(time.time() * 1000)),
                            'ApproximateReceiveCount': '1',
                            'ApproximateFirstReceiveTimestamp': str(int(time.time() * 1000))
                        },
                        'message_attributes': {},
                        '_kafka_offset': msg.offset(),
                        '_kafka_partition': msg.partition()
                    }
                    
                    messages.append(message)
                    
                    # Store the offset for later commit
                    consumer.store_offsets(message=msg)
                    
                except Exception as e:
                    logger.error(f"Error processing received message: {e}")
            
            # Close the consumer
            consumer.close()
            
            logger.info(f"Received {len(messages)} messages from SQS simulator")
            return messages
            
        except Exception as e:
            logger.error(f"Error receiving messages: {e}")
            return []

    def delete_message(self, receipt_handle: str) -> bool:
        """
        Delete a message from the simulated queue after processing.
        
        In Kafka, this is simulated by committing the offset for the consumer group.
        
        Args:
            receipt_handle: The receipt handle of the message to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Parse the receipt handle to get topic, partition, offset
            parts = receipt_handle.split('-')
            if len(parts) >= 3:
                topic = parts[0]
                partition = int(parts[1])
                offset = int(parts[2])
                
                # In Kafka, "deleting" a message is done by committing the offset
                # We've already stored the offset when receiving, so no additional action is needed
                logger.debug(f"Simulated deletion of message with receipt handle {receipt_handle[:10]}...")
                return True
            else:
                logger.error(f"Invalid receipt handle format: {receipt_handle}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting message: {e}")
            return False
    
    def send_message(self, message_body: Dict[str, Any]) -> Optional[str]:
        """
        Send a message to the simulated SQS queue.
        
        Args:
            message_body: Message body as a dictionary, will be converted to JSON
            
        Returns:
            Message ID if successful, None otherwise
        """
        try:
            # Generate a unique message ID
            message_id = str(uuid.uuid4())
            
            # Prepare the message with SQS-like metadata
            message = {
                'message_id': message_id,
                'body': message_body,
                'timestamp': datetime.now().isoformat()
            }
            
            # Convert to JSON and encode
            message_json = json.dumps(message).encode('utf-8')
            
            # Send the message
            self.producer.produce(
                topic=self.queue_name,
                value=message_json,
                callback=self._delivery_report
            )
            
            # Trigger any available delivery callbacks
            self.producer.poll(0)
            
            logger.info(f"Sent message to SQS simulator with ID {message_id}")
            return message_id
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return None
    
    def stream_messages(self, handler_func, poll_interval: int = 5, max_messages: int = 10):
        """
        Stream messages continuously from the queue and process them with a handler function.
        
        Args:
            handler_func: Function that will process each message
            poll_interval: Time to wait between polling attempts in seconds
            max_messages: Maximum number of messages to retrieve per poll
        """
        logger.info(f"Starting SQS simulator message streaming from {self.queue_name}")
        
        while True:
            try:
                messages = self.receive_messages(max_messages=max_messages)
                
                for message in messages:
                    # Process the message with the handler function
                    result = handler_func(message)
                    
                    # If processing was successful, delete the message from the queue
                    if result:
                        self.delete_message(message['receipt_handle'])
                
                # If no messages were received, wait before polling again
                if not messages:
                    time.sleep(poll_interval)
                    
            except Exception as e:
                logger.error(f"Error in message streaming loop: {e}")
                time.sleep(poll_interval)  # Wait before retrying
    
    def get_queue_url(self) -> str:
        """
        Get the URL of the simulated SQS queue.
        
        Returns:
            A string representing the queue URL (in this case, the Kafka topic name)
        """
        return f"kafka://{self.bootstrap_servers}/{self.queue_name}"
