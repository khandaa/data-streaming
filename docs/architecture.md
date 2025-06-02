# Technical Architecture

This document describes the technical architecture of the AWS SQS to Kafka Streaming Application, including system components, data flow, and technical design decisions.

## System Architecture

The application follows a distributed architecture that spans multiple network subnets, facilitating data flow from AWS SQS to Kafka and then to consumer applications.

### Architecture Diagram

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

### Component Layering

The application follows a layered architecture:

1. **Infrastructure Layer**: AWS SQS, Kafka, and network infrastructure
2. **Connector Layer**: SQS and Kafka connectors that abstract away infrastructure details
3. **Processing Layer**: Stream processor that handles the core data flow logic
4. **API Layer**: Flask-based RESTful API that exposes functionality to clients
5. **Presentation Layer**: React-based frontend for visualization and control

## Key Components

### 1. AWS SQS Connector

The SQS Connector encapsulates all interaction with AWS SQS, including:

- Authentication and authorization with AWS
- Retrieving messages from the queue
- Deleting messages after successful processing
- Error handling and retry logic
- Cross-subnet communication via VPC endpoints

**Technical Details**:
- Implemented using Python's `boto3` library
- Uses asynchronous processing with threading
- Implements exponential backoff for rate limiting
- Provides metrics on queue depth and message age

### 2. Kafka Connector

The Kafka Connector manages all interaction with the Kafka cluster, including:

- Establishing and maintaining connections to Kafka brokers
- Publishing messages to topics
- Creating and managing topics
- Handling security (SASL/SSL)
- Providing connection status and metrics

**Technical Details**:
- Implemented using `confluent-kafka` library
- Supports various security protocols (PLAINTEXT, SASL_PLAINTEXT, SSL)
- Handles producer configuration for performance and reliability
- Implements idempotent production to prevent duplicates

### 3. Stream Processor

The Stream Processor is the core component that manages data flow from SQS to Kafka:

- Retrieves messages from SQS via the SQS Connector
- Processes and transforms messages as needed
- Publishes messages to Kafka via the Kafka Connector
- Tracks metrics and provides monitoring
- Implements error handling and recovery

**Technical Details**:
- Uses a producer-consumer pattern with a message queue
- Implements threading for parallel processing
- Provides configurable batch sizes and processing intervals
- Tracks processing time, throughput, and error rates
- Uses Python's `logging` module for comprehensive logging

### 4. Backend API

The Flask-based RESTful API provides:

- Endpoints for stream control (start/stop)
- Metrics and status information
- Kafka topic management
- Authentication and authorization
- Configuration management

**Technical Details**:
- Implemented using Flask and Flask-RESTful
- Uses JWT for authentication
- Implements rate limiting to prevent abuse
- Provides OpenAPI/Swagger documentation
- Uses environment variables for configuration

### 5. Frontend Dashboard

The React-based user interface includes:

- Streaming status and metrics visualization
- Controls for managing the stream
- Kafka topic management
- Admin dashboard for configuration
- Help and documentation

**Technical Details**:
- Built with React and React Router
- Uses Material UI and Bootstrap for styling
- Implements responsive design for all screen sizes
- Uses Axios for API communication
- Includes Chart.js for metrics visualization

## Cross-Subnet Communication

A key technical challenge in this architecture is enabling communication between different network subnets:

### VPC Endpoint Strategy

The application uses AWS VPC endpoints to facilitate communication across subnets:

1. **Interface Endpoint** for SQS: Allows private connectivity to SQS from Subnet A
2. **Transit Gateway**: Connects Subnet A and Subnet B, enabling communication between the Stream Processor and Kafka

### Network Configuration

The network configuration includes:

- Security groups that control inbound and outbound traffic
- Network ACLs for subnet-level security
- Route tables that direct traffic between subnets
- DNS resolution for VPC endpoints

## Data Flow

The data flow through the system follows these steps:

1. **Message Production**: External systems produce messages to AWS SQS queue in Subnet A
2. **Message Retrieval**: The SQS Connector receives messages from SQS
3. **Message Processing**: The Stream Processor processes messages
4. **Message Publication**: The Kafka Connector publishes messages to Kafka topics in Subnet B
5. **Message Consumption**: The Analytics Processor and Real-time Data Processor consume messages from Kafka
6. **Metrics Collection**: The system collects metrics at each step
7. **Visualization**: The Frontend Dashboard displays metrics and status information

## Security Model

The application implements a layered security model:

### Authentication and Authorization

- **AWS IAM**: Controls access to SQS resources
- **Kafka ACLs**: Controls access to Kafka topics
- **JWT**: Secures the Backend API
- **Environment Variables**: Stores sensitive configuration

### Network Security

- **VPC Isolation**: Separates components into different subnets
- **Security Groups**: Controls inbound and outbound traffic
- **Private Networking**: Uses private IP addresses where possible
- **Encryption in Transit**: Uses HTTPS for API and SSL for Kafka

### Data Security

- **Message Validation**: Validates messages before processing
- **Sanitization**: Cleanses data to prevent injection attacks
- **Secure Defaults**: Conservative default configurations

## Error Handling

The application implements comprehensive error handling:

### Error Categories

1. **Connection Errors**: Issues connecting to SQS or Kafka
2. **Authentication Errors**: Issues with credentials or permissions
3. **Message Format Errors**: Invalid message formats
4. **Processing Errors**: Issues during message processing
5. **System Errors**: Issues with the application itself

### Error Recovery Strategies

1. **Retry with Backoff**: For transient errors
2. **Circuit Breaking**: To prevent cascading failures
3. **Dead Letter Queues**: For messages that cannot be processed
4. **Alerting**: For critical errors requiring human intervention
5. **Graceful Degradation**: To maintain partial functionality during failures

## Monitoring and Metrics

The application collects and exposes various metrics:

### Operational Metrics

- **Message Throughput**: Messages processed per second
- **Processing Latency**: Time to process each message
- **Error Rate**: Percentage of messages that fail processing
- **Queue Depth**: Number of messages waiting in SQS
- **Connection Status**: Health of SQS and Kafka connections

### Business Metrics

- **Message Types**: Distribution of different message types
- **Processing Time by Type**: Processing time for each message type
- **Error Rate by Type**: Error rate for each message type

### System Metrics

- **CPU Usage**: Percentage of CPU utilization
- **Memory Usage**: Percentage of memory utilization
- **Disk Usage**: Percentage of disk utilization
- **Network Traffic**: Bytes sent and received

## Scalability and Performance

The application is designed for scalability and performance:

### Horizontal Scaling

- **Multiple Processors**: The Stream Processor can be scaled horizontally
- **Kafka Partitioning**: Kafka topics use multiple partitions for parallel processing
- **Stateless Design**: Components are stateless to facilitate scaling

### Performance Optimizations

- **Batch Processing**: Messages are processed in batches for efficiency
- **Connection Pooling**: Reuses connections to reduce overhead
- **Asynchronous Processing**: Non-blocking I/O for improved throughput
- **Caching**: Caches frequently accessed data
- **Compression**: Compresses messages to reduce network traffic

## Deployment Model

The application supports flexible deployment options:

### Container-Based Deployment

- **Docker Containers**: Each component is containerized
- **Docker Compose**: For development and testing
- **Kubernetes**: For production deployment

### Cloud Deployment

- **AWS ECS/EKS**: For container orchestration
- **AWS CloudFormation**: For infrastructure as code
- **AWS CloudWatch**: For monitoring and alerting

### On-Premises Deployment

- **Virtual Machines**: For traditional infrastructure
- **Physical Servers**: For high-performance requirements

## Disaster Recovery

The application includes disaster recovery capabilities:

### Backup and Restore

- **Configuration Backup**: Regular backups of configuration
- **Message Replay**: Ability to replay messages from SQS
- **State Recovery**: Recovery of processing state

### High Availability

- **Multiple Instances**: Running multiple instances of each component
- **Load Balancing**: Distributing load across instances
- **Failover**: Automatic failover to backup instances

## Dependencies

The application has the following key dependencies:

### Backend Dependencies

- **Python 3.8+**: Programming language
- **Flask**: Web framework
- **boto3**: AWS SDK
- **confluent-kafka**: Kafka client
- **pyjwt**: JWT implementation
- **marshmallow**: Object serialization/deserialization
- **apscheduler**: Task scheduling

### Frontend Dependencies

- **React**: UI library
- **Material UI**: Component library
- **Bootstrap**: CSS framework
- **Axios**: HTTP client
- **Chart.js**: Charting library
- **React Router**: Routing library
