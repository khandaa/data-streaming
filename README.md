# AWS SQS to Kafka Streaming Application

## Overview

A distributed data streaming application that enables seamless data transfer from AWS SQS queues to Kafka topics across different network subnets. The application includes connectors, stream processors, consumer applications, and a comprehensive monitoring dashboard to enable real-time data processing and analytics.

## Key Features

- **Cross-subnet Data Streaming**: Stream data between AWS SQS and Kafka in different network subnets
- **Real-time Monitoring**: Track streaming metrics, connection status, and system health
- **Kafka Topic Management**: Create and manage Kafka topics through a user-friendly interface
- **Streaming Applications**: Two consumer applications for analytics and real-time processing
- **Admin Controls**: Comprehensive admin dashboard for configuration and system management
- **Secure Authentication**: Role-based access control for administrative functions
- **Responsive UI**: Modern interface built with React, Material UI, and Bootstrap

## Architecture

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

## Technology Stack

### Backend
- **Language**: Python 3.8+
- **Framework**: Flask
- **AWS SDK**: boto3
- **Kafka Libraries**: confluent-kafka, kafka-python

### Frontend
- **Framework**: React
- **UI Libraries**: Material UI, Bootstrap
- **Data Visualization**: Chart.js, React Chartjs 2
- **HTTP Client**: Axios

## Project Structure

```
data_streaming/
├── backend/                # Flask backend application
│   ├── src/
│   │   ├── app.py          # Main application entry point
│   │   ├── connectors/     # SQS and Kafka connector modules
│   │   ├── config/         # Configuration management
│   │   ├── utils/          # Stream processor and utilities
│   │   └── streaming_app*  # Streaming applications
│   └── tests/              # Backend test files
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/     # Reusable React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service modules
│   │   └── styles/         # CSS and styling
│   └── public/             # Static assets
├── database/               # Database files and schemas
├── docs/                   # Comprehensive documentation
│   ├── overview.md         # Project overview
│   ├── installation.md     # Installation guide
│   ├── user_guide.md       # End-user documentation
│   ├── admin_guide.md      # Administrator guide
│   ├── api_reference.md    # API documentation
│   ├── architecture.md     # Technical architecture
│   └── development_guide.md# Guide for developers
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore file
├── CHANGELOG.md            # Version history
└── README.md               # Project overview
```

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm 6+
- Git
- AWS account with SQS access
- Kafka cluster access

### Quick Setup (Local Development)

1. Clone this repository
2. Set up the backend environment:
   ```bash
   # Create and activate virtual environment
   python -m venv ../venv
   source ../venv/bin/activate  # On Windows: ..\venv\Scripts\activate
   
   # Install dependencies
   cd backend
   pip install -r requirements.txt
   ```

3. Set up the frontend environment:
   ```bash
   cd ../frontend
   npm install
   ```

4. Configure environment variables:
   ```bash
   # Copy the example environment file
   cp env.example.txt .env
   
   # Edit with your actual settings
   nano .env
   ```

5. Start the backend:
   ```bash
   cd backend
   source ../venv/bin/activate
   python src/app.py
   ```

6. Start the frontend (in a separate terminal):
   ```bash
   cd frontend
   npm start
   ```

7. Start the streaming applications (in separate terminals):
   ```bash
   # Analytics Processor
   cd backend
   source ../venv/bin/activate
   python src/streaming_app1.py
   
   # Real-time Data Processor
   cd backend
   source ../venv/bin/activate
   python src/streaming_app2.py
   ```

### Docker Deployment

1. Clone this repository

2. Configure environment variables:
   ```bash
   # Copy the example Docker environment file
   cp backend/.env.docker.example backend/.env.docker
   
   # Edit with your actual settings
   nano backend/.env.docker
   ```

3. Build and start the containers:
   ```bash
   # Build and start all services
   docker compose up -d
   ```

4. Verify all services are running:
   ```bash
   docker ps
   ```

5. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Kafka UI: http://localhost:8080

6. Stop the application:
   ```bash
   docker compose down
   ```

7. For development with live changes:
   ```bash
   # Uncomment the volumes section in docker-compose.yml for the backend service
   # Then rebuild and restart
   docker compose up -d --build
   ```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- [Project Overview](docs/overview.md) - Introduction and system architecture
- [Installation Guide](docs/installation.md) - Detailed setup instructions
- [User Guide](docs/user_guide.md) - End-user documentation
- [Admin Guide](docs/admin_guide.md) - Administrator documentation
- [API Reference](docs/api_reference.md) - Backend API documentation
- [Technical Architecture](docs/architecture.md) - Detailed technical design
- [Development Guide](docs/development_guide.md) - Guide for developers

## Default Admin Credentials

- **Username**: admin
- **Password**: admin

**IMPORTANT**: Change these credentials immediately after first login by going to the Admin Dashboard > Security tab.

## Version History

See the [CHANGELOG.md](CHANGELOG.md) for a detailed version history.

## License

MIT
