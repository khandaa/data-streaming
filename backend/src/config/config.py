"""
Configuration module for the data streaming application.
Loads environment variables and provides configuration settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# AWS SQS Configuration
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL', '')
SQS_SUBNET_ID = os.getenv('SQS_SUBNET_ID', '')

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'sqs-data')
KAFKA_SUBNET_ID = os.getenv('KAFKA_SUBNET_ID', '')
KAFKA_SECURITY_PROTOCOL = os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT')
KAFKA_SASL_MECHANISM = os.getenv('KAFKA_SASL_MECHANISM', '')
KAFKA_SASL_USERNAME = os.getenv('KAFKA_SASL_USERNAME', '')
KAFKA_SASL_PASSWORD = os.getenv('KAFKA_SASL_PASSWORD', '')

# Application Configuration
APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
APP_PORT = int(os.getenv('APP_PORT', '5000'))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ENV = os.getenv('ENV', 'development')

# Admin credentials
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# VPC and Subnet Configuration for AWS
VPC_ID = os.getenv('VPC_ID', '')
