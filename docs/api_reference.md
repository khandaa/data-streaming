# API Reference

This document provides detailed information about all the REST API endpoints available in the AWS SQS to Kafka Streaming Application.

## Base URL

All API endpoints are relative to the base URL:

```
http://localhost:5000/api
```

This can be configured using the `APP_HOST` and `APP_PORT` environment variables.

## Authentication

Most API endpoints require authentication. The application uses JWT (JSON Web Token) based authentication.

**Headers**:
```
Authorization: Bearer <token>
```

To obtain a token, use the login endpoint.

## Endpoints

### Authentication

#### Login

Authenticates a user and returns a JWT token.

- **URL**: `/auth/login`
- **Method**: `POST`
- **Auth Required**: No
- **Request Body**:
  ```json
  {
    "username": "admin",
    "password": "admin"
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "user": {
        "username": "admin",
        "role": "admin"
      }
    }
    ```
- **Error Response**:
  - **Code**: 401 UNAUTHORIZED
  - **Content**:
    ```json
    {
      "error": "Invalid credentials"
    }
    ```

### Stream Management

#### Get Stream Status

Returns the current status of the streaming service.

- **URL**: `/stream/status`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "status": "running",
      "uptime_seconds": 3600,
      "messages_processed": 1500,
      "messages_per_second": 15.5,
      "errors": 2,
      "last_error": "Connection timeout at 2025-06-01T12:34:56Z"
    }
    ```

#### Start Stream

Starts the streaming service.

- **URL**: `/stream/start`
- **Method**: `POST`
- **Auth Required**: Yes
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "message": "Stream started successfully",
      "status": "running"
    }
    ```
- **Error Response**:
  - **Code**: 400 BAD REQUEST
  - **Content**:
    ```json
    {
      "error": "Stream is already running"
    }
    ```

#### Stop Stream

Stops the streaming service.

- **URL**: `/stream/stop`
- **Method**: `POST`
- **Auth Required**: Yes
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "message": "Stream stopped successfully",
      "status": "stopped"
    }
    ```
- **Error Response**:
  - **Code**: 400 BAD REQUEST
  - **Content**:
    ```json
    {
      "error": "Stream is already stopped"
    }
    ```

### Metrics

#### Get System Metrics

Returns detailed metrics about the streaming system.

- **URL**: `/metrics`
- **Method**: `GET`
- **Auth Required**: Yes
- **Query Parameters**:
  - `timeframe`: (optional) Duration in minutes to retrieve metrics for. Default is 60.
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "sqs": {
        "connection_status": "healthy",
        "queue_size": 245,
        "oldest_message_age_seconds": 120
      },
      "kafka": {
        "connection_status": "healthy",
        "broker_count": 3,
        "topics": 5
      },
      "stream": {
        "status": "running",
        "messages_processed": 1500,
        "processing_time_ms_avg": 42.5,
        "errors": 2,
        "error_rate": 0.13
      },
      "system": {
        "cpu_usage_percent": 45.2,
        "memory_usage_percent": 62.8,
        "disk_usage_percent": 78.3
      },
      "history": [
        {
          "timestamp": "2025-06-02T14:00:00Z",
          "messages_processed": 123,
          "errors": 0
        },
        {
          "timestamp": "2025-06-02T14:05:00Z",
          "messages_processed": 145,
          "errors": 1
        }
        // ... more history data
      ]
    }
    ```

#### Get Health Status

Returns the health status of all system components.

- **URL**: `/health`
- **Method**: `GET`
- **Auth Required**: No
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "status": "healthy",
      "components": {
        "api": {
          "status": "healthy",
          "uptime_seconds": 3600
        },
        "sqs": {
          "status": "healthy",
          "message": "Connected to SQS queue"
        },
        "kafka": {
          "status": "healthy",
          "message": "Connected to Kafka brokers"
        },
        "processor": {
          "status": "healthy",
          "message": "Stream processor is running"
        }
      }
    }
    ```

### Kafka Topic Management

#### List Topics

Returns a list of all Kafka topics.

- **URL**: `/topics`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "topics": [
        {
          "name": "sqs-data",
          "partitions": 3,
          "replication_factor": 2,
          "configs": {
            "cleanup.policy": "delete",
            "retention.ms": 604800000
          }
        },
        {
          "name": "analytics-processed",
          "partitions": 2,
          "replication_factor": 2,
          "configs": {
            "cleanup.policy": "compact",
            "retention.ms": 1209600000
          }
        }
      ]
    }
    ```

#### Create Topic

Creates a new Kafka topic.

- **URL**: `/topics`
- **Method**: `POST`
- **Auth Required**: Yes
- **Request Body**:
  ```json
  {
    "name": "new-topic",
    "partitions": 3,
    "replication_factor": 2,
    "configs": {
      "cleanup.policy": "delete",
      "retention.ms": 604800000
    }
  }
  ```
- **Success Response**:
  - **Code**: 201 CREATED
  - **Content**:
    ```json
    {
      "message": "Topic created successfully",
      "topic": {
        "name": "new-topic",
        "partitions": 3,
        "replication_factor": 2
      }
    }
    ```
- **Error Response**:
  - **Code**: 400 BAD REQUEST
  - **Content**:
    ```json
    {
      "error": "Topic already exists"
    }
    ```

#### Delete Topic

Deletes a Kafka topic.

- **URL**: `/topics/{topic_name}`
- **Method**: `DELETE`
- **Auth Required**: Yes
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "message": "Topic deleted successfully",
      "topic": "topic-name"
    }
    ```
- **Error Response**:
  - **Code**: 404 NOT FOUND
  - **Content**:
    ```json
    {
      "error": "Topic not found"
    }
    ```

### Streaming Applications

#### List Streaming Applications

Returns information about all streaming applications.

- **URL**: `/apps`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "apps": [
        {
          "id": "analytics-processor",
          "name": "Analytics Processor",
          "status": "running",
          "messages_processed": 12500,
          "last_processed": "2025-06-02T15:30:45Z",
          "description": "Processes data for analytics purposes"
        },
        {
          "id": "realtime-processor",
          "name": "Real-time Data Processor",
          "status": "running",
          "messages_processed": 15200,
          "last_processed": "2025-06-02T15:31:12Z",
          "description": "Processes data in real-time for alerts and monitoring"
        }
      ]
    }
    ```

#### Get Streaming Application

Returns information about a specific streaming application.

- **URL**: `/apps/{app_id}`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "id": "analytics-processor",
      "name": "Analytics Processor",
      "status": "running",
      "messages_processed": 12500,
      "last_processed": "2025-06-02T15:30:45Z",
      "description": "Processes data for analytics purposes",
      "metrics": {
        "cpu_usage_percent": 35.2,
        "memory_usage_mb": 256,
        "processing_time_ms_avg": 42.5,
        "error_rate": 0.05
      },
      "config": {
        "batch_size": 100,
        "processing_interval_ms": 5000,
        "input_topic": "sqs-data",
        "output_topic": "analytics-processed"
      }
    }
    ```
- **Error Response**:
  - **Code**: 404 NOT FOUND
  - **Content**:
    ```json
    {
      "error": "Application not found"
    }
    ```

### System Configuration

#### Get Configuration

Returns the current system configuration.

- **URL**: `/config`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "aws": {
        "region": "us-east-1",
        "sqs_queue_url": "https://sqs.us-east-1.amazonaws.com/123456789012/data-stream-queue",
        "sqs_subnet_id": "subnet-12345",
        "vpc_id": "vpc-12345"
      },
      "kafka": {
        "bootstrap_servers": "kafka:9092",
        "topic": "sqs-data",
        "security_protocol": "PLAINTEXT",
        "kafka_subnet_id": "subnet-67890"
      },
      "app": {
        "host": "0.0.0.0",
        "port": 5000,
        "debug": false,
        "log_level": "INFO"
      }
    }
    ```

#### Update Configuration

Updates the system configuration.

- **URL**: `/config`
- **Method**: `PUT`
- **Auth Required**: Yes
- **Request Body**:
  ```json
  {
    "aws": {
      "region": "us-west-2",
      "sqs_queue_url": "https://sqs.us-west-2.amazonaws.com/123456789012/data-stream-queue"
    },
    "kafka": {
      "bootstrap_servers": "new-kafka:9092"
    },
    "app": {
      "log_level": "DEBUG"
    }
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "message": "Configuration updated successfully",
      "restart_required": true
    }
    ```
- **Error Response**:
  - **Code**: 400 BAD REQUEST
  - **Content**:
    ```json
    {
      "error": "Invalid configuration values",
      "details": {
        "aws.region": "Invalid region specified"
      }
    }
    ```

### System Logs

#### Get Logs

Returns system logs.

- **URL**: `/logs`
- **Method**: `GET`
- **Auth Required**: Yes
- **Query Parameters**:
  - `level`: (optional) Log level filter (INFO, WARNING, ERROR, DEBUG). Default is all levels.
  - `component`: (optional) Component filter (api, sqs, kafka, processor). Default is all components.
  - `limit`: (optional) Maximum number of logs to return. Default is 100.
  - `offset`: (optional) Offset for pagination. Default is 0.
  - `from`: (optional) Start timestamp in ISO format. Default is 24 hours ago.
  - `to`: (optional) End timestamp in ISO format. Default is now.
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "total": 1250,
      "returned": 100,
      "logs": [
        {
          "timestamp": "2025-06-02T15:30:45Z",
          "level": "INFO",
          "component": "processor",
          "message": "Processed 100 messages from SQS"
        },
        {
          "timestamp": "2025-06-02T15:30:40Z",
          "level": "ERROR",
          "component": "kafka",
          "message": "Failed to connect to broker-3.kafka:9092"
        }
        // ... more logs
      ]
    }
    ```

## Error Handling

All API endpoints follow a consistent error format:

```json
{
  "error": "Error message",
  "details": {
    // Optional additional error details
  },
  "code": "ERROR_CODE"
}
```

Common error codes:

- `UNAUTHORIZED`: Authentication failed or token expired
- `FORBIDDEN`: User does not have permission to access the resource
- `NOT_FOUND`: Requested resource not found
- `BAD_REQUEST`: Invalid request parameters
- `INTERNAL_ERROR`: Server-side error

## Rate Limiting

API endpoints are rate-limited to prevent abuse. The current limits are:

- 60 requests per minute for authenticated users
- 10 requests per minute for unauthenticated endpoints

When rate limited, the API will respond with:

- **Code**: 429 TOO MANY REQUESTS
- **Content**:
  ```json
  {
    "error": "Rate limit exceeded",
    "retry_after": 45
  }
  ```

The `retry_after` field indicates the number of seconds to wait before making another request.
