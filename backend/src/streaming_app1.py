"""
Streaming Application 1: Data Analytics Processor

This application consumes data from Kafka and processes it for analytics purposes.
It demonstrates how the same data stream can be used by different applications.
"""
import json
import logging
import time
import threading
import signal
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional

from confluent_kafka import Consumer, KafkaError, KafkaException

from backend.src.config.config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
    KAFKA_SECURITY_PROTOCOL,
    KAFKA_SASL_MECHANISM,
    KAFKA_SASL_USERNAME,
    KAFKA_SASL_PASSWORD
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('streaming_app1')

class AnalyticsProcessor:
    """
    Analytics processor that consumes data from Kafka for analytics purposes.
    """
    
    def __init__(self, bootstrap_servers: Optional[str] = None, 
                 topic: Optional[str] = None, 
                 group_id: str = 'analytics-processor'):
        """
        Initialize the analytics processor.
        
        Args:
            bootstrap_servers: Kafka bootstrap servers
            topic: Kafka topic to consume from
            group_id: Consumer group ID
        """
        self.bootstrap_servers = bootstrap_servers or KAFKA_BOOTSTRAP_SERVERS
        self.topic = topic or KAFKA_TOPIC
        self.group_id = group_id
        self.consumer = None
        self.running = False
        self.stop_event = threading.Event()
        
        # Metrics for monitoring
        self.metrics = {
            'messages_processed': 0,
            'processing_errors': 0,
            'last_message_time': None,
            'processing_latency_ms': 0
        }
        
        # Analytics data store (in a real application, this would be a database)
        self.analytics_data = {
            'event_counts': {},
            'message_sizes': [],
            'processing_times': []
        }
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def _signal_handler(self, sig, frame):
        """
        Handle shutdown signals.
        """
        logger.info(f"Received signal {sig}, shutting down...")
        self.stop()
        sys.exit(0)
        
    def _connect(self):
        """
        Connect to Kafka and create a consumer.
        """
        # Configure Kafka consumer
        config = {
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
            'max.poll.interval.ms': 300000,  # 5 minutes
            'session.timeout.ms': 30000,  # 30 seconds
        }
        
        # Add security configuration if provided
        if KAFKA_SECURITY_PROTOCOL:
            config['security.protocol'] = KAFKA_SECURITY_PROTOCOL
            
        if KAFKA_SASL_MECHANISM and KAFKA_SASL_USERNAME and KAFKA_SASL_PASSWORD:
            config['sasl.mechanisms'] = KAFKA_SASL_MECHANISM
            config['sasl.username'] = KAFKA_SASL_USERNAME
            config['sasl.password'] = KAFKA_SASL_PASSWORD
        
        try:
            logger.info(f"Connecting to Kafka at {self.bootstrap_servers}")
            self.consumer = Consumer(config)
            self.consumer.subscribe([self.topic])
            logger.info(f"Connected to Kafka and subscribed to topic {self.topic}")
        except KafkaException as e:
            logger.error(f"Error connecting to Kafka: {e}")
            raise
    
    def process_message(self, message: Dict[str, Any]):
        """
        Process a message for analytics.
        
        Args:
            message: Message from Kafka
        """
        try:
            # Extract data for analytics
            if 'data' in message:
                # Track event counts by type (if available)
                event_type = message.get('data', {}).get('type', 'unknown')
                self.analytics_data['event_counts'][event_type] = \
                    self.analytics_data['event_counts'].get(event_type, 0) + 1
                
                # Track message size
                message_size = len(json.dumps(message))
                self.analytics_data['message_sizes'].append(message_size)
                
                # Keep only the last 1000 message sizes
                if len(self.analytics_data['message_sizes']) > 1000:
                    self.analytics_data['message_sizes'] = self.analytics_data['message_sizes'][-1000:]
                
                # Example analytics: calculate average size
                avg_size = sum(self.analytics_data['message_sizes']) / len(self.analytics_data['message_sizes'])
                logger.debug(f"Average message size: {avg_size:.2f} bytes")
                
                # Example analytics: log event counts periodically
                if self.metrics['messages_processed'] % 100 == 0:
                    logger.info(f"Event counts: {self.analytics_data['event_counts']}")
                
            # Update metrics
            self.metrics['messages_processed'] += 1
            self.metrics['last_message_time'] = datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"Error processing message for analytics: {e}")
            self.metrics['processing_errors'] += 1
    
    def consume_messages(self):
        """
        Continuously consume messages from Kafka and process them.
        """
        if not self.consumer:
            self._connect()
        
        logger.info("Starting to consume messages...")
        
        while not self.stop_event.is_set():
            try:
                # Poll for messages
                msg = self.consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition, not an error
                        logger.debug(f"Reached end of partition {msg.partition()}")
                    else:
                        logger.error(f"Kafka error: {msg.error()}")
                        self.metrics['processing_errors'] += 1
                else:
                    # Process the message
                    start_time = time.time()
                    
                    try:
                        # Parse message value
                        value = json.loads(msg.value().decode('utf-8'))
                        
                        # Process the message
                        self.process_message(value)
                        
                        # Commit the offset
                        self.consumer.commit(msg)
                        
                        # Calculate processing time
                        processing_time = (time.time() - start_time) * 1000  # in ms
                        self.metrics['processing_latency_ms'] = processing_time
                        self.analytics_data['processing_times'].append(processing_time)
                        
                        # Keep only the last 1000 processing times
                        if len(self.analytics_data['processing_times']) > 1000:
                            self.analytics_data['processing_times'] = self.analytics_data['processing_times'][-1000:]
                            
                    except json.JSONDecodeError as e:
                        logger.error(f"Error decoding message: {e}")
                        self.metrics['processing_errors'] += 1
                        self.consumer.commit(msg)  # Commit anyway to avoid getting stuck
                    
            except KafkaException as e:
                logger.error(f"Kafka error in consumer loop: {e}")
                self.metrics['processing_errors'] += 1
                time.sleep(1)  # Wait before retrying
    
    def start(self):
        """
        Start consuming and processing messages.
        """
        if self.running:
            logger.warning("Analytics processor is already running")
            return
        
        self.stop_event.clear()
        self.running = True
        
        # Start the consumer in a separate thread
        self.consumer_thread = threading.Thread(
            target=self.consume_messages,
            daemon=True
        )
        self.consumer_thread.start()
        logger.info("Analytics processor started")
    
    def stop(self):
        """
        Stop consuming messages and close the consumer.
        """
        if not self.running:
            logger.warning("Analytics processor is not running")
            return
        
        logger.info("Stopping analytics processor...")
        self.stop_event.set()
        
        # Wait for the thread to finish
        if hasattr(self, 'consumer_thread') and self.consumer_thread.is_alive():
            self.consumer_thread.join(timeout=10)
        
        # Close the consumer
        if self.consumer:
            self.consumer.close()
            
        self.running = False
        logger.info("Analytics processor stopped")
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current metrics.
        
        Returns:
            Dictionary of metrics
        """
        # Add some computed metrics
        if self.analytics_data['processing_times']:
            avg_processing_time = sum(self.analytics_data['processing_times']) / len(self.analytics_data['processing_times'])
            self.metrics['avg_processing_time_ms'] = avg_processing_time
        
        if self.analytics_data['message_sizes']:
            avg_message_size = sum(self.analytics_data['message_sizes']) / len(self.analytics_data['message_sizes'])
            self.metrics['avg_message_size_bytes'] = avg_message_size
        
        return self.metrics

if __name__ == '__main__':
    # Create and start the analytics processor
    processor = AnalyticsProcessor()
    processor.start()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(60)
            metrics = processor.get_metrics()
            logger.info(f"Current metrics: {metrics}")
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down...")
        processor.stop()
