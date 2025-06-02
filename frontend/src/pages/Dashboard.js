import React, { useState, useEffect } from 'react';
import { Container, Grid, Card, CardContent, Typography, Box, Button } from '@mui/material';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import ApiService from '../services/ApiService';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function Dashboard() {
  const [metrics, setMetrics] = useState({
    messages_processed: 0,
    processing_errors: 0,
    last_processing_time: null,
    stream_status: 'stopped'
  });
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Messages Processed',
        data: [],
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
      {
        label: 'Errors',
        data: [],
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
    ],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Initial fetch
    fetchMetrics();

    // Set up polling
    const interval = setInterval(() => {
      fetchMetrics();
    }, 5000); // Poll every 5 seconds

    return () => clearInterval(interval);
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await ApiService.getMetrics();
      setMetrics(response.data);
      updateChartData(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching metrics:', err);
      setError('Failed to fetch metrics. Please try again later.');
      setLoading(false);
    }
  };

  const updateChartData = (newMetrics) => {
    const now = new Date().toLocaleTimeString();
    
    setChartData(prevData => {
      // Keep only the last 10 data points
      const labels = [...prevData.labels, now].slice(-10);
      const messagesData = [...prevData.datasets[0].data, newMetrics.messages_processed].slice(-10);
      const errorsData = [...prevData.datasets[1].data, newMetrics.processing_errors].slice(-10);
      
      return {
        labels,
        datasets: [
          {
            ...prevData.datasets[0],
            data: messagesData,
          },
          {
            ...prevData.datasets[1],
            data: errorsData,
          },
        ],
      };
    });
  };

  const handleStartStream = async () => {
    try {
      await ApiService.startStream();
      fetchMetrics();
    } catch (err) {
      console.error('Error starting stream:', err);
      setError('Failed to start stream. Please try again later.');
    }
  };

  const handleStopStream = async () => {
    try {
      await ApiService.stopStream();
      fetchMetrics();
    } catch (err) {
      console.error('Error stopping stream:', err);
      setError('Failed to stop stream. Please try again later.');
    }
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4">Loading dashboard data...</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Header */}
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom>
            Data Streaming Dashboard
          </Typography>
          {error && (
            <Typography color="error" gutterBottom>
              {error}
            </Typography>
          )}
        </Grid>

        {/* Stream Status */}
        <Grid item xs={12} md={6}>
          <Card className="card-stats">
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Stream Status
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <span 
                  className={`status-indicator ${
                    metrics.stream_status === 'running' 
                      ? 'status-running' 
                      : 'status-stopped'
                  }`}
                ></span>
                <Typography variant="h5">
                  {metrics.stream_status === 'running' ? 'Running' : 'Stopped'}
                </Typography>
              </Box>
              <Box sx={{ mt: 2 }}>
                {metrics.stream_status === 'running' ? (
                  <Button 
                    variant="contained" 
                    color="error" 
                    onClick={handleStopStream}
                  >
                    Stop Stream
                  </Button>
                ) : (
                  <Button 
                    variant="contained" 
                    color="success" 
                    onClick={handleStartStream}
                  >
                    Start Stream
                  </Button>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Message Stats */}
        <Grid item xs={12} md={6}>
          <Card className="card-stats">
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Message Stats
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Messages Processed
                  </Typography>
                  <Typography variant="h5">
                    {metrics.messages_processed}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Processing Errors
                  </Typography>
                  <Typography variant="h5" color={metrics.processing_errors > 0 ? 'error' : 'inherit'}>
                    {metrics.processing_errors}
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="body2" color="text.secondary">
                    Last Processing Time
                  </Typography>
                  <Typography variant="body1">
                    {metrics.last_processing_time 
                      ? new Date(metrics.last_processing_time).toLocaleString() 
                      : 'N/A'}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Chart */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Message Processing Trends
              </Typography>
              <Box sx={{ height: 300 }}>
                <Line 
                  data={chartData} 
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                      y: {
                        beginAtZero: true,
                      },
                    },
                  }} 
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Dashboard;
