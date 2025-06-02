"""
Test script for the SQS Simulator Connector.
Tests the functionality of the SQS Simulator using Kafka.
"""
import json
import logging
import time
import sys
import os
from typing import List, Dict, Any

# Add project root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.src.connectors.sqs_simulator_connector import SQSSimulatorConnector
# Update import path to use test-data folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'test-data'))
from data_generator import TestDataGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SQSSimulatorTest:
    """
    Test class for the SQS Simulator Connector.
    """
    
    def __init__(self, bootstrap_servers: str = "localhost:29092", queue_name: str = "sqs-queue-1"):
        """
        Initialize the test class.
        
        Args:
            bootstrap_servers: Kafka bootstrap servers
            queue_name: Name of the SQS simulator queue (Kafka topic)
        """
        self.bootstrap_servers = bootstrap_servers
        self.queue_name = queue_name
        self.connector = SQSSimulatorConnector(queue_name=queue_name, bootstrap_servers=bootstrap_servers)
        
    def test_send_message(self) -> str:
        """
        Test sending a message to the SQS simulator.
        
        Returns:
            Message ID if successful, None otherwise
        """
        logger.info("Testing send_message method")
        
        # Generate test message
        message = TestDataGenerator.generate_user_event()
        
        # Send message
        message_id = self.connector.send_message(message)
        
        if message_id:
            logger.info(f"Successfully sent message with ID: {message_id}")
        else:
            logger.error("Failed to send message")
            
        return message_id
    
    def test_send_batch(self, count: int = 10, data_type: str = "mixed") -> List[str]:
        """
        Test sending a batch of messages to the SQS simulator.
        
        Args:
            count: Number of messages to send
            data_type: Type of test data to generate
            
        Returns:
            List of successfully sent message IDs
        """
        logger.info(f"Testing sending batch of {count} {data_type} messages")
        
        # Generate batch of test messages
        messages = TestDataGenerator.generate_batch(count, data_type)
        
        # Send messages and collect IDs
        message_ids = []
        
        for message in messages:
            message_id = self.connector.send_message(message)
            if message_id:
                message_ids.append(message_id)
        
        logger.info(f"Successfully sent {len(message_ids)} of {count} messages")
        
        return message_ids
    
    def test_receive_messages(self, max_messages: int = 10) -> List[Dict[str, Any]]:
        """
        Test receiving messages from the SQS simulator.
        
        Args:
            max_messages: Maximum number of messages to receive
            
        Returns:
            List of received messages
        """
        logger.info(f"Testing receive_messages method (max: {max_messages})")
        
        # Receive messages
        messages = self.connector.receive_messages(max_messages=max_messages)
        
        logger.info(f"Received {len(messages)} messages")
        
        return messages
    
    def test_delete_message(self, receipt_handle: str) -> bool:
        """
        Test deleting a message from the SQS simulator.
        
        Args:
            receipt_handle: Receipt handle of the message to delete
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Testing delete_message method for receipt handle: {receipt_handle[:15]}...")
        
        # Delete message
        result = self.connector.delete_message(receipt_handle)
        
        if result:
            logger.info("Successfully deleted message")
        else:
            logger.error("Failed to delete message")
            
        return result
    
    def test_send_receive_delete_cycle(self, count: int = 5) -> bool:
        """
        Test the complete send-receive-delete message cycle.
        
        Args:
            count: Number of messages to send
            
        Returns:
            True if all stages completed successfully, False otherwise
        """
        logger.info(f"Testing complete send-receive-delete cycle with {count} messages")
        
        # Step 1: Send messages
        sent_ids = self.test_send_batch(count)
        
        if len(sent_ids) != count:
            logger.error(f"Failed to send all {count} messages, only sent {len(sent_ids)}")
            return False
        
        # Step 2: Wait a moment for messages to be available
        logger.info("Waiting for messages to be available...")
        time.sleep(2)
        
        # Step 3: Receive messages
        received_messages = self.test_receive_messages(max_messages=count)
        
        if len(received_messages) == 0:
            logger.error("Failed to receive any messages")
            return False
        
        # Step 4: Delete received messages
        delete_success = True
        
        for message in received_messages:
            receipt_handle = message['receipt_handle']
            if not self.test_delete_message(receipt_handle):
                delete_success = False
                
        if delete_success:
            logger.info("All messages were successfully deleted")
        else:
            logger.warning("Some messages could not be deleted")
        
        # Step 5: Verify deletion by trying to receive them again
        logger.info("Verifying deletion by trying to receive messages again...")
        verification_messages = self.test_receive_messages(max_messages=count)
        
        # We should receive fewer messages than before if deletion worked
        logger.info(f"Received {len(verification_messages)} messages after deletion (should be fewer than {len(received_messages)})")
        
        return delete_success and len(verification_messages) < len(received_messages)
    
    def run_all_tests(self):
        """
        Run all SQS simulator tests.
        """
        logger.info("=== Starting SQS Simulator Tests ===")
        
        # Test individual methods
        self.test_send_message()
        self.test_send_batch(5)
        self.test_receive_messages()
        
        # Test complete cycle
        cycle_success = self.test_send_receive_delete_cycle()
        
        if cycle_success:
            logger.info("=== All SQS Simulator Tests Passed ===")
        else:
            logger.error("=== Some SQS Simulator Tests Failed ===")
            
        return cycle_success

if __name__ == "__main__":
    # Run the tests
    test = SQSSimulatorTest()
    test.run_all_tests()
