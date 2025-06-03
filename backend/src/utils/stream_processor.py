"""
Stream processor module that handles the processing of messages from SQS to Kafka.
"""
import logging
import time
import threading
import json
from datetime import datetime
from typing import Dict, Any, Optional, List

from src.connectors.sqs_connector import SQSConnector
from src.connectors.kafka_connector import KafkaConnector
from src.config.config import KAFKA_TOPIC

logger = logging.getLogger(__name__)

class StreamProcessor:
    """
    Stream processor that connects AWS SQS to Kafka.
    
    This class handles the streaming process between SQS and Kafka,
    including message transformation and error handling.
    """
    
    def __init__(self, sqs_connector: SQSConnector, kafka_connector: KafkaConnector):
        """
        Initialize the stream processor.
        
        Args:
            sqs_connector: SQS connector instance
            kafka_connector: Kafka connector instance
        """
        self.sqs_connector = sqs_connector
        self.kafka_connector = kafka_connector
        self.running = False
        self.thread = None
        self.stop_event = threading.Event()
        
    def process_message(self, message: Dict[str, Any]) -> bool:
        """
        Process a single message from SQS and send it to Kafka.
        
        Args:
            message: Message from SQS
            
        Returns:
            True if processing was successful, False otherwise
        """
        try:
            message_id = message['message_id']
            body = message['body']
            
            # Add metadata to the message
            enriched_message = {
                'message_id': message_id,
                'source': 'aws-sqs',
                'timestamp': datetime.now().isoformat(),
                'data': body
            }
            
            # Add any additional processing logic here
            
            # Send the message to Kafka
            success = self.kafka_connector.send_message(
                enriched_message, 
                key=message_id
            )
            
            if success:
                logger.debug(f"Successfully processed message {message_id}")
                return True
            else:
                logger.error(f"Failed to send message {message_id} to Kafka")
                return False
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return False
    
    def streaming_worker(self, metrics: Optional[Dict[str, Any]] = None):
        """
        Worker function that continuously processes messages from SQS to Kafka.
        
        Args:
            metrics: Optional dictionary to update with metrics
        """
        logger.info("Streaming worker started")
        
        while not self.stop_event.is_set():
            try:
                # Receive messages from SQS
                start_time = time.time()
                messages = self.sqs_connector.receive_messages(max_messages=10)
                
                # Process each message
                for message in messages:
                    try:
                        success = self.process_message(message)
                        
                        if success:
                            # Delete the message from SQS if processing was successful
                            self.sqs_connector.delete_message(message['receipt_handle'])
                            
                            # Update metrics
                            if metrics is not None:
                                metrics['messages_processed'] += 1
                                metrics['last_processing_time'] = datetime.now().isoformat()
                        else:
                            # Update error metrics
                            if metrics is not None:
                                metrics['kafka_send_errors'] += 1
                    except Exception as e:
                        logger.error(f"Error in message processing loop: {e}")
                        if metrics is not None:
                            metrics['processing_errors'] += 1
                
                # Ensure all messages are sent to Kafka
                self.kafka_connector.flush()
                
                # If no messages were received, wait before polling again
                if not messages:
                    time.sleep(5)
                    
            except Exception as e:
                logger.error(f"Error in streaming worker: {e}")
                if metrics is not None:
                    metrics['processing_errors'] += 1
                time.sleep(5)  # Wait before retrying
    
    def start_streaming(self, metrics: Optional[Dict[str, Any]] = None):
        """
        Start the streaming process.
        
        Args:
            metrics: Optional dictionary to update with metrics
        """
        if self.running:
            logger.warning("Streaming is already running")
            return
        
        self.stop_event.clear()
        self.running = True
        
        # Start the streaming worker in a separate thread
        self.thread = threading.Thread(
            target=self.streaming_worker,
            args=(metrics,),
            daemon=True
        )
        self.thread.start()
        logger.info("Streaming process started")
    
    def stop_streaming(self):
        """
        Stop the streaming process.
        """
        if not self.running:
            logger.warning("Streaming is not running")
            return
        
        logger.info("Stopping streaming process")
        self.stop_event.set()
        
        # Wait for the thread to finish
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=10)
        
        self.running = False
        logger.info("Streaming process stopped")
    
    def get_available_topics(self) -> List[str]:
        """
        Get a list of available Kafka topics.
        
        Returns:
            List of topic names
        """
        try:
            # Use the admin client to list topics
            metadata = self.kafka_connector.admin_client.list_topics(timeout=10)
            topics = list(metadata.topics.keys())
            return topics
        except Exception as e:
            logger.error(f"Error getting topics: {e}")
            return [KAFKA_TOPIC]  # Return default topic if listing fails
    
    @staticmethod
    def transform_message(message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform a message for Kafka.
        
        Args:
            message: Original message
            
        Returns:
            Transformed message
        """
        # Add any transformation logic here
        transformed = {
            'id': message.get('message_id', ''),
            'timestamp': datetime.now().isoformat(),
            'payload': message.get('body', {}),
            'metadata': {
                'source': 'aws-sqs',
                'attributes': message.get('attributes', {}),
                'message_attributes': message.get('message_attributes', {})
            }
        }
        
        return transformed
