import axios from 'axios';
import { authService } from './auth';

const api = axios.create({
    baseURL: '/api'
});

// Add auth token to requests
api.interceptors.request.use(config => {
    const token = authService.getToken();
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const summaryApi = {
    getSummaries: (params) => api.get('/summaries', { params }),
    search: (query) => api.get(`/summaries/search?q=${query}`),
};

export const sourceApi = {
    getSources: () => api.get('/sources'),
    addSource: (sourceData) => api.post('/sources', sourceData),
    deleteSource: (sourceId) => api.delete(`/sources/${sourceId}`),
};

export const feedbackApi = {
    submitFeedback: (feedbackData) => api.post('/feedback', feedbackData),
};

export default api;
