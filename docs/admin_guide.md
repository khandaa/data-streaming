# Administrator Guide

This guide provides detailed instructions for administrators of the AWS SQS to Kafka Streaming Application.

## Table of Contents

- [Admin Dashboard](#admin-dashboard)
- [System Controls](#system-controls)
- [Configuration Management](#configuration-management)
- [Security](#security)
- [Monitoring and Logging](#monitoring-and-logging)
- [Maintenance Tasks](#maintenance-tasks)
- [Troubleshooting](#troubleshooting)

## Admin Dashboard

The Admin Dashboard is a privileged section of the application that provides powerful controls and configurations for the system administrator.

### Accessing the Admin Dashboard

1. Navigate to `/admin/login` or click the Admin icon in the sidebar
2. Enter your admin credentials:
   - Default username: `admin`
   - Default password: `admin`
   - **Important:** Change the default credentials immediately after first login

### Dashboard Layout

The Admin Dashboard consists of four main tabs:

1. **System Controls**: Start/stop streaming services and perform system operations
2. **Configuration**: View and edit system configuration settings
3. **Logs**: View system logs and diagnostics
4. **Security**: Manage authentication and access control

## System Controls

The System Controls tab provides actions to manage the streaming service.

### Available Actions

- **Start Stream**: Begin processing messages from SQS to Kafka
- **Stop Stream**: Halt message processing
- **Restart Service**: Restart the entire application (both frontend and backend)
- **Flush Metrics**: Clear accumulated metrics data
- **Test Connections**: Verify connectivity to SQS and Kafka
- **Export Metrics**: Download metrics data as CSV or JSON

### Managing Stream Process

To start the stream process:

1. Navigate to the System Controls tab
2. Click the "Start Stream" button
3. Confirm the action in the dialog
4. The status indicator will turn green when the stream is running

To stop the stream process:

1. Navigate to the System Controls tab
2. Click the "Stop Stream" button
3. Confirm the action in the dialog
4. The status indicator will turn red when the stream is stopped

**Note**: Stopping the stream will not process any new messages from SQS, but will not affect already published messages in Kafka.

## Configuration Management

The Configuration tab allows administrators to view and modify the system configuration.

### Configuration Sections

- **AWS Configuration**: SQS and VPC settings
- **Kafka Configuration**: Broker and topic settings
- **Application Configuration**: General app settings
- **Stream Processor Configuration**: Processing parameters

### Editing Configuration

To edit configuration settings:

1. Navigate to the Configuration tab
2. Select the section you want to modify
3. Click the "Edit" button
4. Make your changes in the form
5. Click "Save Changes"

**Important Notes**:
- Some configuration changes require a system restart to take effect
- Sensitive values (passwords, access keys) are masked in the UI
- Configuration is stored in the `.env` file on the server

### Critical Configuration Parameters

| Parameter | Description | Default | Impact if Changed |
|-----------|-------------|---------|------------------|
| AWS_ACCESS_KEY_ID | AWS access key | - | Auth failure if incorrect |
| AWS_SECRET_ACCESS_KEY | AWS secret key | - | Auth failure if incorrect |
| SQS_QUEUE_URL | URL of SQS queue | - | Cannot access queue if incorrect |
| KAFKA_BOOTSTRAP_SERVERS | Kafka server addresses | kafka:9092 | Connection failure if incorrect |
| KAFKA_TOPIC | Default Kafka topic | sqs-data | Messages will go to wrong topic |
| APP_PORT | Backend API port | 5000 | API access on different port |
| ADMIN_USERNAME | Admin username | admin | Login issues if changed without notice |
| ADMIN_PASSWORD | Admin password | admin | Login issues if changed without notice |

## Security

The Security tab provides tools for managing authentication and access control.

### User Management

The default admin account is created with:
- Username: `admin`
- Password: `admin`

**IMPORTANT**: Change these credentials immediately after installation.

To change admin credentials:

1. Navigate to the Security tab
2. In the User Management section, click "Change Credentials"
3. Enter the current password and new credentials
4. Click "Update Credentials"

### Authentication

The application uses JWT (JSON Web Tokens) for authentication:

- Tokens expire after 24 hours by default
- All admin API calls require a valid token
- Failed login attempts are logged

### Best Practices

- Change default credentials immediately
- Use strong passwords (12+ characters, mixed case, numbers, symbols)
- Rotate credentials regularly
- Limit admin access to authorized personnel only
- Use environment-specific credentials for development, testing, and production

## Monitoring and Logging

The Logs tab provides access to system logs and diagnostic information.

### Log Levels

The application uses the following log levels:

- **DEBUG**: Detailed information for debugging
- **INFO**: General operational information
- **WARNING**: Potential issues that don't prevent operation
- **ERROR**: Errors that prevent specific functions
- **CRITICAL**: Severe errors that may cause system failure

### Viewing Logs

To view system logs:

1. Navigate to the Logs tab
2. Use the filters to narrow down log entries:
   - By log level (INFO, WARNING, ERROR, etc.)
   - By component (SQS, Kafka, API, etc.)
   - By time range
3. Click "Refresh" to update the log view
4. Click "Export" to download logs for offline analysis

### Log Retention

By default, logs are retained for:
- 7 days for DEBUG and INFO levels
- 30 days for WARNING, ERROR, and CRITICAL levels

### Metrics Collection

The system collects the following metrics:

- Messages processed per second
- Average processing time
- Error rate
- SQS queue depth
- Kafka producer latency
- System resource utilization (CPU, memory, disk)

These metrics can be viewed in real-time on the Streaming Status page and historically in the Admin Dashboard.

## Maintenance Tasks

Regular maintenance ensures the system runs smoothly and reliably.

### Scheduled Tasks

| Task | Frequency | Description |
|------|-----------|-------------|
| Log Rotation | Weekly | Archive and compress old logs |
| Metric Cleanup | Monthly | Remove old metrics data |
| Configuration Backup | Monthly | Backup system configuration |
| Security Audit | Quarterly | Review access logs and credentials |
| Update Dependencies | Quarterly | Update software dependencies |

### Backup and Recovery

To backup the system:

1. Export the configuration from the Admin Dashboard
2. Backup the `.env` file
3. Backup any custom scripts or modifications

To recover the system:

1. Reinstall the application if necessary
2. Restore the `.env` file
3. Import the configuration from backup
4. Restart the application

## Troubleshooting

This section provides solutions for common issues administrators may encounter.

### Common Issues

#### Stream Not Starting

**Symptoms**:
- Stream status remains "stopped" after clicking "Start Stream"
- Error messages in logs about connection failures

**Possible Causes and Solutions**:
1. **AWS Credentials Invalid**
   - Check AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in configuration
   - Verify the IAM user has proper permissions for SQS

2. **SQS Queue Not Accessible**
   - Verify the SQS_QUEUE_URL is correct
   - Check network connectivity to AWS region
   - Verify VPC endpoint configuration if using cross-subnet communication

3. **Kafka Connection Issues**
   - Verify KAFKA_BOOTSTRAP_SERVERS is correct
   - Check network connectivity to Kafka cluster
   - Verify Kafka credentials if using authentication

#### High Error Rate

**Symptoms**:
- Many ERROR level log entries
- Increasing error count in metrics
- Poor message throughput

**Possible Causes and Solutions**:
1. **Message Format Issues**
   - Check SQS message format compatibility
   - Review any message transformation logic

2. **Kafka Topic Configuration**
   - Verify topic exists and is properly configured
   - Check partition count and replication factor

3. **Resource Constraints**
   - Check system CPU and memory usage
   - Consider scaling up resources if consistently high

#### Performance Degradation

**Symptoms**:
- Decreasing messages processed per second
- Increasing processing latency
- System resource utilization growing

**Possible Causes and Solutions**:
1. **Increasing Queue Depth**
   - Check if producers are sending more messages than can be processed
   - Consider scaling stream processor or increasing batch size

2. **Network Latency**
   - Check network performance between subnets
   - Monitor VPC endpoint performance

3. **Resource Exhaustion**
   - Check disk space, especially for logs
   - Monitor memory usage and potential leaks
   - Verify CPU utilization isn't consistently above 80%

### Diagnostic Procedures

#### Connection Testing

To test SQS connectivity:

1. In the Admin Dashboard, go to System Controls
2. Click "Test SQS Connection"
3. Review the test results for specific error messages

To test Kafka connectivity:

1. In the Admin Dashboard, go to System Controls
2. Click "Test Kafka Connection"
3. Review the test results for specific error messages

#### Log Analysis

For effective log analysis:

1. Set LOG_LEVEL to DEBUG temporarily to get more detailed information
2. Filter logs by component to isolate issues
3. Look for patterns in ERROR and WARNING messages
4. Check timestamps to correlate issues across components

#### Support Resources

If you cannot resolve an issue, contact support with:

1. Exported logs from the problem period
2. System configuration (with sensitive data redacted)
3. Steps to reproduce the issue
4. Error messages and timestamps

## Default Admin Credentials

The system is installed with default admin credentials that should be changed immediately:

- **Username**: admin
- **Password**: admin

These credentials provide full access to the Admin Dashboard and all administrative functions.

**IMPORTANT**: Change these credentials on first login by going to the Security tab in the Admin Dashboard.
