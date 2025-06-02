"""
Test script for the Kafka Connector.
Tests the functionality of the Kafka Connector for producing and managing topics.
"""
import json
import logging
import time
import sys
import os
from typing import List, Dict, Any

# Add project root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.src.connectors.kafka_connector import KafkaConnector
# Update import path to use test-data folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'test-data'))
from data_generator import TestDataGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class KafkaConnectorTest:
    """
    Test class for the Kafka Connector.
    """
    
    def __init__(self, bootstrap_servers: str = "localhost:29092", topic: str = "test-kafka-topic"):
        """
        Initialize the test class.
        
        Args:
            bootstrap_servers: Kafka bootstrap servers
            topic: Name of the test Kafka topic
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.connector = KafkaConnector(bootstrap_servers=bootstrap_servers, topic=topic)
        
    def test_ensure_topic_exists(self):
        """
        Test ensuring that a topic exists.
        """
        logger.info(f"Testing ensure_topic_exists method for topic: {self.topic}")
        
        try:
            self.connector.ensure_topic_exists(self.topic)
            logger.info(f"Topic {self.topic} exists or was created successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to ensure topic exists: {e}")
            return False
    
    def test_create_topics(self, topics: List[str] = None):
        """
        Test creating multiple topics.
        
        Args:
            topics: List of topic names to create
        """
        if topics is None:
            topics = [f"test-topic-{i}" for i in range(1, 4)]
            
        logger.info(f"Testing create_topics method for topics: {', '.join(topics)}")
        
        try:
            self.connector.create_topics(topics)
            logger.info(f"Successfully created topics: {', '.join(topics)}")
            return True
        except Exception as e:
            logger.error(f"Failed to create topics: {e}")
            return False
    
    def test_send_message(self) -> bool:
        """
        Test sending a message to a Kafka topic.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Testing send_message method to topic: {self.topic}")
        
        # Generate test message
        message = TestDataGenerator.generate_user_event()
        
        # Send message
        result = self.connector.send_message(message)
        
        if result:
            logger.info("Successfully sent message to Kafka")
        else:
            logger.error("Failed to send message to Kafka")
            
        return result
    
    def test_send_batch(self, count: int = 10, data_type: str = "mixed") -> bool:
        """
        Test sending a batch of messages to a Kafka topic.
        
        Args:
            count: Number of messages to send
            data_type: Type of test data to generate
            
        Returns:
            True if all messages were sent successfully, False otherwise
        """
        logger.info(f"Testing sending batch of {count} {data_type} messages to topic: {self.topic}")
        
        # Generate batch of test messages
        messages = TestDataGenerator.generate_batch(count, data_type)
        
        # Send messages
        success_count = 0
        
        for message in messages:
            result = self.connector.send_message(message)
            if result:
                success_count += 1
        
        logger.info(f"Successfully sent {success_count} of {count} messages")
        
        # Flush producer to ensure all messages are sent
        self.connector.flush()
        
        return success_count == count
    
    def test_send_with_key(self) -> bool:
        """
        Test sending a message with a key to a Kafka topic.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Testing send_message with key to topic: {self.topic}")
        
        # Generate test message
        message = TestDataGenerator.generate_user_event()
        key = f"key-{message['user_id']}"
        
        # Send message with key
        result = self.connector.send_message(message, key=key)
        
        if result:
            logger.info(f"Successfully sent message with key: {key}")
        else:
            logger.error("Failed to send message with key")
            
        return result
    
    def run_all_tests(self):
        """
        Run all Kafka connector tests.
        """
        logger.info("=== Starting Kafka Connector Tests ===")
        
        # Test topic management
        topic_exists = self.test_ensure_topic_exists()
        if not topic_exists:
            logger.error("Failed to ensure topic exists, cannot proceed with other tests")
            return False
        
        create_topics = self.test_create_topics()
        
        # Test message sending
        send_message = self.test_send_message()
        send_batch = self.test_send_batch(5)
        send_with_key = self.test_send_with_key()
        
        # Flush any remaining messages
        self.connector.flush()
        
        # Overall success
        success = topic_exists and create_topics and send_message and send_batch and send_with_key
        
        if success:
            logger.info("=== All Kafka Connector Tests Passed ===")
        else:
            logger.error("=== Some Kafka Connector Tests Failed ===")
            
        return success

if __name__ == "__main__":
    # Run the tests
    test = KafkaConnectorTest()
    test.run_all_tests()
