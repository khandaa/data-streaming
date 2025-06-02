import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Grid, 
  Card, 
  CardContent, 
  Typography, 
  Button,
  TextField,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Paper,
  CircularProgress,
  Alert,
  Divider
} from '@mui/material';
import TopicIcon from '@mui/icons-material/Topic';
import AddIcon from '@mui/icons-material/Add';
import ApiService from '../services/ApiService';

function Topics() {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [newTopic, setNewTopic] = useState({
    name: '',
    partitions: 3,
    replication: 3
  });
  const [formError, setFormError] = useState('');

  useEffect(() => {
    fetchTopics();
  }, []);

  const fetchTopics = async () => {
    try {
      setLoading(true);
      const response = await ApiService.getTopics();
      setTopics(response.data.topics || []);
      setError(null);
    } catch (err) {
      console.error('Error fetching topics:', err);
      setError('Failed to fetch Kafka topics. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = () => {
    setOpenDialog(true);
    setFormError('');
    setNewTopic({
      name: '',
      partitions: 3,
      replication: 3
    });
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewTopic({
      ...newTopic,
      [name]: name === 'name' ? value : parseInt(value, 10)
    });
  };

  const validateForm = () => {
    if (!newTopic.name) {
      setFormError('Topic name is required');
      return false;
    }
    
    if (!/^[a-zA-Z0-9._-]+$/.test(newTopic.name)) {
      setFormError('Topic name can only contain letters, numbers, dots, underscores, and hyphens');
      return false;
    }
    
    if (newTopic.partitions < 1) {
      setFormError('Number of partitions must be at least 1');
      return false;
    }
    
    if (newTopic.replication < 1) {
      setFormError('Replication factor must be at least 1');
      return false;
    }
    
    return true;
  };

  const handleCreateTopic = async () => {
    if (!validateForm()) {
      return;
    }
    
    try {
      await ApiService.createTopic(newTopic);
      handleCloseDialog();
      fetchTopics();
    } catch (err) {
      console.error('Error creating topic:', err);
      setFormError(err.response?.data?.error || 'Failed to create topic. Please try again.');
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Header */}
        <Grid item xs={12} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h4" gutterBottom>
            Kafka Topics
          </Typography>
          <Button 
            variant="contained" 
            color="primary" 
            startIcon={<AddIcon />}
            onClick={handleOpenDialog}
          >
            Create Topic
          </Button>
        </Grid>

        {error && (
          <Grid item xs={12}>
            <Alert severity="error">{error}</Alert>
          </Grid>
        )}

        {/* Topics List */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Available Topics
              </Typography>
              
              {loading ? (
                <div style={{ textAlign: 'center', padding: '20px' }}>
                  <CircularProgress />
                  <Typography variant="body2" sx={{ mt: 2 }}>
                    Loading topics...
                  </Typography>
                </div>
              ) : topics.length === 0 ? (
                <Paper sx={{ p: 3, textAlign: 'center' }}>
                  <Typography variant="body1" color="text.secondary">
                    No Kafka topics found.
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    Click "Create Topic" to add a new Kafka topic.
                  </Typography>
                </Paper>
              ) : (
                <List component="nav" aria-label="kafka topics">
                  {topics.map((topic, index) => (
                    <React.Fragment key={topic}>
                      <ListItem>
                        <ListItemIcon>
                          <TopicIcon />
                        </ListItemIcon>
                        <ListItemText 
                          primary={topic} 
                          secondary="Click to view topic details (coming soon)"
                        />
                      </ListItem>
                      {index < topics.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Topic Information */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Topic Information
              </Typography>
              <Typography variant="body2" paragraph>
                Kafka topics are a category or feed name to which records are published. 
                Topics in Kafka are always multi-subscriber; that is, a topic can have 
                zero, one, or many consumers that subscribe to the data written to it.
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Partitions:</strong> Each topic is split into partitions, which enables 
                Kafka to handle and process the data in parallel. More partitions allow greater 
                parallelism for consumption but require more files.
              </Typography>
              <Typography variant="body2">
                <strong>Replication Factor:</strong> Represents how many copies of the data will 
                be stored across the Kafka cluster. Higher replication increases fault tolerance 
                but requires more storage.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Create Topic Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>Create New Kafka Topic</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Enter the details for the new Kafka topic. Choose a descriptive name and 
            appropriate partition and replication settings.
          </DialogContentText>
          {formError && (
            <Alert severity="error" sx={{ mt: 2, mb: 2 }}>
              {formError}
            </Alert>
          )}
          <TextField
            autoFocus
            margin="dense"
            id="name"
            name="name"
            label="Topic Name"
            type="text"
            fullWidth
            variant="outlined"
            value={newTopic.name}
            onChange={handleInputChange}
            sx={{ mb: 2, mt: 2 }}
          />
          <TextField
            margin="dense"
            id="partitions"
            name="partitions"
            label="Number of Partitions"
            type="number"
            fullWidth
            variant="outlined"
            value={newTopic.partitions}
            onChange={handleInputChange}
            sx={{ mb: 2 }}
            InputProps={{ inputProps: { min: 1 } }}
          />
          <TextField
            margin="dense"
            id="replication"
            name="replication"
            label="Replication Factor"
            type="number"
            fullWidth
            variant="outlined"
            value={newTopic.replication}
            onChange={handleInputChange}
            InputProps={{ inputProps: { min: 1 } }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleCreateTopic} color="primary" variant="contained">
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default Topics;
