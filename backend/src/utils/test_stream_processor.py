"""
Test stream processor module that uses Kafka SQS Simulator.
"""
import logging
import time
import threading
import json
from datetime import datetime
from typing import Dict, Any, Optional, List

from backend.src.connectors.sqs_simulator_connector import SQSSimulatorConnector
from backend.src.connectors.kafka_connector import KafkaConnector
from backend.src.config.test_config import (
    KAFKA_TOPIC, 
    SQS_SIMULATOR_QUEUE
)

logger = logging.getLogger(__name__)

class TestStreamProcessor:
    """
    Test stream processor that connects simulated SQS (Kafka) to Kafka.
    
    This class handles the streaming process between simulated SQS and Kafka,
    including message transformation and error handling.
    """
    
    def __init__(self, sqs_connector: SQSSimulatorConnector, kafka_connector: KafkaConnector):
        """
        Initialize the test stream processor.
        
        Args:
            sqs_connector: SQS simulator connector instance
            kafka_connector: Kafka connector instance
        """
        self.sqs_connector = sqs_connector
        self.kafka_connector = kafka_connector
        self.running = False
        self.thread = None
        self.stop_event = threading.Event()
        self.metrics = {
            'messages_processed': 0,
            'processing_errors': 0,
            'kafka_send_errors': 0,
            'last_processing_time': None,
            'start_time': None,
            'end_time': None,
            'total_execution_time': 0,
            'messages_per_second': 0
        }
        
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
                'source': 'sqs-simulator',
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
    
    def streaming_worker(self):
        """
        Worker function that continuously processes messages from SQS to Kafka.
        """
        logger.info("Test streaming worker started")
        self.metrics['start_time'] = datetime.now().isoformat()
        
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
                            self.metrics['messages_processed'] += 1
                            self.metrics['last_processing_time'] = datetime.now().isoformat()
                        else:
                            # Update error metrics
                            self.metrics['kafka_send_errors'] += 1
                    except Exception as e:
                        logger.error(f"Error in message processing loop: {e}")
                        self.metrics['processing_errors'] += 1
                
                # Ensure all messages are sent to Kafka
                self.kafka_connector.flush()
                
                # Update performance metrics
                if self.metrics['messages_processed'] > 0:
                    current_time = datetime.now()
                    if self.metrics['start_time']:
                        start_time = datetime.fromisoformat(self.metrics['start_time'])
                        time_diff = (current_time - start_time).total_seconds()
                        if time_diff > 0:
                            self.metrics['total_execution_time'] = time_diff
                            self.metrics['messages_per_second'] = self.metrics['messages_processed'] / time_diff
                
                # If no messages were received, wait before polling again
                if not messages:
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Error in streaming worker: {e}")
                self.metrics['processing_errors'] += 1
                time.sleep(1)  # Wait before retrying
    
    def start_streaming(self):
        """
        Start the streaming process.
        """
        if self.running:
            logger.warning("Streaming is already running")
            return
        
        # Reset metrics
        self.metrics = {
            'messages_processed': 0,
            'processing_errors': 0,
            'kafka_send_errors': 0,
            'last_processing_time': None,
            'start_time': None,
            'end_time': None,
            'total_execution_time': 0,
            'messages_per_second': 0
        }
        
        self.stop_event.clear()
        self.running = True
        
        # Start the streaming worker in a separate thread
        self.thread = threading.Thread(
            target=self.streaming_worker,
            daemon=True
        )
        self.thread.start()
        logger.info("Test streaming process started")
    
    def stop_streaming(self):
        """
        Stop the streaming process.
        """
        if not self.running:
            logger.warning("Streaming is not running")
            return
        
        logger.info("Stopping test streaming process")
        self.stop_event.set()
        
        # Wait for the thread to finish
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=10)
        
        self.running = False
        self.metrics['end_time'] = datetime.now().isoformat()
        
        # Calculate final metrics
        if self.metrics['start_time'] and self.metrics['end_time']:
            start_time = datetime.fromisoformat(self.metrics['start_time'])
            end_time = datetime.fromisoformat(self.metrics['end_time'])
            time_diff = (end_time - start_time).total_seconds()
            self.metrics['total_execution_time'] = time_diff
            if self.metrics['messages_processed'] > 0 and time_diff > 0:
                self.metrics['messages_per_second'] = self.metrics['messages_processed'] / time_diff
        
        logger.info("Test streaming process stopped")
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current streaming metrics.
        
        Returns:
            Dictionary with metrics
        """
        return self.metrics
    
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
