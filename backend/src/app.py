"""
Main application module for the data streaming service.
This Flask application provides APIs for monitoring and managing the data streaming process.
"""
import logging
import threading
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

from backend.src.config.config import (
    APP_HOST,
    APP_PORT,
    DEBUG,
    LOG_LEVEL,
    LOG_FORMAT,
    KAFKA_TOPIC
)
from backend.src.connectors.sqs_connector import SQSConnector
from backend.src.connectors.kafka_connector import KafkaConnector
from backend.src.utils.stream_processor import StreamProcessor

# Set up logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__)
CORS(app)

# Initialize connectors
sqs_connector = SQSConnector()
kafka_connector = KafkaConnector()

# Initialize stream processor
stream_processor = StreamProcessor(sqs_connector, kafka_connector)

# Metrics for monitoring
metrics = {
    'messages_processed': 0,
    'processing_errors': 0,
    'last_processing_time': None,
    'kafka_send_errors': 0,
    'stream_status': 'stopped'
}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'sqs_connected': sqs_connector is not None,
        'kafka_connected': kafka_connector is not None,
        'stream_status': metrics['stream_status']
    })

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get current metrics."""
    return jsonify(metrics)

@app.route('/api/stream/start', methods=['POST'])
def start_stream():
    """Start the streaming process."""
    if metrics['stream_status'] == 'running':
        return jsonify({'message': 'Stream is already running'}), 400
    
    try:
        # Start the stream processor in a background thread
        stream_thread = threading.Thread(
            target=stream_processor.start_streaming,
            args=(metrics,),
            daemon=True
        )
        stream_thread.start()
        
        metrics['stream_status'] = 'running'
        logger.info("Stream processing started")
        return jsonify({'message': 'Stream processing started successfully'})
    except Exception as e:
        logger.error(f"Failed to start stream: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stream/stop', methods=['POST'])
def stop_stream():
    """Stop the streaming process."""
    if metrics['stream_status'] == 'stopped':
        return jsonify({'message': 'Stream is already stopped'}), 400
    
    try:
        stream_processor.stop_streaming()
        metrics['stream_status'] = 'stopped'
        logger.info("Stream processing stopped")
        return jsonify({'message': 'Stream processing stopped successfully'})
    except Exception as e:
        logger.error(f"Failed to stop stream: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Get available Kafka topics."""
    try:
        topics = stream_processor.get_available_topics()
        return jsonify({'topics': topics})
    except Exception as e:
        logger.error(f"Failed to get topics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/topics', methods=['POST'])
def create_topic():
    """Create a new Kafka topic."""
    try:
        data = request.get_json()
        topic_name = data.get('name')
        partitions = data.get('partitions', 3)
        replication = data.get('replication', 3)
        
        if not topic_name:
            return jsonify({'error': 'Topic name is required'}), 400
        
        kafka_connector.create_topics([topic_name], num_partitions=partitions, replication_factor=replication)
        return jsonify({'message': f'Topic {topic_name} created successfully'})
    except Exception as e:
        logger.error(f"Failed to create topic: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Admin login endpoint."""
    from backend.src.config.config import ADMIN_USERNAME, ADMIN_PASSWORD
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return jsonify({'message': 'Login successful', 'role': 'admin'})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

def start_scheduler():
    """Start the background scheduler for periodic tasks."""
    scheduler = BackgroundScheduler()
    
    # Add periodic tasks here if needed
    # Example: scheduler.add_job(check_stream_health, 'interval', minutes=5)
    
    scheduler.start()
    logger.info("Background scheduler started")

if __name__ == '__main__':
    # Start the background scheduler
    start_scheduler()
    
    # Start the Flask application
    logger.info(f"Starting application on {APP_HOST}:{APP_PORT}")
    app.run(host=APP_HOST, port=APP_PORT, debug=DEBUG)
