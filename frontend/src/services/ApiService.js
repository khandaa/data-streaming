import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const ApiService = {
  // Health check
  healthCheck: () => {
    return axios.get(`${API_URL}/health`);
  },
  
  // Metrics
  getMetrics: () => {
    return axios.get(`${API_URL}/metrics`);
  },
  
  // Stream control
  startStream: () => {
    return axios.post(`${API_URL}/stream/start`);
  },
  
  stopStream: () => {
    return axios.post(`${API_URL}/stream/stop`);
  },
  
  // Topics
  getTopics: () => {
    return axios.get(`${API_URL}/topics`);
  },
  
  createTopic: (data) => {
    return axios.post(`${API_URL}/topics`, data);
  },
  
  // Admin
  login: (credentials) => {
    return axios.post(`${API_URL}/admin/login`, credentials);
  },
  
  // Add interceptor for authentication
  setupInterceptors: () => {
    axios.interceptors.request.use(
      (config) => {
        const user = JSON.parse(localStorage.getItem('user'));
        if (user && user.token) {
          config.headers['Authorization'] = `Bearer ${user.token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );
    
    axios.interceptors.response.use(
      (response) => {
        return response;
      },
      (error) => {
        if (error.response && error.response.status === 401) {
          // Handle 401 Unauthorized - redirect to login or clear local storage
          localStorage.removeItem('user');
          window.location.href = '/admin/login';
        }
        return Promise.reject(error);
      }
    );
  }
};

// Set up interceptors
ApiService.setupInterceptors();

export default ApiService;
