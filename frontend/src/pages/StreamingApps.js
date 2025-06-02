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
  Chip,
  CircularProgress,
  Alert,
  Divider
} from '@mui/material';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';
import ApiService from '../services/ApiService';

// This would be a real API call in a production app
const mockAppsData = [
  {
    id: 'app1',
    name: 'Analytics Processor',
    description: 'Processes data for analytics purposes',
    status: 'running',
    type: 'analytics',
    metrics: {
      messages_processed: 1248,
      processing_errors: 3,
      avg_processing_time_ms: 42.5,
      avg_message_size_bytes: 8192
    },
    lastUpdated: new Date().toISOString()
  },
  {
    id: 'app2',
    name: 'Real-time Data Processor',
    description: 'Processes data for real-time alerting',
    status: 'running',
    type: 'realtime',
    metrics: {
      messages_processed: 1325,
      alerts_triggered: 27,
      processing_errors: 5,
      processing_latency_ms: 63.8
    },
    lastUpdated: new Date().toISOString()
  }
];

function StreamingApps() {
  const [apps, setApps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // In a real app, you would fetch the data from the API
    // For now, we'll use mock data
    const fetchApps = async () => {
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        setApps(mockAppsData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching streaming apps:', err);
        setError('Failed to fetch streaming applications. Please try again later.');
        setLoading(false);
      }
    };

    fetchApps();
  }, []);

  const formatDateTime = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'running':
        return 'success';
      case 'stopped':
        return 'error';
      case 'warning':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getAppIcon = (type) => {
    switch (type) {
      case 'analytics':
        return <AnalyticsIcon />;
      case 'realtime':
        return <NotificationsActiveIcon />;
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, textAlign: 'center' }}>
        <CircularProgress />
        <Typography variant="h6" sx={{ mt: 2 }}>Loading streaming applications...</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Header */}
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom>
            Streaming Applications
          </Typography>
          <Typography variant="body1" gutterBottom>
            These applications consume data from Kafka and process it for different purposes.
          </Typography>
          {error && (
            <Alert severity="error" sx={{ mt: 2, mb: 2 }}>
              {error}
            </Alert>
          )}
        </Grid>

        {/* Apps Overview */}
        {apps.map((app) => (
          <Grid item xs={12} key={app.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ mr: 2 }}>
                    {getAppIcon(app.type)}
                  </Box>
                  <Typography variant="h6" component="div">
                    {app.name}
                  </Typography>
                  <Box sx={{ flexGrow: 1 }} />
                  <Chip 
                    label={app.status.toUpperCase()} 
                    color={getStatusColor(app.status)} 
                    size="small" 
                  />
                </Box>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {app.description}
                </Typography>
                <Divider sx={{ my: 2 }} />
                <Typography variant="subtitle2" gutterBottom>
                  Application Metrics
                </Typography>
                <TableContainer component={Paper} variant="outlined" sx={{ mb: 2 }}>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell><strong>Metric</strong></TableCell>
                        <TableCell align="right"><strong>Value</strong></TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {Object.entries(app.metrics).map(([key, value]) => (
                        <TableRow key={key}>
                          <TableCell component="th" scope="row">
                            {key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                          </TableCell>
                          <TableCell align="right">
                            {typeof value === 'number' && key.includes('time') || key.includes('latency') ? 
                              `${value.toFixed(2)} ms` : 
                              value.toLocaleString()}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
                <Typography variant="caption" color="text.secondary">
                  Last updated: {formatDateTime(app.lastUpdated)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}

        {/* Documentation */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                About Streaming Applications
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Analytics Processor:</strong> This application consumes data from Kafka and processes it for analytics purposes. 
                It calculates metrics such as message size, event counts, and processing times. The results can be used for business 
                intelligence and trend analysis.
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Real-time Data Processor:</strong> This application consumes data from Kafka for immediate processing and alerting. 
                It checks for certain conditions in the data stream and triggers alerts when those conditions are met. This is useful 
                for monitoring systems and responding to critical events in real-time.
              </Typography>
              <Typography variant="body2">
                Both applications share the same data stream from Kafka, but process it differently based on their specific purposes.
                This demonstrates how a single data stream can be used by multiple applications for different business needs.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
}

export default StreamingApps;
