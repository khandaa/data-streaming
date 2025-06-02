"""
Streaming Application 2: Real-time Data Processor

This application consumes data from Kafka for real-time processing and alerting.
It demonstrates how the same data stream can be used by different applications.
"""
import json
import logging
import time
import threading
import signal
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable

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
logger = logging.getLogger('streaming_app2')

class RealTimeProcessor:
    """
    Real-time processor that consumes data from Kafka for immediate processing and alerting.
    """
    
    def __init__(self, bootstrap_servers: Optional[str] = None, 
                 topic: Optional[str] = None, 
                 group_id: str = 'realtime-processor'):
        """
        Initialize the real-time processor.
        
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
            'alerts_triggered': 0,
            'processing_errors': 0,
            'last_message_time': None,
            'processing_latency_ms': 0
        }
        
        # Alert thresholds and handlers
        self.alert_thresholds = {
            'high_priority': lambda msg: msg.get('data', {}).get('priority') == 'high',
            'error_message': lambda msg: 'error' in str(msg.get('data', {})).lower(),
            'large_payload': lambda msg: len(json.dumps(msg)) > 10000  # Alert on messages > 10KB
        }
        
        # Alert history (in a real application, this would be in a database)
        self.alert_history = []
        
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
    
    def check_alerts(self, message: Dict[str, Any]) -> List[str]:
        """
        Check if a message triggers any alerts.
        
        Args:
            message: Message from Kafka
            
        Returns:
            List of triggered alert names
        """
        triggered_alerts = []
        
        for alert_name, threshold_func in self.alert_thresholds.items():
            try:
                if threshold_func(message):
                    triggered_alerts.append(alert_name)
                    self.metrics['alerts_triggered'] += 1
                    
                    # Add to alert history
                    alert_record = {
                        'alert_name': alert_name,
                        'message_id': message.get('message_id', 'unknown'),
                        'timestamp': datetime.now().isoformat(),
                        'message_snippet': str(message)[:100] + '...' if len(str(message)) > 100 else str(message)
                    }
                    self.alert_history.append(alert_record)
                    
                    # Keep alert history at a reasonable size
                    if len(self.alert_history) > 1000:
                        self.alert_history = self.alert_history[-1000:]
                        
                    # Log the alert
                    logger.warning(f"Alert '{alert_name}' triggered by message {message.get('message_id', 'unknown')}")
            except Exception as e:
                logger.error(f"Error checking alert '{alert_name}': {e}")
        
        return triggered_alerts
    
    def process_message(self, message: Dict[str, Any]):
        """
        Process a message for real-time handling.
        
        Args:
            message: Message from Kafka
        """
        try:
            # Process message in real-time (example: enrich with additional data)
            enriched_data = {
                'original_message': message,
                'processing_time': datetime.now().isoformat(),
                'source_topic': self.topic
            }
            
            # Check if any alerts are triggered
            triggered_alerts = self.check_alerts(message)
            
            if triggered_alerts:
                enriched_data['triggered_alerts'] = triggered_alerts
                # In a real application, this could send notifications or take other actions
                
            # Real-time processing would normally do something with the enriched data
            # For example, store it in a database, send it to another system, etc.
            
            # Update metrics
            self.metrics['messages_processed'] += 1
            self.metrics['last_message_time'] = datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"Error processing message for real-time handling: {e}")
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
            logger.warning("Real-time processor is already running")
            return
        
        self.stop_event.clear()
        self.running = True
        
        # Start the consumer in a separate thread
        self.consumer_thread = threading.Thread(
            target=self.consume_messages,
            daemon=True
        )
        self.consumer_thread.start()
        logger.info("Real-time processor started")
    
    def stop(self):
        """
        Stop consuming messages and close the consumer.
        """
        if not self.running:
            logger.warning("Real-time processor is not running")
            return
        
        logger.info("Stopping real-time processor...")
        self.stop_event.set()
        
        # Wait for the thread to finish
        if hasattr(self, 'consumer_thread') and self.consumer_thread.is_alive():
            self.consumer_thread.join(timeout=10)
        
        # Close the consumer
        if self.consumer:
            self.consumer.close()
            
        self.running = False
        logger.info("Real-time processor stopped")
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current metrics.
        
        Returns:
            Dictionary of metrics
        """
        return self.metrics
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the most recent alerts.
        
        Args:
            limit: Maximum number of alerts to return
            
        Returns:
            List of recent alerts
        """
        return self.alert_history[-limit:] if self.alert_history else []

if __name__ == '__main__':
    # Create and start the real-time processor
    processor = RealTimeProcessor()
    processor.start()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(60)
            metrics = processor.get_metrics()
            logger.info(f"Current metrics: {metrics}")
            
            # Print recent alerts
            recent_alerts = processor.get_recent_alerts(5)
            if recent_alerts:
                logger.info(f"Recent alerts: {recent_alerts}")
                
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down...")
        processor.stop()
