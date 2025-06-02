# Installation and Setup Guide

This guide will walk you through the process of setting up and running the AWS SQS to Kafka Streaming Application.

## Prerequisites

Before you begin, ensure you have the following prerequisites:

- Python 3.8 or higher
- Node.js 14 or higher
- npm 6 or higher
- AWS account with SQS access
- Kafka cluster access
- Git

## System Requirements

- OS: Linux, macOS, or Windows with WSL
- RAM: Minimum 4GB (8GB recommended)
- Disk Space: At least 1GB free space
- Network: Internet connection for AWS and Kafka access

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd data_streaming
```

### 2. Backend Setup

#### Create a Virtual Environment

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv ../venv

# Activate the virtual environment
# On Linux/macOS
source ../venv/bin/activate
# On Windows
..\venv\Scripts\activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

```bash
# Copy the example environment file
cp ../.env.example ../.env

# Edit the .env file with your actual configuration values
nano ../.env
```

Update the following variables in the .env file:
- AWS credentials and region
- SQS queue URL and subnet IDs
- Kafka bootstrap servers and credentials
- Application host and port
- Admin credentials (default: admin/admin)

### 3. Frontend Setup

```bash
# Navigate to the frontend directory
cd ../frontend

# Install dependencies
npm install

# Create a production build
npm run build
```

## Configuration

### AWS Configuration

Ensure your AWS credentials have the following permissions:
- SQS:ReceiveMessage
- SQS:DeleteMessage
- SQS:GetQueueAttributes
- SQS:SendMessage

If using VPC endpoints for cross-subnet communication, you'll also need to configure:
- VPC endpoints for SQS
- Appropriate security groups and network ACLs

### Kafka Configuration

For the Kafka connection, you'll need:
- Bootstrap servers addresses
- Authentication details (if using SASL/SSL)
- Topic creation permissions
- Appropriate network routing between subnets

## Running the Application

### Start the Backend

```bash
# Ensure you're in the backend directory with the virtual environment activated
cd backend
source ../venv/bin/activate

# Start the Flask application
python src/app.py
```

### Start the Frontend (Development Mode)

```bash
# In a separate terminal, navigate to the frontend directory
cd frontend

# Start the development server
npm start
```

### Start the Frontend (Production Mode)

```bash
# For production, serve the built files using a web server
# Example with serve
npm install -g serve
serve -s build
```

### Start the Streaming Applications

```bash
# In separate terminals, start each streaming application
# Ensure the virtual environment is activated in each terminal

# Start the Analytics Processor
python backend/src/streaming_app1.py

# Start the Real-time Data Processor
python backend/src/streaming_app2.py
```

## Verification

To verify that the application is running correctly:

1. Open a web browser and navigate to `http://localhost:3000` (or the configured frontend port)
2. Log in with the admin credentials (default: admin/admin)
3. Check the Streaming Status page to ensure all connections are healthy
4. Navigate to the Topics page to view available Kafka topics
5. Check the Admin Dashboard for system controls and logs

## Troubleshooting Common Issues

### Connection Issues

If you encounter connection issues with AWS SQS or Kafka:

1. Verify your credentials in the .env file
2. Check network connectivity between subnets
3. Ensure VPC endpoints are correctly configured
4. Verify that security groups and network ACLs allow the necessary traffic

### Application Startup Issues

If the application fails to start:

1. Check the logs for specific error messages
2. Verify that all dependencies are installed
3. Ensure the .env file has all required variables
4. Check that ports are not already in use by other applications

## Next Steps

After successful installation, refer to the following documentation:
- [User Guide](/docs/user_guide.md) for general usage
- [Admin Guide](/docs/admin_guide.md) for administration tasks
- [API Reference](/docs/api_reference.md) for backend API details
- [Development Guide](/docs/development_guide.md) for contributing to the project
