"""
Test configuration for the application using Kafka SQS simulator.
This configuration is used for local testing and simulates AWS SQS with Kafka.
"""
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Kafka SQS Simulator Settings
SQS_SIMULATOR_ENABLED = True
SQS_SIMULATOR_QUEUE = "sqs-queue-1"

# AWS Settings (not used in simulation mode, but kept for compatibility)
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "test-access-key")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "test-secret-key")
SQS_QUEUE_URL = os.environ.get("SQS_QUEUE_URL", "https://sqs.us-east-1.amazonaws.com/123456789012/test-queue")
SQS_SUBNET_ID = os.environ.get("SQS_SUBNET_ID", "subnet-12345678")
VPC_ID = os.environ.get("VPC_ID", "vpc-12345678")

# Kafka Settings
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "streaming-topic")
KAFKA_SECURITY_PROTOCOL = os.environ.get("KAFKA_SECURITY_PROTOCOL", None)
KAFKA_SASL_MECHANISM = os.environ.get("KAFKA_SASL_MECHANISM", None)
KAFKA_SASL_USERNAME = os.environ.get("KAFKA_SASL_USERNAME", None)
KAFKA_SASL_PASSWORD = os.environ.get("KAFKA_SASL_PASSWORD", None)
KAFKA_SUBNET_ID = os.environ.get("KAFKA_SUBNET_ID", None)

# App Settings
APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = int(os.environ.get("APP_PORT", "5000"))
APP_DEBUG = os.environ.get("APP_DEBUG", "True").lower() == "true"
APP_LOG_LEVEL = os.environ.get("APP_LOG_LEVEL", "INFO")

# Admin Settings
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")

# JWT Settings
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-key")
JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", "3600"))  # 1 hour

# Test Settings
TEST_DATA_GENERATE_COUNT = int(os.environ.get("TEST_DATA_GENERATE_COUNT", "100"))
TEST_DATA_BATCH_SIZE = int(os.environ.get("TEST_DATA_BATCH_SIZE", "10"))
TEST_CONSUMER_GROUP = os.environ.get("TEST_CONSUMER_GROUP", "test-consumer-group")
