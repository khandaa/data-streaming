"""
Isolated test script for testing components without external dependencies.
This script properly mocks all Kafka interactions.
"""
import json
import logging
import sys
import os
import time
import uuid
from typing import Dict, Any, List
import unittest
from unittest.mock import MagicMock, patch, Mock

# Add project root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import test data generator directly
sys.path.insert(0, os.path.dirname(__file__))
from test_data_generator import TestDataGenerator

class TestSQSSimulatorInIsolation(unittest.TestCase):
    """
    Test SQS Simulator connector in isolation.
    """
    
    def setUp(self):
        """Set up test environment."""
        # Create patch for the confluent_kafka.Producer
        self.producer_patch = patch('confluent_kafka.Producer')
        self.mock_producer_class = self.producer_patch.start()
        self.mock_producer = Mock()
        self.mock_producer_class.return_value = self.mock_producer
        
        # Create patch for the confluent_kafka.Consumer
        self.consumer_patch = patch('confluent_kafka.Consumer')
        self.mock_consumer_class = self.consumer_patch.start()
        self.mock_consumer = Mock()
        self.mock_consumer_class.return_value = self.mock_consumer
        
        # Create patch for the confluent_kafka.admin.AdminClient
        self.admin_patch = patch('confluent_kafka.admin.AdminClient')
        self.mock_admin_class = self.admin_patch.start()
        self.mock_admin = Mock()
        self.mock_admin_class.return_value = self.mock_admin
        
        # Configure the mocks
        self.mock_producer.produce.return_value = None
        self.mock_producer.flush.return_value = 0
        
        # For poll method, return None to simulate no messages
        self.mock_consumer.poll.return_value = None
        
        # Setup the mock message that will be returned when needed
        self.mock_message = Mock()
        self.mock_message.error.return_value = None
        self.mock_message.value.return_value = json.dumps({
            "message_id": "test-id",
            "body": {"test": "message"},
            "attributes": {"SenderId": "test-sender"}
        }).encode('utf-8')
        self.mock_message.key.return_value = "test-key".encode('utf-8')
        self.mock_message.topic.return_value = "test-queue"
        self.mock_message.partition.return_value = 0
        self.mock_message.offset.return_value = 123
        
        # Import the SQS simulator connector after patching
        from backend.src.connectors.sqs_simulator_connector import SQSSimulatorConnector
        self.sqs = SQSSimulatorConnector(queue_name="test-queue", bootstrap_servers="localhost:9092")
    
    def tearDown(self):
        """Clean up after test."""
        self.producer_patch.stop()
        self.consumer_patch.stop()
        self.admin_patch.stop()
    
    def test_send_message(self):
        """Test sending a message."""
        # Configure mock
        self.mock_producer.produce.return_value = None
        
        # Generate test message
        test_message = TestDataGenerator.generate_user_event()
        
        # Call the method
        message_id = self.sqs.send_message(test_message)
        
        # Assertions
        self.assertIsNotNone(message_id, "Message ID should not be None")
        self.mock_producer.produce.assert_called_once()
        self.mock_producer.flush.assert_called_once()
    
    def test_receive_messages_empty(self):
        """Test receiving messages when none are available."""
        # Configure mock to return no messages
        self.mock_consumer.poll.return_value = None
        
        # Call the method
        messages = self.sqs.receive_messages()
        
        # Assertions
        self.assertEqual(len(messages), 0, "Should receive no messages")
    
    def test_receive_messages(self):
        """Test receiving messages."""
        # Configure mock to return a message once, then None
        self.mock_consumer.poll.side_effect = [self.mock_message, None]
        
        # Call the method
        messages = self.sqs.receive_messages(max_messages=1)
        
        # Assertions
        self.assertEqual(len(messages), 1, "Should receive 1 message")
        self.assertEqual(messages[0]['body']['test'], "message", "Message content should match")
        self.assertIn('receipt_handle', messages[0], "Message should have receipt handle")
    
    def test_delete_message(self):
        """Test deleting a message."""
        # Create a receipt handle
        receipt_handle = f"test-queue:0:123:{uuid.uuid4()}"
        
        # Call the method
        result = self.sqs.delete_message(receipt_handle)
        
        # Assertions
        self.assertTrue(result, "Delete should succeed")
        self.mock_consumer.commit.assert_called_once()


class TestKafkaConnectorInIsolation(unittest.TestCase):
    """
    Test Kafka connector in isolation.
    """
    
    def setUp(self):
        """Set up test environment."""
        # Create patch for the confluent_kafka.Producer
        self.producer_patch = patch('confluent_kafka.Producer')
        self.mock_producer_class = self.producer_patch.start()
        self.mock_producer = Mock()
        self.mock_producer_class.return_value = self.mock_producer
        
        # Create patch for the confluent_kafka.admin.AdminClient
        self.admin_patch = patch('confluent_kafka.admin.AdminClient')
        self.mock_admin_class = self.admin_patch.start()
        self.mock_admin = Mock()
        self.mock_admin_class.return_value = self.mock_admin
        
        # Configure the mocks
        self.mock_producer.produce.return_value = None
        self.mock_producer.flush.return_value = 0
        
        # Configure admin client for topic creation
        self.mock_admin.create_topics.return_value = Mock()
        self.mock_admin.create_topics.return_value.result.return_value = {}
        
        # Import the Kafka connector after patching
        from backend.src.connectors.kafka_connector import KafkaConnector
        self.kafka = KafkaConnector(bootstrap_servers="localhost:9092", topic="test-topic")
    
    def tearDown(self):
        """Clean up after test."""
        self.producer_patch.stop()
        self.admin_patch.stop()
    
    def test_send_message(self):
        """Test sending a message."""
        # Generate test message
        test_message = TestDataGenerator.generate_user_event()
        
        # Call the method
        result = self.kafka.send_message(test_message)
        
        # Assertions
        self.assertTrue(result, "Send should succeed")
        self.mock_producer.produce.assert_called_once()
    
    def test_send_message_with_key(self):
        """Test sending a message with key."""
        # Generate test message
        test_message = TestDataGenerator.generate_user_event()
        test_key = "test-key"
        
        # Call the method
        result = self.kafka.send_message(test_message, key=test_key)
        
        # Assertions
        self.assertTrue(result, "Send with key should succeed")
        self.mock_producer.produce.assert_called_once()
    
    def test_ensure_topic_exists(self):
        """Test ensuring topic exists."""
        # Configure mock
        self.mock_admin.list_topics.return_value = Mock()
        self.mock_admin.list_topics.return_value.topics = {"other-topic": Mock()}
        
        # Call the method
        self.kafka.ensure_topic_exists("test-topic")
        
        # Assertions
        self.mock_admin.create_topics.assert_called_once()


class TestStreamProcessor(unittest.TestCase):
    """
    Test stream processor functionality.
    """
    
    def setUp(self):
        """Set up test environment."""
        # Create mock SQS and Kafka connectors
        self.mock_sqs = Mock()
        self.mock_kafka = Mock()
        
        # Configure SQS mock
        self.mock_sqs.receive_messages.return_value = [
            {
                'message_id': 'test-id',
                'body': {'test': 'message'},
                'receipt_handle': 'test-receipt-handle'
            }
        ]
        self.mock_sqs.delete_message.return_value = True
        
        # Configure Kafka mock
        self.mock_kafka.send_message.return_value = True
        self.mock_kafka.flush.return_value = None
        
        # Import the stream processor after setting up mocks
        from backend.src.utils.test_stream_processor import TestStreamProcessor
        self.processor = TestStreamProcessor(self.mock_sqs, self.mock_kafka)
    
    def test_process_message(self):
        """Test processing a single message."""
        # Create a test message
        message = {
            'message_id': 'test-id',
            'body': {'test': 'message'},
            'receipt_handle': 'test-receipt-handle'
        }
        
        # Call the method
        result = self.processor.process_message(message)
        
        # Assertions
        self.assertTrue(result, "Process should succeed")
        self.mock_kafka.send_message.assert_called_once()
    
    def test_start_stop_streaming(self):
        """Test starting and stopping streaming."""
        # Start streaming
        self.processor.start_streaming()
        
        # Assertions
        self.assertTrue(self.processor.running, "Processor should be running")
        
        # Stop streaming
        self.processor.stop_streaming()
        
        # Assertions
        self.assertFalse(self.processor.running, "Processor should not be running")
    
    def test_get_metrics(self):
        """Test getting metrics."""
        # Get metrics
        metrics = self.processor.get_metrics()
        
        # Assertions
        self.assertIsInstance(metrics, dict, "Metrics should be a dictionary")
        self.assertIn('messages_processed', metrics, "Metrics should include messages_processed")


if __name__ == '__main__':
    unittest.main()
