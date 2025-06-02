"""
Kafka Connector for sending messages to Kafka topics.
This connector can work with Kafka clusters located on a different subnet.
"""
import json
import logging
from typing import Dict, Any, Optional, List

from confluent_kafka import Producer, KafkaException, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic

from backend.src.config.config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
    KAFKA_SECURITY_PROTOCOL,
    KAFKA_SASL_MECHANISM,
    KAFKA_SASL_USERNAME,
    KAFKA_SASL_PASSWORD,
    KAFKA_SUBNET_ID
)

logger = logging.getLogger(__name__)

class KafkaConnector:
    """
    Connector class for Kafka.
    
    This class handles connection to Kafka and provides methods
    to send messages to Kafka topics.
    """
    
    def __init__(self, bootstrap_servers: Optional[str] = None, topic: Optional[str] = None):
        """
        Initialize the Kafka connector.
        
        Args:
            bootstrap_servers: Kafka bootstrap servers. Defaults to value from config.
            topic: Default Kafka topic. Defaults to value from config.
        """
        self.bootstrap_servers = bootstrap_servers or KAFKA_BOOTSTRAP_SERVERS
        self.topic = topic or KAFKA_TOPIC
        self.producer = None
        self.admin_client = None
        
        # Configure Kafka connection
        self.config = {
            'bootstrap.servers': self.bootstrap_servers,
            'client.id': 'sqs-kafka-connector',
            'message.max.bytes': 1000000,  # 1MB max message size
            'compression.type': 'snappy',  # Enable compression
            'retries': 5,  # Retry on failure
            'retry.backoff.ms': 500,  # Backoff time between retries
        }
        
        # Add security configuration if provided
        if KAFKA_SECURITY_PROTOCOL:
            self.config['security.protocol'] = KAFKA_SECURITY_PROTOCOL
            
        if KAFKA_SASL_MECHANISM and KAFKA_SASL_USERNAME and KAFKA_SASL_PASSWORD:
            self.config['sasl.mechanisms'] = KAFKA_SASL_MECHANISM
            self.config['sasl.username'] = KAFKA_SASL_USERNAME
            self.config['sasl.password'] = KAFKA_SASL_PASSWORD
            
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
            
            # Ensure the topic exists
            self.ensure_topic_exists(self.topic)
            
        except KafkaException as e:
            logger.error(f"Error connecting to Kafka: {e}")
            raise
            
    def ensure_topic_exists(self, topic: str, num_partitions: int = 3, replication_factor: int = 3):
        """
        Ensure that the topic exists, create it if it doesn't.
        
        Args:
            topic: Topic name
            num_partitions: Number of partitions for the topic
            replication_factor: Replication factor for the topic
        """
        try:
            # Get existing topics
            metadata = self.admin_client.list_topics(timeout=10)
            
            # Check if the topic exists
            if topic not in metadata.topics:
                logger.info(f"Topic {topic} does not exist, creating it")
                topic_list = [NewTopic(
                    topic, 
                    num_partitions=num_partitions, 
                    replication_factor=replication_factor
                )]
                
                # Create the topic
                self.admin_client.create_topics(topic_list)
                logger.info(f"Topic {topic} created successfully")
            else:
                logger.info(f"Topic {topic} already exists")
                
        except KafkaException as e:
            logger.warning(f"Error checking/creating topic: {e}")
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
            
    def send_message(self, message: Dict[str, Any], topic: Optional[str] = None, key: Optional[str] = None) -> bool:
        """
        Send a message to a Kafka topic.
        
        Args:
            message: Message as a dictionary, will be converted to JSON
            topic: Topic to send the message to. Defaults to the default topic.
            key: Optional message key for partitioning
            
        Returns:
            True if the message was sent, False otherwise
        """
        try:
            target_topic = topic or self.topic
            message_json = json.dumps(message).encode('utf-8')
            
            # If key is provided, encode it
            key_bytes = key.encode('utf-8') if key else None
            
            # Send the message
            self.producer.produce(
                topic=target_topic,
                key=key_bytes,
                value=message_json,
                callback=self._delivery_report
            )
            
            # Trigger any available delivery callbacks
            self.producer.poll(0)
            
            return True
            
        except KafkaException as e:
            logger.error(f"Error sending message to Kafka: {e}")
            return False
            
    def flush(self, timeout: int = 10):
        """
        Wait for all messages in the producer queue to be delivered.
        
        Args:
            timeout: Maximum time to wait in seconds
        """
        self.producer.flush(timeout)
    
    def create_topics(self, topics: List[str], num_partitions: int = 3, replication_factor: int = 3):
        """
        Create multiple Kafka topics.
        
        Args:
            topics: List of topic names to create
            num_partitions: Number of partitions for each topic
            replication_factor: Replication factor for each topic
        """
        try:
            topic_list = [
                NewTopic(
                    topic, 
                    num_partitions=num_partitions, 
                    replication_factor=replication_factor
                ) 
                for topic in topics
            ]
            
            self.admin_client.create_topics(topic_list)
            logger.info(f"Created topics: {', '.join(topics)}")
            
        except KafkaException as e:
            logger.error(f"Error creating topics: {e}")
            raise
