import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // You can add auth tokens here
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const apiService = {
  // Analytics endpoints
  getAnalyticsData: (timeRange) => 
    api.get(`/analytics/data?timeRange=${timeRange}`),
  
  // Filter endpoints
  getFilters: () => 
    api.get('/filters'),
  createFilter: (filter) => 
    api.post('/filters', filter),
  updateFilter: (id, updates) => 
    api.put(`/filters/${id}`, updates),
  deleteFilter: (id) => 
    api.delete(`/filters/${id}`),
  
  // Chat endpoints
  getChatHistory: () => 
    api.get('/chat/history'),
  sendMessage: (message) => 
    api.post('/chat/message', { message })
};
