import axios, { AxiosInstance } from 'axios';
import { FilterRule } from '../types/filter.types';
import { AnalyticsData, AnalyticsMetrics } from '../types/analytics.types';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.REACT_APP_API_URL || '/api',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // Add request interceptor for authentication
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('auth_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Add response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Handle unauthorized access
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Filter endpoints
  async getFilters(): Promise<FilterRule[]> {
    const response = await this.api.get('/filters');
    return response.data;
  }

  async createFilter(filter: Omit<FilterRule, 'id'>): Promise<FilterRule> {
    const response = await this.api.post('/filters', filter);
    return response.data;
  }

  async updateFilter(id: string, updates: Partial<FilterRule>): Promise<FilterRule> {
    const response = await this.api.patch(`/filters/${id}`, updates);
    return response.data;
  }

  async deleteFilter(id: string): Promise<void> {
    await this.api.delete(`/filters/${id}`);
  }

  async testFilter(filter: FilterRule): Promise<{
    passRate: number;
    sampleSize: number;
    processingTime: number;
  }> {
    const response = await this.api.post('/filters/test', filter);
    return response.data;
  }

  // Analytics endpoints
  async getAnalyticsData(timeRange: string): Promise<AnalyticsData[]> {
    const response = await this.api.get(`/analytics/data?timeRange=${timeRange}`);
    return response.data;
  }

  async getAnalyticsMetrics(): Promise<AnalyticsMetrics> {
    const response = await this.api.get('/analytics/metrics');
    return response.data;
  }

  // Chat endpoints
  async sendChatMessage(message: string, context?: any): Promise<{
    message: string;
    metadata?: any;
  }> {
    const response = await this.api.post('/chat/message', { message, context });
    return response.data;
  }

  async getChatHistory(): Promise<{
    messages: Array<{
      id: string;
      content: string;
      sender: 'user' | 'assistant';
      timestamp: Date;
    }>;
  }> {
    const response = await this.api.get('/chat/history');
    return response.data;
  }
}

export const apiService = new ApiService(); 