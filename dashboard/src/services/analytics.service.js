import { apiService } from './api.service';
import { wsService } from './websocket.service';

class AnalyticsService {
  constructor() {
    this.subscribeToUpdates();
  }

  subscribeToUpdates() {
    wsService.subscribe('analytics_update', (data) => {
      // Handle real-time updates
      console.log('Received analytics update:', data);
      // You can dispatch Redux actions here or use callbacks
    });
  }

  async getAnalyticsData(timeRange = '24h') {
    try {
      return await apiService.getAnalyticsData(timeRange);
    } catch (error) {
      console.error('Error fetching analytics data:', error);
      throw error;
    }
  }
}

export const analyticsService = new AnalyticsService();
