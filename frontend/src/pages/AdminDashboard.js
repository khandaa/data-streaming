import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Grid, 
  Card, 
  CardContent, 
  Typography, 
  Box,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
  Alert,
  Divider,
  Switch,
  FormControlLabel
} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import StopIcon from '@mui/icons-material/Stop';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import SettingsIcon from '@mui/icons-material/Settings';
import ApiService from '../services/ApiService';

function AdminDashboard() {
  const [config, setConfig] = useState({
    aws: {
      region: 'us-east-1',
      sqs_queue_url: 'https://sqs.us-east-1.amazonaws.com/123456789012/data-stream-queue',
      sqs_subnet_id: 'subnet-12345',
      vpc_id: 'vpc-12345'
    },
    kafka: {
      bootstrap_servers: 'kafka:9092',
      topic: 'sqs-data',
      subnet_id: 'subnet-67890'
    },
    app: {
      debug_mode: false,
      log_level: 'INFO'
    }
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [activeTab, setActiveTab] = useState('system');
  const [logs, setLogs] = useState([
    { timestamp: '2025-06-02T10:20:45', level: 'INFO', message: 'Application started' },
    { timestamp: '2025-06-02T10:21:13', level: 'INFO', message: 'Connected to AWS SQS' },
    { timestamp: '2025-06-02T10:21:15', level: 'INFO', message: 'Connected to Kafka' },
    { timestamp: '2025-06-02T10:25:30', level: 'INFO', message: 'Stream processing started' },
    { timestamp: '2025-06-02T10:30:12', level: 'WARNING', message: 'Slow message processing detected' },
    { timestamp: '2025-06-02T10:32:45', level: 'ERROR', message: 'Failed to connect to SQS: Network timeout' },
    { timestamp: '2025-06-02T10:35:10', level: 'INFO', message: 'Reconnected to AWS SQS' },
    { timestamp: '2025-06-02T10:40:23', level: 'INFO', message: 'Processed 1000 messages' }
  ]);

  useEffect(() => {
    // Simulating API call to get configuration
    const fetchConfig = async () => {
      try {
        // In a real app, this would be an API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        setLoading(false);
      } catch (err) {
        console.error('Error fetching configuration:', err);
        setError('Failed to fetch configuration. Please try again later.');
        setLoading(false);
      }
    };

    fetchConfig();
  }, []);

  const handleConfigChange = (section, field, value) => {
    setConfig({
      ...config,
      [section]: {
        ...config[section],
        [field]: value
      }
    });
    setSaveSuccess(false);
  };

  const handleSaveConfig = async () => {
    try {
      setLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      setSaveSuccess(true);
      setLoading(false);
    } catch (err) {
      console.error('Error saving configuration:', err);
      setError('Failed to save configuration. Please try again later.');
      setLoading(false);
    }
  };

  const handleRestartService = async () => {
    try {
      setLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      setLoading(false);
    } catch (err) {
      console.error('Error restarting service:', err);
      setError('Failed to restart service. Please try again later.');
      setLoading(false);
    }
  };

  const formatLogLevel = (level) => {
    switch (level) {
      case 'ERROR':
        return <Typography color="error" fontWeight="bold">{level}</Typography>;
      case 'WARNING':
        return <Typography color="warning.main" fontWeight="bold">{level}</Typography>;
      case 'INFO':
        return <Typography color="info.main">{level}</Typography>;
      default:
        return <Typography>{level}</Typography>;
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  const renderConfigSection = () => (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            AWS Configuration
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="AWS Region"
                value={config.aws.region}
                onChange={(e) => handleConfigChange('aws', 'region', e.target.value)}
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="SQS Queue URL"
                value={config.aws.sqs_queue_url}
                onChange={(e) => handleConfigChange('aws', 'sqs_queue_url', e.target.value)}
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="SQS Subnet ID"
                value={config.aws.sqs_subnet_id}
                onChange={(e) => handleConfigChange('aws', 'sqs_subnet_id', e.target.value)}
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="VPC ID"
                value={config.aws.vpc_id}
                onChange={(e) => handleConfigChange('aws', 'vpc_id', e.target.value)}
                margin="normal"
              />
            </Grid>
          </Grid>

          <Divider sx={{ my: 3 }} />

          <Typography variant="h6" gutterBottom>
            Kafka Configuration
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Bootstrap Servers"
                value={config.kafka.bootstrap_servers}
                onChange={(e) => handleConfigChange('kafka', 'bootstrap_servers', e.target.value)}
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Default Topic"
                value={config.kafka.topic}
                onChange={(e) => handleConfigChange('kafka', 'topic', e.target.value)}
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Kafka Subnet ID"
                value={config.kafka.subnet_id}
                onChange={(e) => handleConfigChange('kafka', 'subnet_id', e.target.value)}
                margin="normal"
              />
            </Grid>
          </Grid>

          <Divider sx={{ my: 3 }} />

          <Typography variant="h6" gutterBottom>
            Application Settings
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth margin="normal">
                <InputLabel id="log-level-label">Log Level</InputLabel>
                <Select
                  labelId="log-level-label"
                  value={config.app.log_level}
                  onChange={(e) => handleConfigChange('app', 'log_level', e.target.value)}
                  label="Log Level"
                >
                  <MenuItem value="DEBUG">DEBUG</MenuItem>
                  <MenuItem value="INFO">INFO</MenuItem>
                  <MenuItem value="WARNING">WARNING</MenuItem>
                  <MenuItem value="ERROR">ERROR</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControlLabel
                control={
                  <Switch
                    checked={config.app.debug_mode}
                    onChange={(e) => handleConfigChange('app', 'debug_mode', e.target.checked)}
                  />
                }
                label="Debug Mode"
                sx={{ mt: 2 }}
              />
            </Grid>
          </Grid>

          <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleSaveConfig}
              disabled={loading}
            >
              Save Configuration
            </Button>
          </Box>
        </Paper>
      </Grid>
    </Grid>
  );

  const renderSystemControls = () => (
    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              System Controls
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
              <Button
                variant="contained"
                color="success"
                startIcon={<PlayArrowIcon />}
                onClick={() => ApiService.startStream()}
              >
                Start Stream Processing
              </Button>
              <Button
                variant="contained"
                color="error"
                startIcon={<StopIcon />}
                onClick={() => ApiService.stopStream()}
              >
                Stop Stream Processing
              </Button>
              <Button
                variant="contained"
                color="warning"
                startIcon={<RestartAltIcon />}
                onClick={handleRestartService}
              >
                Restart Service
              </Button>
              <Button
                variant="outlined"
                startIcon={<SettingsIcon />}
                onClick={() => setActiveTab('config')}
              >
                Configure Settings
              </Button>
            </Box>
          </CardContent>
        </Card>
      </Grid>

      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              System Status
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableBody>
                  <TableRow>
                    <TableCell component="th" scope="row">
                      <strong>Application Status</strong>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label="Running" 
                        color="success" 
                        size="small" 
                      />
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell component="th" scope="row">
                      <strong>SQS Connection</strong>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label="Connected" 
                        color="success" 
                        size="small" 
                      />
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell component="th" scope="row">
                      <strong>Kafka Connection</strong>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label="Connected" 
                        color="success" 
                        size="small" 
                      />
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell component="th" scope="row">
                      <strong>Stream Processing</strong>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label="Active" 
                        color="success" 
                        size="small" 
                      />
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell component="th" scope="row">
                      <strong>Memory Usage</strong>
                    </TableCell>
                    <TableCell>478 MB</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell component="th" scope="row">
                      <strong>CPU Usage</strong>
                    </TableCell>
                    <TableCell>12%</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      </Grid>

      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              System Logs
            </Typography>
            <TableContainer sx={{ maxHeight: 400 }}>
              <Table stickyHeader size="small">
                <TableHead>
                  <TableRow>
                    <TableCell width="25%"><strong>Timestamp</strong></TableCell>
                    <TableCell width="15%"><strong>Level</strong></TableCell>
                    <TableCell><strong>Message</strong></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {logs.map((log, index) => (
                    <TableRow key={index}>
                      <TableCell>{formatTimestamp(log.timestamp)}</TableCell>
                      <TableCell>{formatLogLevel(log.level)}</TableCell>
                      <TableCell>{log.message}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );

  if (loading && !config) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, textAlign: 'center' }}>
        <CircularProgress />
        <Typography variant="h6" sx={{ mt: 2 }}>
          Loading admin dashboard...
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Header */}
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h4" gutterBottom>
              Admin Dashboard
            </Typography>
            <Box>
              <Button
                variant={activeTab === 'system' ? 'contained' : 'outlined'}
                onClick={() => setActiveTab('system')}
                sx={{ mr: 1 }}
              >
                System Controls
              </Button>
              <Button
                variant={activeTab === 'config' ? 'contained' : 'outlined'}
                onClick={() => setActiveTab('config')}
              >
                Configuration
              </Button>
            </Box>
          </Box>
          
          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}
          
          {saveSuccess && (
            <Alert severity="success" sx={{ mb: 3 }}>
              Configuration saved successfully!
            </Alert>
          )}
        </Grid>

        {/* Main Content */}
        {activeTab === 'system' ? renderSystemControls() : renderConfigSection()}
      </Grid>
    </Container>
  );
}

export default AdminDashboard;
