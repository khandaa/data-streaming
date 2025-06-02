# Development Guide

This guide provides information for developers who want to contribute to or extend the AWS SQS to Kafka Streaming Application.

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Contribution Workflow](#contribution-workflow)
- [API and Component Reference](#api-and-component-reference)
- [Extending the Application](#extending-the-application)

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm 6 or higher
- Git
- Docker and Docker Compose (optional, for containerized development)
- AWS account (for SQS testing)
- Kafka cluster (or local Kafka setup)

### Local Setup

1. **Clone the repository**

```bash
git clone <repository-url>
cd data_streaming
```

2. **Set up the backend environment**

```bash
# Create and activate a virtual environment
python -m venv ../venv
source ../venv/bin/activate  # On Windows: ..\venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

3. **Set up the frontend environment**

```bash
cd ../frontend
npm install
```

4. **Configure environment variables**

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with local development settings
nano .env
```

For local development, you may want to use:
- LocalStack for AWS services
- Kafka running in Docker
- SQLite for any database needs

5. **Start the development servers**

```bash
# Terminal 1: Start the backend
cd backend
source ../venv/bin/activate
python src/app.py

# Terminal 2: Start the frontend
cd frontend
npm start
```

### Docker Development Environment

For a containerized development environment:

```bash
# Build and start the containers
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop the containers
docker-compose -f docker-compose.dev.yml down
```

## Project Structure

The project follows a structured layout for better organization:

```
data_streaming/
├── backend/                # Backend Flask application
│   ├── src/
│   │   ├── app.py          # Main application entry point
│   │   ├── config/         # Configuration modules
│   │   ├── connectors/     # SQS and Kafka connectors
│   │   ├── utils/          # Utility functions and classes
│   │   ├── models/         # Data models
│   │   ├── api/            # API endpoints
│   │   └── streaming_app*  # Streaming applications
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
├── frontend/               # Frontend React application
│   ├── src/
│   │   ├── components/     # Reusable React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service modules
│   │   ├── styles/         # CSS and styling
│   │   ├── utils/          # Utility functions
│   │   ├── App.js          # Main App component
│   │   └── index.js        # Entry point
│   ├── public/             # Static assets
│   └── package.json        # Node.js dependencies
├── docs/                   # Documentation
├── database/               # Database files (if any)
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore file
├── CHANGELOG.md            # Version history
└── README.md               # Project overview
```

## Coding Standards

### Python Coding Standards

We follow PEP 8 standards for Python code:

- Use 4 spaces for indentation (no tabs)
- Use snake_case for variable and function names
- Use CamelCase for class names
- Maximum line length of 79 characters
- Docstrings for all functions and classes
- Type hints where appropriate

Example:

```python
def process_message(message: dict) -> bool:
    """
    Process an SQS message and return success status.
    
    Args:
        message: The SQS message dictionary
        
    Returns:
        bool: True if processing succeeded, False otherwise
    """
    try:
        # Process the message
        return True
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return False
```

### JavaScript/React Coding Standards

For JavaScript and React code:

- Use camelCase for variable and function names
- Use PascalCase for component names
- Use 2 spaces for indentation
- Prefer functional components with hooks
- Use PropTypes or TypeScript for type checking
- Use JSDoc comments for functions

Example:

```javascript
/**
 * A component that displays stream metrics
 * @param {Object} props - Component props
 * @param {Object} props.metrics - The metrics data
 * @param {boolean} props.isLoading - Whether metrics are loading
 */
function StreamMetrics({ metrics, isLoading }) {
  if (isLoading) {
    return <div>Loading metrics...</div>;
  }
  
  return (
    <div className="metrics-container">
      <div className="metric-item">
        <span className="metric-label">Messages Processed:</span>
        <span className="metric-value">{metrics.messagesProcessed}</span>
      </div>
      {/* More metrics */}
    </div>
  );
}

StreamMetrics.propTypes = {
  metrics: PropTypes.object.isRequired,
  isLoading: PropTypes.bool
};

export default StreamMetrics;
```

## Testing Guidelines

We follow a test-driven development (TDD) approach:

1. Write tests first
2. Implement the feature
3. Verify tests pass
4. Refactor as needed

### Backend Testing

For backend testing, we use:
- `pytest` for unit and integration tests
- `coverage` for test coverage
- `pytest-mock` for mocking

Test files should:
- Be placed in the `backend/tests` directory
- Follow the naming convention `test_*.py`
- Include unit tests for individual functions
- Include integration tests for API endpoints
- Mock external services (AWS SQS, Kafka)

Example:

```python
# backend/tests/test_sqs_connector.py
import pytest
from unittest.mock import MagicMock, patch
from src.connectors.sqs_connector import SQSConnector

def test_receive_message_success():
    # Arrange
    mock_sqs_client = MagicMock()
    mock_sqs_client.receive_message.return_value = {
        'Messages': [
            {
                'MessageId': '123',
                'Body': 'test message',
                'ReceiptHandle': 'handle123'
            }
        ]
    }
    
    with patch('boto3.client', return_value=mock_sqs_client):
        connector = SQSConnector('queue_url')
        
        # Act
        result = connector.receive_message()
        
        # Assert
        assert result is not None
        assert result['MessageId'] == '123'
        assert result['Body'] == 'test message'
        mock_sqs_client.receive_message.assert_called_once()
```

To run backend tests:

```bash
cd backend
pytest
pytest --cov=src tests/  # With coverage
```

### Frontend Testing

For frontend testing, we use:
- Jest for unit tests
- React Testing Library for component tests
- Cypress for end-to-end tests

Test files should:
- Be placed next to the component they test
- Follow the naming convention `*.test.js` or `*.spec.js`
- Test component rendering and behavior
- Mock API calls

Example:

```javascript
// frontend/src/components/StreamMetrics.test.js
import { render, screen } from '@testing-library/react';
import StreamMetrics from './StreamMetrics';

test('displays loading state', () => {
  render(<StreamMetrics isLoading={true} metrics={{}} />);
  expect(screen.getByText(/loading metrics/i)).toBeInTheDocument();
});

test('displays metrics when loaded', () => {
  const metrics = {
    messagesProcessed: 1500,
    errorRate: 0.02
  };
  
  render(<StreamMetrics isLoading={false} metrics={metrics} />);
  expect(screen.getByText('1500')).toBeInTheDocument();
});
```

To run frontend tests:

```bash
cd frontend
npm test
npm run test:coverage  # With coverage
```

## Contribution Workflow

We follow a standard Git workflow for contributions:

1. **Fork the repository** (for external contributors)
2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Write tests** for your feature
4. **Implement your feature** and make sure tests pass
5. **Commit your changes** with a descriptive message
   ```bash
   git commit -m "Add feature: description of your feature"
   ```
6. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a pull request** against the main branch
8. **Address any review comments**
9. **Update the documentation** if necessary
10. **Update the CHANGELOG.md** file

### Commit Message Guidelines

Follow these guidelines for commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line
- Consider using the following prefixes:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation changes
  - `style:` for formatting changes
  - `refactor:` for code refactoring
  - `test:` for adding tests
  - `chore:` for maintenance tasks

## API and Component Reference

### Backend Components

#### SQS Connector

The `SQSConnector` class in `backend/src/connectors/sqs_connector.py` provides the following methods:

- `receive_message()`: Receives a message from SQS
- `delete_message(receipt_handle)`: Deletes a message from SQS
- `send_message(message_body)`: Sends a message to SQS
- `stream_messages()`: Continuously streams messages from SQS

#### Kafka Connector

The `KafkaConnector` class in `backend/src/connectors/kafka_connector.py` provides:

- `produce_message(topic, message)`: Produces a message to a Kafka topic
- `create_topic(topic_name, partitions, replication)`: Creates a new Kafka topic
- `list_topics()`: Lists all available Kafka topics

#### Stream Processor

The `StreamProcessor` class in `backend/src/utils/stream_processor.py` provides:

- `start()`: Starts the stream processing
- `stop()`: Stops the stream processing
- `get_metrics()`: Returns processing metrics

### Frontend Components

#### ApiService

The `ApiService` module in `frontend/src/services/ApiService.js` provides:

- `getStreamStatus()`: Gets the current stream status
- `startStream()`: Starts the stream
- `stopStream()`: Stops the stream
- `getMetrics()`: Gets system metrics
- `getTopics()`: Gets Kafka topics
- `createTopic(topic)`: Creates a new Kafka topic
- `login(credentials)`: Authenticates a user

#### UI Components

- `StreamingStatus`: Displays streaming status and metrics
- `Topics`: Manages Kafka topics
- `StreamingApps`: Shows streaming application status
- `AdminDashboard`: Provides admin controls and configuration

## Extending the Application

### Adding a New Connector

To add a new connector (e.g., for a different message queue):

1. Create a new file in `backend/src/connectors/`
2. Implement a class with similar methods to existing connectors
3. Add configuration in `backend/src/config/config.py`
4. Add tests in `backend/tests/`
5. Update the stream processor to use the new connector

Example for a RabbitMQ connector:

```python
# backend/src/connectors/rabbitmq_connector.py
import pika
import json
import logging

logger = logging.getLogger(__name__)

class RabbitMQConnector:
    def __init__(self, host, queue):
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None
        self._connect()
        
    def _connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)
            logger.info(f"Connected to RabbitMQ at {self.host}")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise
            
    def receive_message(self):
        # Implementation details
        pass
        
    def delete_message(self, delivery_tag):
        # Implementation details
        pass
        
    def send_message(self, message_body):
        # Implementation details
        pass
        
    def close(self):
        if self.connection:
            self.connection.close()
```

### Adding a New API Endpoint

To add a new API endpoint:

1. Define the endpoint in `backend/src/app.py` or create a new route file
2. Implement the endpoint logic
3. Add authentication if required
4. Add tests
5. Update the API documentation

Example:

```python
@app.route('/api/connector/status', methods=['GET'])
@jwt_required
def get_connector_status():
    try:
        sqs_status = sqs_connector.get_status()
        kafka_status = kafka_connector.get_status()
        
        return jsonify({
            'sqs': sqs_status,
            'kafka': kafka_status
        }), 200
    except Exception as e:
        logger.error(f"Error getting connector status: {e}")
        return jsonify({'error': str(e)}), 500
```

### Adding a New Frontend Page

To add a new frontend page:

1. Create a new component in `frontend/src/pages/`
2. Add the route in `frontend/src/App.js`
3. Add a menu item in `frontend/src/components/Sidebar.js`
4. Implement the page functionality
5. Add tests

Example:

```javascript
// frontend/src/pages/ConnectorStatus.js
import React, { useState, useEffect } from 'react';
import { Grid, Card, CardContent, Typography } from '@mui/material';
import ApiService from '../services/ApiService';

function ConnectorStatus() {
  const [status, setStatus] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await ApiService.getConnectorStatus();
        setStatus(response.data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };
    
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);
  
  // Render the component
  // ...
}

export default ConnectorStatus;
```

Then add the route in App.js:

```javascript
<Route path="/connector-status" element={<ConnectorStatus />} />
```

### Implementing a New Streaming Application

To implement a new streaming application:

1. Create a new file in `backend/src/` (e.g., `streaming_app3.py`)
2. Implement the Kafka consumer logic
3. Add specific processing logic
4. Add configuration
5. Add monitoring and metrics
6. Add documentation

Example:

```python
# backend/src/streaming_app3.py
import os
import json
import logging
from kafka import KafkaConsumer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AlertProcessor:
    def __init__(self):
        self.bootstrap_servers = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')
        self.topic = os.environ.get('KAFKA_TOPIC')
        self.consumer = self._create_consumer()
        self.messages_processed = 0
        
    def _create_consumer(self):
        try:
            consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=self.bootstrap_servers,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='alert-processor',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            logger.info(f"Connected to Kafka at {self.bootstrap_servers}")
            return consumer
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            raise
            
    def process_message(self, message):
        # Alert processing logic
        if 'alert' in message and message['alert']:
            logger.warning(f"Alert detected: {message['alert']}")
            # Send notification, trigger action, etc.
            
        self.messages_processed += 1
        
    def start(self):
        logger.info(f"Starting Alert Processor on topic {self.topic}")
        try:
            for message in self.consumer:
                self.process_message(message.value)
        except KeyboardInterrupt:
            logger.info("Shutting down Alert Processor")
        except Exception as e:
            logger.error(f"Error in Alert Processor: {e}")
        finally:
            self.consumer.close()
            
if __name__ == "__main__":
    processor = AlertProcessor()
    processor.start()
```

## Versioning and Releases

We follow Semantic Versioning (SemVer) for version numbers:

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality
- **PATCH** version for backwards-compatible bug fixes

### Release Process

1. Update the version number in relevant files
2. Update the CHANGELOG.md with the changes
3. Create a git tag for the version
   ```bash
   git tag -a v1.0.0 -m "Version 1.0.0"
   git push origin v1.0.0
   ```
4. Create a release in GitHub with release notes
5. Build and publish the release artifacts

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://reactjs.org/docs/getting-started.html)
- [AWS SQS Documentation](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
- [Kafka Documentation](https://kafka.apache.org/documentation/)
