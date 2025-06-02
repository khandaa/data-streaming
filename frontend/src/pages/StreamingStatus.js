import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Grid, 
  Card, 
  CardContent, 
  Typography, 
  Box, 
  Paper, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  CircularProgress,
  Alert
} from '@mui/material';
import ApiService from '../services/ApiService';

function StreamingStatus() {
  const [metrics, setMetrics] = useState({
    messages_processed: 0,
    processing_errors: 0,
    last_processing_time: null,
    kafka_send_errors: 0,
    stream_status: 'stopped'
  });
  const [healthStatus, setHealthStatus] = useState({
    status: 'unknown',
    sqs_connected: false,
    kafka_connected: false
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    // Initial fetch
    fetchData();

    // Set up polling
    const interval = setInterval(() => {
      fetchData();
    }, 3000); // Poll every 3 seconds

    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      // Fetch both metrics and health status
      const [metricsResponse, healthResponse] = await Promise.all([
        ApiService.getMetrics(),
        ApiService.healthCheck()
      ]);
      
      setMetrics(metricsResponse.data);
      setHealthStatus(healthResponse.data);
      setLastUpdated(new Date());
      setLoading(false);
      setError(null);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to fetch streaming status. Please try again later.');
      setLoading(false);
    }
  };

  const formatDateTime = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, textAlign: 'center' }}>
        <CircularProgress />
        <Typography variant="h6" sx={{ mt: 2 }}>Loading streaming status...</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Header */}
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom>
            Streaming Status
          </Typography>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Last updated: {lastUpdated ? lastUpdated.toLocaleString() : 'N/A'}
          </Typography>
        </Grid>

        {/* Connection Status */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Connection Status
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                  <Paper 
                    elevation={1} 
                    sx={{ 
                      p: 2, 
                      textAlign: 'center',
                      bgcolor: healthStatus.status === 'healthy' ? '#e8f5e9' : '#ffebee'
                    }}
                  >
                    <Typography variant="body2" color="text.secondary">
                      API Status
                    </Typography>
                    <Typography 
                      variant="h6" 
                      color={healthStatus.status === 'healthy' ? 'success.main' : 'error.main'}
                    >
                      {healthStatus.status === 'healthy' ? 'HEALTHY' : 'UNHEALTHY'}
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Paper 
                    elevation={1} 
                    sx={{ 
                      p: 2, 
                      textAlign: 'center',
                      bgcolor: healthStatus.sqs_connected ? '#e8f5e9' : '#ffebee'
                    }}
                  >
                    <Typography variant="body2" color="text.secondary">
                      SQS Connection
                    </Typography>
                    <Typography 
                      variant="h6" 
                      color={healthStatus.sqs_connected ? 'success.main' : 'error.main'}
                    >
                      {healthStatus.sqs_connected ? 'CONNECTED' : 'DISCONNECTED'}
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Paper 
                    elevation={1} 
                    sx={{ 
                      p: 2, 
                      textAlign: 'center',
                      bgcolor: healthStatus.kafka_connected ? '#e8f5e9' : '#ffebee'
                    }}
                  >
                    <Typography variant="body2" color="text.secondary">
                      Kafka Connection
                    </Typography>
                    <Typography 
                      variant="h6" 
                      color={healthStatus.kafka_connected ? 'success.main' : 'error.main'}
                    >
                      {healthStatus.kafka_connected ? 'CONNECTED' : 'DISCONNECTED'}
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Streaming Metrics */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Streaming Metrics
              </Typography>
              <TableContainer component={Paper}>
                <Table aria-label="streaming metrics table">
                  <TableHead>
                    <TableRow>
                      <TableCell><strong>Metric</strong></TableCell>
                      <TableCell><strong>Value</strong></TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    <TableRow>
                      <TableCell>Stream Status</TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <span 
                            className={`status-indicator ${
                              metrics.stream_status === 'running' 
                                ? 'status-running' 
                                : 'status-stopped'
                            }`}
                          ></span>
                          {metrics.stream_status === 'running' ? 'Running' : 'Stopped'}
                        </Box>
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Messages Processed</TableCell>
                      <TableCell>{metrics.messages_processed}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Processing Errors</TableCell>
                      <TableCell>{metrics.processing_errors}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Kafka Send Errors</TableCell>
                      <TableCell>{metrics.kafka_send_errors}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Last Processing Time</TableCell>
                      <TableCell>{formatDateTime(metrics.last_processing_time)}</TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* System Information */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Information
              </Typography>
              <Typography variant="body2" paragraph>
                This streaming application connects AWS SQS to Kafka across different subnets. 
                Data is processed in real-time and made available to multiple streaming applications.
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Network Configuration:</strong> The application uses VPC endpoints to 
                communicate with AWS SQS and Kafka across different subnets, ensuring secure and 
                reliable data transfer even across network boundaries.
              </Typography>
              <Typography variant="body2">
                <strong>For more details:</strong> Please check the Help page or contact your system administrator.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
}

export default StreamingStatus;
