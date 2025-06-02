# User Guide

This guide provides detailed instructions for using the AWS SQS to Kafka Streaming Application.

## Table of Contents

- [Dashboard Overview](#dashboard-overview)
- [Streaming Status](#streaming-status)
- [Kafka Topics](#kafka-topics)
- [Streaming Applications](#streaming-applications)
- [Help and Support](#help-and-support)

## Dashboard Overview

The application dashboard provides a comprehensive view of your data streaming system, with easy navigation to all features through the sidebar menu.

### Navigation

- **Sidebar**: Access all pages from the expandable sidebar on the left
- **Navbar**: Contains user information, logout button, and sidebar toggle
- **Main Content**: Displays the selected page content

### Home Dashboard

The home dashboard displays:

- **Overview Cards**: Quick statistics on messages processed, error rate, and system health
- **Performance Graphs**: Visual representation of message throughput and system metrics
- **Status Indicators**: Health status of all system components (SQS, Kafka, Processors)

## Streaming Status

The Streaming Status page provides real-time information about the data flow from AWS SQS to Kafka.

### Key Features

- **Connection Status**: Visual indicators for SQS and Kafka connections
- **Stream Metrics**: Real-time statistics including:
  - Messages processed per second
  - Total messages processed
  - Error rate
  - Processing latency
- **Historical Data**: Charts showing performance over time
- **System Information**: Details about the running environment and configuration

### Interpreting Status Indicators

| Indicator | Color | Meaning |
|-----------|-------|---------|
| Green     | 🟢    | Healthy, functioning normally |
| Yellow    | 🟡    | Warning, potential issues |
| Red       | 🔴    | Error, requires attention |

The status indicators pulse when active, indicating live data flow.

## Kafka Topics

The Topics page allows you to view and manage Kafka topics used by the streaming application.

### Viewing Topics

The Topics page displays a list of all available Kafka topics with details including:

- Topic name
- Number of partitions
- Replication factor
- Configuration settings
- Creation date

### Creating a New Topic

To create a new Kafka topic:

1. Click the **+ New Topic** button in the upper right corner
2. In the dialog form, enter:
   - **Topic Name**: Alphanumeric characters and hyphens (example: `my-new-topic`)
   - **Partitions**: Number of partitions (1-100)
   - **Replication Factor**: Typically 2 or 3 for production
   - **Advanced Configurations**: Optional settings for retention, cleanup policy, etc.
3. Click **Create Topic**

**Note**: Topic names must be unique and follow Kafka naming conventions.

### Topic Validation Rules

- Topic names must be 1-249 characters
- Can only contain alphanumeric characters, periods (`.`), underscores (`_`), and hyphens (`-`)
- Cannot be only periods (`.`) or (`..`)
- Should not begin with a period (`.`) or underscore (`_`)

## Streaming Applications

The Streaming Apps page provides monitoring and information about the consumer applications processing data from Kafka.

### Available Applications

#### 1. Analytics Processor

The Analytics Processor consumes messages for batch processing and analytics purposes.

**Metrics displayed**:
- Total messages processed
- Processing rate
- Batch size
- CPU and memory utilization
- Error rate
- Last processed timestamp

#### 2. Real-time Data Processor

The Real-time Data Processor consumes messages for immediate alerting and real-time dashboards.

**Metrics displayed**:
- Total messages processed
- Processing latency
- Events triggered
- Error rate
- CPU and memory utilization
- Last processed timestamp

### Application Cards

Each application is displayed as a card with:

- Status indicator (running/stopped)
- Key metrics
- Description of purpose
- Quick action buttons

## Help and Support

The Help page provides comprehensive information about the application.

### Available Resources

- **Architecture Overview**: Diagrams showing system components and data flow
- **Configuration Guide**: Instructions for setting up environment variables
- **Troubleshooting**: Common issues and solutions
- **FAQs**: Answers to frequently asked questions

### ASCII Architecture Diagram

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

### ASCII Data Flow Diagram

```
+-----------+     +-----------+     +-----------+     +-----------+     +-----------+
|           |     |           |     |           |     |           |     |           |
|  Message  +---->+    SQS    +---->+  Stream   +---->+   Kafka   +---->+ Consumer  |
| Producer  |     |   Queue   |     | Processor |     |   Topic   |     |   Apps    |
|           |     |           |     |           |     |           |     |           |
+-----------+     +-----------+     +-----------+     +-----------+     +-----------+
                                         |
                                         v
                                    +-----------+
                                    |           |
                                    |  Metrics  |
                                    |           |
                                    +-----------+
                                         |
                                         v
                  +-----------+     +-----------+     +-----------+
                  |           |     |           |     |           |
                  | Frontend  |<--->+  Backend  |<--->+   Admin   |
                  | Dashboard |     |    API    |     | Controls  |
                  |           |     |           |     |           |
                  +-----------+     +-----------+     +-----------+
```

### Getting Support

If you encounter issues not covered in the documentation:

1. Check the logs in the Admin Dashboard
2. Refer to the Troubleshooting section in the Help page
3. Contact the system administrator at admin@example.com

## Keyboard Shortcuts

The application supports the following keyboard shortcuts:

| Shortcut | Action |
|----------|--------|
| `Alt+S`  | Go to Streaming Status page |
| `Alt+T`  | Go to Topics page |
| `Alt+A`  | Go to Streaming Apps page |
| `Alt+H`  | Go to Help page |
| `Alt+D`  | Go to Admin Dashboard (if logged in) |
| `Alt+M`  | Toggle sidebar menu |
| `Alt+R`  | Refresh current page data |
| `Alt+L`  | Go to Login page (if not logged in) |
