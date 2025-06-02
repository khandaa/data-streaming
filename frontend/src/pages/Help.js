import React from 'react';
import { 
  Container, 
  Grid, 
  Card, 
  CardContent, 
  Typography, 
  Box,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ArrowRightIcon from '@mui/icons-material/ArrowRight';
import DataObjectIcon from '@mui/icons-material/DataObject';
import StorageIcon from '@mui/icons-material/Storage';
import SettingsIcon from '@mui/icons-material/Settings';
import ArchitectureIcon from '@mui/icons-material/Architecture';
import AccountTreeIcon from '@mui/icons-material/AccountTree';
import HelpIcon from '@mui/icons-material/Help';

function Help() {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Header */}
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom>
            Help & Documentation
          </Typography>
          <Typography variant="body1" paragraph>
            This guide provides information about the AWS SQS to Kafka Data Streaming Application, 
            including its architecture, components, and operation.
          </Typography>
        </Grid>

        {/* Project Overview */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Project Overview
              </Typography>
              <Typography variant="body1" paragraph>
                This distributed data streaming application facilitates the seamless transfer of data 
                from AWS SQS to Kafka across different network subnets. The system consists of connectors, 
                stream processors, and consumer applications that work together to enable real-time 
                data processing and analytics.
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>Key Features:</strong>
              </Typography>
              <List>
                <ListItem>
                  <ListItemIcon>
                    <ArrowRightIcon />
                  </ListItemIcon>
                  <ListItemText primary="Cross-subnet data streaming from AWS SQS to Kafka" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <ArrowRightIcon />
                  </ListItemIcon>
                  <ListItemText primary="Two independent streaming consumer applications for data sharing" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <ArrowRightIcon />
                  </ListItemIcon>
                  <ListItemText primary="Real-time monitoring and management dashboard" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <ArrowRightIcon />
                  </ListItemIcon>
                  <ListItemText primary="Comprehensive metrics and health status tracking" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <ArrowRightIcon />
                  </ListItemIcon>
                  <ListItemText primary="Admin control panel for configuration and system management" />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Architecture Diagram */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <ArchitectureIcon sx={{ mr: 1 }} />
                System Architecture
              </Typography>
              <Typography variant="body1" paragraph>
                The application follows a distributed architecture with the following components:
              </Typography>
              
              {/* ASCII Art Architecture Diagram */}
              <Box 
                sx={{ 
                  p: 2, 
                  backgroundColor: '#f5f5f5', 
                  borderRadius: 1,
                  fontFamily: 'monospace',
                  fontSize: '0.875rem',
                  whiteSpace: 'pre',
                  overflow: 'auto'
                }}
              >
{`+-------------------+      +------------------+      +-------------------+
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
                     +-------------+         +-------------+        +-------------+`}
              </Box>
              
              <Typography variant="body1" sx={{ mt: 3 }} paragraph>
                <strong>Component Description:</strong>
              </Typography>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>AWS SQS Queue (Subnet A)</strong></Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    The source of streaming data located in Subnet A. The application uses AWS SQS 
                    connector with VPC endpoint support to consume messages from this queue.
                  </Typography>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>Stream Processor</strong></Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    The core component that retrieves messages from SQS, processes them, and forwards 
                    them to Kafka. It runs in background threads and tracks metrics for performance 
                    and error handling.
                  </Typography>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>Kafka Cluster (Subnet B)</strong></Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    The destination for processed data, located in Subnet B. Messages from SQS are 
                    published to Kafka topics for consumption by streaming applications.
                  </Typography>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>Backend Flask API</strong></Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    RESTful API that provides endpoints for starting/stopping the stream, retrieving 
                    metrics, managing Kafka topics, and handling administrative functions.
                  </Typography>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>Frontend Dashboard</strong></Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    React-based user interface for monitoring and managing the streaming process. 
                    Provides visualizations of metrics, health status, and control functions.
                  </Typography>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>Streaming Applications</strong></Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    Two separate applications consume data from Kafka:
                    <ul>
                      <li><strong>Analytics Processor:</strong> Processes data for analytics purposes, calculates metrics and statistics.</li>
                      <li><strong>Real-time Processor:</strong> Processes data for immediate alerting and real-time decision making.</li>
                    </ul>
                  </Typography>
                </AccordionDetails>
              </Accordion>
            </CardContent>
          </Card>
        </Grid>

        {/* Data Flow Diagram */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <AccountTreeIcon sx={{ mr: 1 }} />
                Data Flow Diagram
              </Typography>
              <Typography variant="body1" paragraph>
                The following diagram illustrates the flow of data through the system:
              </Typography>
              
              {/* ASCII Art Flow Diagram */}
              <Box 
                sx={{ 
                  p: 2, 
                  backgroundColor: '#f5f5f5', 
                  borderRadius: 1,
                  fontFamily: 'monospace',
                  fontSize: '0.875rem',
                  whiteSpace: 'pre',
                  overflow: 'auto'
                }}
              >
{`   +--------+
   | Start  |
   +---+----+
       |
       v
+------+-------+     +-----------------+     +----------------+
|  AWS SQS     +---->+ SQSConnector    +---->+ StreamProcessor|
|  Queue       |     | receive_message |     |                |
+------+-------+     +-----------------+     +-------+--------+
                                                     |
                                                     v
+----------------+     +----------------+     +------+---------+
| Streaming App1 |<----+ KafkaConsumer  |<----+ KafkaConnector |
| (Analytics)    |     |                |     | produce_message|
+----------------+     +----------------+     +----------------+
                             ^
                             |
+----------------+           |
| Streaming App2 |<----------+
| (Real-time)    |
+----------------+

       ^                    ^                      ^
       |                    |                      |
       |                    |                      |
+------+--------------------+----------------------+-------+
|                                                          |
|                       Flask REST API                     |
|                                                          |
+----------------------------+-----------------------------+
                             ^
                             |
                             |
                      +------+------+
                      |  React      |
                      |  Frontend   |
                      |  Dashboard  |
                      +-------------+`}
              </Box>
              
              <Typography variant="body1" sx={{ mt: 3 }} paragraph>
                <strong>Data Flow Steps:</strong>
              </Typography>
              <List>
                <ListItem>
                  <ListItemIcon>
                    <DataObjectIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="1. Messages are retrieved from AWS SQS via the SQS connector" 
                    secondary="The connector handles authentication, retrieval, and deletion of messages from the queue"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <DataObjectIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="2. Stream Processor handles the messages" 
                    secondary="Messages are processed, validated, and prepared for Kafka publishing"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <DataObjectIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="3. Kafka Connector publishes messages to Kafka" 
                    secondary="Messages are sent to the configured Kafka topic"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <DataObjectIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="4. Streaming Applications consume from Kafka" 
                    secondary="Two separate applications consume and process the data for different purposes"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <DataObjectIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="5. Flask API provides management and monitoring" 
                    secondary="RESTful endpoints for controlling the stream and accessing metrics"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <DataObjectIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="6. React Frontend displays status and controls" 
                    secondary="User interface for monitoring and managing the entire system"
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Configuration */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <SettingsIcon sx={{ mr: 1 }} />
                Configuration Guide
              </Typography>
              <Typography variant="body1" paragraph>
                The application requires configuration for AWS SQS, Kafka, and application settings. 
                These can be set through environment variables or the admin interface.
              </Typography>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>AWS Configuration</strong></Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    Required AWS settings:
                    <ul>
                      <li><strong>AWS_ACCESS_KEY_ID:</strong> AWS access key with SQS permissions</li>
                      <li><strong>AWS_SECRET_ACCESS_KEY:</strong> AWS secret key</li>
                      <li><strong>AWS_REGION:</strong> AWS region where the SQS queue is located</li>
                      <li><strong>SQS_QUEUE_URL:</strong> The URL of the SQS queue to consume from</li>
                      <li><strong>SQS_SUBNET_ID:</strong> The subnet ID where SQS is located</li>
                      <li><strong>VPC_ID:</strong> The VPC ID for cross-subnet communication</li>
                    </ul>
                  </Typography>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>Kafka Configuration</strong></Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    Required Kafka settings:
                    <ul>
                      <li><strong>KAFKA_BOOTSTRAP_SERVERS:</strong> Comma-separated list of Kafka brokers</li>
                      <li><strong>KAFKA_TOPIC:</strong> The topic to publish messages to</li>
                      <li><strong>KAFKA_SECURITY_PROTOCOL:</strong> Security protocol (PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL)</li>
                      <li><strong>KAFKA_SASL_MECHANISM:</strong> SASL mechanism if using SASL</li>
                      <li><strong>KAFKA_SASL_USERNAME:</strong> SASL username if using SASL</li>
                      <li><strong>KAFKA_SASL_PASSWORD:</strong> SASL password if using SASL</li>
                      <li><strong>KAFKA_SUBNET_ID:</strong> The subnet ID where Kafka is located</li>
                    </ul>
                  </Typography>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>Application Configuration</strong></Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    Application settings:
                    <ul>
                      <li><strong>APP_HOST:</strong> Host for the Flask application (default: 0.0.0.0)</li>
                      <li><strong>APP_PORT:</strong> Port for the Flask application (default: 5000)</li>
                      <li><strong>DEBUG:</strong> Enable debug mode (true/false)</li>
                      <li><strong>LOG_LEVEL:</strong> Logging level (DEBUG, INFO, WARNING, ERROR)</li>
                      <li><strong>ADMIN_USERNAME:</strong> Username for admin login (default: admin)</li>
                      <li><strong>ADMIN_PASSWORD:</strong> Password for admin login (default: admin)</li>
                    </ul>
                  </Typography>
                </AccordionDetails>
              </Accordion>
            </CardContent>
          </Card>
        </Grid>

        {/* FAQs */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <HelpIcon sx={{ mr: 1 }} />
                Frequently Asked Questions
              </Typography>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>How does the cross-subnet communication work?</strong></Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    The application uses AWS VPC endpoints to establish secure communication between different subnets. 
                    This allows the SQS connector to communicate with SQS in one subnet, and the Kafka connector to 
                    communicate with Kafka in another subnet.
                  </Typography>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>What happens if the SQS connection fails?</strong></Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    The SQS connector includes error handling and retry logic. If the connection fails, it will 
                    attempt to reconnect automatically with exponential backoff. The failure will be logged and 
                    metrics will be updated to reflect the error.
                  </Typography>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>How can I monitor the system's performance?</strong></Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    The dashboard provides real-time metrics including messages processed, processing errors, 
                    and processing time. For more detailed monitoring, you can use the Admin Dashboard which 
                    provides system logs and more comprehensive metrics.
                  </Typography>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>Can I add more streaming applications?</strong></Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    Yes, you can add additional streaming applications that consume from the same Kafka topic. 
                    Each application can process the data differently based on its specific requirements. You 
                    would need to implement the application logic and register it with the system.
                  </Typography>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>How do I secure the application?</strong></Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    The application supports several security measures:
                    <ul>
                      <li>Admin authentication for the dashboard</li>
                      <li>HTTPS for the web interface</li>
                      <li>AWS IAM roles for SQS access</li>
                      <li>Kafka SASL/SSL for secure Kafka communication</li>
                      <li>Environment variables for sensitive configuration</li>
                    </ul>
                    It's recommended to use all these security features in production.
                  </Typography>
                </AccordionDetails>
              </Accordion>
            </CardContent>
          </Card>
        </Grid>

        {/* Support */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Support & Contact
              </Typography>
              <Typography variant="body1" paragraph>
                For additional support or questions about this application, please contact the system administrator 
                or refer to the project documentation.
              </Typography>
              <Typography variant="body2" color="text.secondary">
                This application was developed by the EmployDEX team.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Help;
