"""
Test script for the Stream Processor.
Tests the complete streaming process from SQS simulator to Kafka.
"""
import json
import logging
import time
import sys
import os
import threading
from typing import List, Dict, Any

# Add project root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.src.connectors.sqs_simulator_connector import SQSSimulatorConnector
from backend.src.connectors.kafka_connector import KafkaConnector
from backend.src.utils.test_stream_processor import TestStreamProcessor
# Update import path to use test-data folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'test-data'))
from data_generator import TestDataGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StreamProcessorTest:
    """
    Test class for the Stream Processor.
    """
    
    def __init__(
        self, 
        bootstrap_servers: str = "localhost:29092", 
        sqs_queue: str = "sqs-queue-1",
        kafka_topic: str = "streaming-topic"
    ):
        """
        Initialize the test class.
        
        Args:
            bootstrap_servers: Kafka bootstrap servers
            sqs_queue: Name of the SQS simulator queue (Kafka topic)
            kafka_topic: Name of the destination Kafka topic
        """
        self.bootstrap_servers = bootstrap_servers
        self.sqs_queue = sqs_queue
        self.kafka_topic = kafka_topic
        
        # Initialize connectors
        self.sqs_connector = SQSSimulatorConnector(queue_name=sqs_queue, bootstrap_servers=bootstrap_servers)
        self.kafka_connector = KafkaConnector(bootstrap_servers=bootstrap_servers, topic=kafka_topic)
        
        # Initialize stream processor
        self.stream_processor = TestStreamProcessor(self.sqs_connector, self.kafka_connector)
        
    def test_process_message(self) -> bool:
        """
        Test processing a single message.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("Testing process_message method")
        
        # Generate and send a test message to SQS
        message = TestDataGenerator.generate_user_event()
        message_id = self.sqs_connector.send_message(message)
        
        if not message_id:
            logger.error("Failed to send message to SQS simulator")
            return False
        
        logger.info(f"Sent message to SQS simulator with ID: {message_id}")
        
        # Wait for message to be available
        time.sleep(1)
        
        # Receive the message from SQS
        messages = self.sqs_connector.receive_messages(max_messages=1)
        
        if not messages:
            logger.error("Failed to receive message from SQS simulator")
            return False
        
        # Process the message
        result = self.stream_processor.process_message(messages[0])
        
        if result:
            logger.info("Successfully processed message")
            # Ensure message is sent to Kafka
            self.kafka_connector.flush()
            
            # Delete the message from SQS
            self.sqs_connector.delete_message(messages[0]['receipt_handle'])
            
            return True
        else:
            logger.error("Failed to process message")
            return False
    
    def test_start_stop_streaming(self) -> bool:
        """
        Test starting and stopping the streaming process.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("Testing start_streaming and stop_streaming methods")
        
        # Start streaming
        self.stream_processor.start_streaming()
        
        # Verify that streaming is running
        if not self.stream_processor.running:
            logger.error("Stream processor did not start")
            return False
        
        logger.info("Stream processor started successfully")
        
        # Wait a moment
        time.sleep(2)
        
        # Stop streaming
        self.stream_processor.stop_streaming()
        
        # Verify that streaming is stopped
        if self.stream_processor.running:
            logger.error("Stream processor did not stop")
            return False
        
        logger.info("Stream processor stopped successfully")
        return True
    
    def test_metrics_collection(self) -> bool:
        """
        Test metrics collection during streaming.
        
        Returns:
            True if metrics are collected properly, False otherwise
        """
        logger.info("Testing metrics collection during streaming")
        
        # Start streaming
        self.stream_processor.start_streaming()
        
        # Generate and send multiple messages to SQS
        num_messages = 10
        logger.info(f"Sending {num_messages} test messages to SQS simulator")
        
        for _ in range(num_messages):
            message = TestDataGenerator.generate_user_event()
            self.sqs_connector.send_message(message)
        
        # Wait for messages to be processed
        logger.info(f"Waiting for messages to be processed...")
        wait_time = 0
        metrics = None
        
        # Wait up to 30 seconds for all messages to be processed
        while wait_time < 30:
            time.sleep(5)
            wait_time += 5
            
            metrics = self.stream_processor.get_metrics()
            processed = metrics.get('messages_processed', 0)
            
            logger.info(f"Processed {processed} of {num_messages} messages...")
            
            if processed >= num_messages:
                break
        
        # Stop streaming
        self.stream_processor.stop_streaming()
        
        # Get final metrics
        metrics = self.stream_processor.get_metrics()
        
        logger.info(f"Final metrics: {json.dumps(metrics, indent=2)}")
        
        # Verify metrics
        if 'messages_processed' not in metrics:
            logger.error("Metrics do not include 'messages_processed'")
            return False
        
        if metrics['messages_processed'] < 1:
            logger.error("No messages were processed according to metrics")
            return False
        
        if 'total_execution_time' not in metrics or metrics['total_execution_time'] <= 0:
            logger.error("Invalid 'total_execution_time' in metrics")
            return False
        
        logger.info("Metrics collection test passed")
        return True
    
    def test_end_to_end_streaming(self, num_messages: int = 20, run_time: int = 30) -> bool:
        """
        Test complete end-to-end streaming process with multiple messages.
        
        Args:
            num_messages: Number of messages to send
            run_time: How long to run the streaming process in seconds
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"=== Testing end-to-end streaming with {num_messages} messages, running for {run_time}s ===")
        
        # Start streaming
        self.stream_processor.start_streaming()
        
        # Generate and send test messages in a separate thread
        def send_test_messages():
            logger.info(f"Starting to send {num_messages} test messages...")
            
            for i in range(num_messages):
                # Mix up the data types for a more realistic test
                data_type = "mixed"
                if i % 3 == 0:
                    data_type = "user_event"
                elif i % 3 == 1:
                    data_type = "sensor_data"
                else:
                    data_type = "log_entry"
                
                message = TestDataGenerator.generate_batch(1, data_type)[0]
                self.sqs_connector.send_message(message)
                
                # Add a small delay between messages
                time.sleep(0.5)
                
            logger.info(f"Completed sending {num_messages} test messages")
        
        # Start sending messages in background
        message_thread = threading.Thread(target=send_test_messages)
        message_thread.start()
        
        # Wait for specified run time
        logger.info(f"Streaming process will run for {run_time} seconds...")
        
        # Log metrics periodically
        start_time = time.time()
        end_time = start_time + run_time
        
        while time.time() < end_time:
            current_metrics = self.stream_processor.get_metrics()
            processed = current_metrics.get('messages_processed', 0)
            errors = current_metrics.get('processing_errors', 0) + current_metrics.get('kafka_send_errors', 0)
            
            logger.info(f"Processed: {processed}, Errors: {errors}")
            
            time.sleep(5)
        
        # Wait for message thread to complete
        message_thread.join()
        
        # Stop streaming
        self.stream_processor.stop_streaming()
        
        # Get final metrics
        final_metrics = self.stream_processor.get_metrics()
        
        logger.info(f"Final metrics: {json.dumps(final_metrics, indent=2)}")
        
        # Verify metrics
        messages_processed = final_metrics.get('messages_processed', 0)
        total_errors = final_metrics.get('processing_errors', 0) + final_metrics.get('kafka_send_errors', 0)
        
        # Success criteria: at least 50% of messages processed successfully with fewer than 25% errors
        success = (messages_processed >= num_messages / 2) and (total_errors < num_messages / 4)
        
        if success:
            logger.info(f"End-to-end streaming test passed: processed {messages_processed} messages with {total_errors} errors")
        else:
            logger.error(f"End-to-end streaming test failed: processed only {messages_processed} of {num_messages} messages with {total_errors} errors")
        
        return success
    
    def run_all_tests(self):
        """
        Run all stream processor tests.
        """
        logger.info("=== Starting Stream Processor Tests ===")
        
        # Test individual methods
        process_message = self.test_process_message()
        start_stop = self.test_start_stop_streaming()
        metrics = self.test_metrics_collection()
        
        # Test end-to-end streaming
        end_to_end = self.test_end_to_end_streaming()
        
        # Overall success
        success = process_message and start_stop and metrics and end_to_end
        
        if success:
            logger.info("=== All Stream Processor Tests Passed ===")
        else:
            logger.error("=== Some Stream Processor Tests Failed ===")
            
        return success

if __name__ == "__main__":
    # Run the tests
    test = StreamProcessorTest()
    test.run_all_tests()
