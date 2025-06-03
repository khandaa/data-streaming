#!/usr/bin/env python3
"""
Docker Test Script for SQS Simulator with Kafka.

This script tests the SQS Simulator and Kafka connector with a real Kafka cluster
running in Docker. It sends and receives messages to verify the setup is working correctly.
"""
import json
import logging
import os
import sys
import time
import uuid

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Add test-data folder to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'test-data'))

# Import test data generator
from data_generator import TestDataGenerator

# Import connectors
from backend.src.connectors.sqs_simulator_connector import SQSSimulatorConnector
from backend.src.connectors.kafka_connector import KafkaConnector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_sqs_simulator():
    """Test the SQS Simulator with a real Kafka cluster."""
    logger.info("Testing SQS Simulator with real Kafka cluster")
    
    # Create SQS Simulator with Kafka at localhost (using port 29092 for Docker mapping)
    sqs = SQSSimulatorConnector(
        queue_name="test-queue",
        bootstrap_servers="localhost:29092"
    )
    
    # Generate test data
    test_data = TestDataGenerator.generate_batch(
        data_type="user_event",
        count=5
    )
    
    message_ids = []
    
    # Send messages
    logger.info(f"Sending {len(test_data)} messages to SQS Simulator")
    for message in test_data:
        message_id = sqs.send_message(message)
        message_ids.append(message_id)
        logger.info(f"Sent message with ID: {message_id}")
    
    # Wait for messages to be processed
    time.sleep(2)
    
    # Receive messages
    logger.info("Receiving messages from SQS Simulator")
    received_messages = sqs.receive_messages(max_messages=10, wait_time=5)
    
    logger.info(f"Received {len(received_messages)} messages")
    for message in received_messages:
        logger.info(f"Message ID: {message['message_id']}")
        
        # Delete the message
        receipt_handle = message['receipt_handle']
        result = sqs.delete_message(receipt_handle)
        if result:
            logger.info(f"Deleted message with receipt handle: {receipt_handle[:20]}...")
        else:
            logger.error(f"Failed to delete message with receipt handle: {receipt_handle[:20]}...")
    
    return len(message_ids), len(received_messages)


def test_kafka_connector():
    """Test the Kafka Connector with a real Kafka cluster."""
    logger.info("Testing Kafka Connector with real Kafka cluster")
    
    # Create Kafka Connector
    kafka = KafkaConnector(
        bootstrap_servers="localhost:29092",
        topic="test-topic"
    )
    
    # Generate test data
    test_data = TestDataGenerator.generate_batch(
        data_type="user_event",
        count=5
    )
    
    # Send messages
    logger.info(f"Sending {len(test_data)} messages to Kafka")
    for i, message in enumerate(test_data):
        key = f"test-key-{i}"
        result = kafka.send_message(message, key=key)
        if result:
            logger.info(f"Sent message with key: {key}")
        else:
            logger.error(f"Failed to send message with key: {key}")
    
    # Flush to ensure messages are delivered
    kafka.flush()
    
    return len(test_data)


if __name__ == "__main__":
    logger.info("Starting Docker test")
    
    try:
        # Test SQS Simulator
        sent_count, received_count = test_sqs_simulator()
        logger.info(f"SQS Simulator test complete - Sent: {sent_count}, Received: {received_count}")
        
        # Test Kafka Connector
        sent_to_kafka = test_kafka_connector()
        logger.info(f"Kafka Connector test complete - Sent: {sent_to_kafka}")
        
        # Overall result
        if sent_count > 0 and received_count > 0 and sent_to_kafka > 0:
            logger.info("Docker test PASSED!")
        else:
            logger.error("Docker test FAILED!")
            
    except Exception as e:
        logger.exception(f"Error during Docker test: {e}")
