# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-06-03

### Added
- Complete Docker containerization of the application
- Docker Compose setup with Kafka, Zookeeper, Kafka UI, Backend, and Frontend services
- Environment file templates for Docker deployment
- Docker deployment documentation in README

### Fixed
- SQS Simulator receipt handle parsing bug with queue names containing hyphens
- Import path issues in backend Python files
- Werkzeug compatibility issue with Flask 2.2.3
- Missing frontend public files for React build

### Changed
- Updated docker-compose.yml with production-ready configurations
- Improved security in Docker setup with proper user permissions
- Added healthchecks for all containerized services

## [1.0.0] - 2025-06-02

### Added
- Initial project setup with React frontend and Flask backend
- AWS SQS connector with cross-subnet VPC endpoint support
- Kafka connector for publishing messages to topics
- Stream processor for handling data flow from SQS to Kafka
- RESTful API endpoints for stream control, metrics, and management
- Two streaming applications for consuming Kafka data:
  - Analytics Processor for batch processing and analysis
  - Real-time Data Processor for immediate alerting
- Frontend dashboard with:
  - Stream status monitoring
  - Kafka topic management
  - Streaming application status viewing
  - Admin dashboard for configuration and system controls
  - Help page with architecture and flow diagrams
- Comprehensive error handling and metrics collection
- Environment configuration via .env files
- Test scaffolding for TDD approach

### Technical Details
- Backend: Python/Flask, boto3, kafka-python, confluent-kafka
- Frontend: React, Material UI, Bootstrap, Chart.js
- Cross-subnet communication using AWS VPC endpoints
- Responsive design for desktop and mobile viewing
- Authentication for admin access
