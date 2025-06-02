# AWS SQS to Kafka Streaming Application

## Project Overview

The AWS SQS to Kafka Streaming Application is a distributed data streaming solution that facilitates seamless data transfer from AWS SQS queues to Kafka topics across different network subnets. The application includes connectors, stream processors, and consumer applications that enable real-time data processing and analytics.

## Table of Contents

- [System Architecture](#system-architecture)
- [Key Components](#key-components)
- [Data Flow](#data-flow)
- [Setup and Installation](#setup-and-installation)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Admin Guide](#admin-guide)
- [User Guide](#user-guide)
- [Troubleshooting](#troubleshooting)
- [FAQs](#faqs)

## System Architecture

The application follows a distributed architecture with the following components:

```
+-------------------+      +------------------+      +-------------------+
|                   |      |                  |      |                   |
|   AWS SQS Queue   |----->|  Stream Processor|----->|   Kafka Cluster   |
|   (Subnet A)      |      |                  |      |   (Subnet B)      |
|                   |      |                  |      |                   |
+-------------------+      +------------------+      +---------+---------+
                                                               |
                                                               |
                                                               v
                      +----------------+          +------------+------------+
                      |                |          |                         |
                      |  Frontend      |<-------->|  Backend Flask API      |
                      |  Dashboard     |          |                         |
                      |                |          |                         |
                      +----------------+          +-------------------------+
                                                               |
                                                               |
                            +-----------------------+-----------------------+
                            |                       |                       |
                     +------v------+         +------v------+        +------v------+
                     |             |         |             |        |             |
                     | Analytics   |         | Real-time   |        | Admin       |
                     | Processor   |         | Processor   |        | Dashboard   |
                     |             |         |             |        |             |
                     +-------------+         +-------------+        +-------------+
```

### Network Configuration

The application operates across different subnets:
- AWS SQS operates in Subnet A
- Kafka cluster operates in Subnet B
- Communication between these subnets is facilitated through AWS VPC endpoints

This cross-subnet architecture provides several benefits:
- Network isolation for security
- Compliance with organizational network policies
- Ability to integrate with diverse infrastructure setups

## Key Components

### 1. Connectors

#### SQS Connector
- Connects to AWS SQS queues
- Handles authentication and authorization
- Retrieves and deletes messages
- Implements error handling and retry logic
- Supports cross-subnet communication via VPC endpoints

#### Kafka Connector
- Connects to Kafka clusters
- Publishes messages to topics
- Creates and manages topics
- Handles security (SASL/SSL)
- Provides metrics on connection status and performance

### 2. Stream Processor
- Core component that manages data flow
- Retrieves messages from SQS
- Processes and transforms data as needed
- Publishes to Kafka topics
- Tracks metrics and provides monitoring
- Implements error handling and recovery

### 3. Streaming Applications

#### Analytics Processor
- Consumes data from Kafka for analytics purposes
- Calculates metrics and statistics
- Processes data in batches
- Provides insights for business intelligence

#### Real-time Data Processor
- Consumes data from Kafka for immediate processing
- Triggers alerts based on defined conditions
- Monitors real-time metrics
- Enables quick response to critical events

### 4. Backend API
- Flask-based RESTful API
- Provides endpoints for stream control (start/stop)
- Retrieves metrics and status information
- Manages Kafka topics
- Handles authentication and authorization
- Serves as the intermediary between the frontend and streaming components

### 5. Frontend Dashboard
- React-based user interface
- Displays streaming status and metrics
- Provides controls for managing the stream
- Visualizes data and performance metrics
- Includes admin dashboard for configuration
- Features comprehensive help and documentation

## Data Flow

1. **Data Ingestion**: Messages are retrieved from AWS SQS queue in Subnet A via the SQS connector.
2. **Processing**: The Stream Processor handles the messages, performing any necessary transformations or validations.
3. **Publication**: Processed messages are published to Kafka topics in Subnet B via the Kafka connector.
4. **Consumption**: Two streaming applications consume data from Kafka for different purposes:
   - Analytics Processor for metrics and insights
   - Real-time Processor for immediate alerting
5. **Monitoring and Control**: The Flask API provides management capabilities and metrics to the frontend dashboard.
6. **Visualization and Administration**: The React frontend displays status and metrics while allowing for system management.

## Technology Stack

### Backend
- **Language**: Python 3.8+
- **Framework**: Flask
- **AWS SDK**: boto3
- **Kafka Libraries**: confluent-kafka, kafka-python
- **Additional Libraries**: marshmallow, python-dotenv, pydantic, apscheduler, prometheus-client

### Frontend
- **Framework**: React
- **UI Libraries**: Material UI, Bootstrap
- **Data Visualization**: Chart.js, React Chartjs 2
- **HTTP Client**: Axios
- **Routing**: React Router

### Infrastructure
- **Message Queue**: AWS SQS
- **Message Broker**: Apache Kafka
- **Network**: AWS VPC with cross-subnet communication
