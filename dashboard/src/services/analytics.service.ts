import { apiService } from './api.service';
import { wsService } from './websocket.service';
import { AnalyticsData, AnalyticsMetrics } from '../types/analytics.types';

class AnalyticsService {
  private listeners: Map<string, Set<(data: any) => void>> = new Map();

  constructor() {
    // Subscribe to real-time analytics updates
    wsService.subscribe('analytics_update', (data) => {
      this.notifyListeners('update', data);
    });
  }

  async getAnalyticsData(timeRange: string): Promise<AnalyticsData[]> {
    return apiService.getAnalyticsData(timeRange);
  }

  async getMetrics(): Promise<AnalyticsMetrics> {
    return apiService.getAnalyticsMetrics();
  }

  subscribeToUpdates(callback: (data: any) => void) {
    if (!this.listeners.has('update')) {
      this.listeners.set('update', new Set());
    }
    this.listeners.get('update')?.add(callback);
  }

  unsubscribeFromUpdates(callback: (data: any) => void) {
    this.listeners.get('update')?.delete(callback);
  }

  private notifyListeners(event: string, data: any) {
    this.listeners.get(event)?.forEach(callback => callback(data));
  }

  async exportData(timeRange: string, format: 'csv' | 'json') {
    const data = await this.getAnalyticsData(timeRange);
    
    if (format === 'csv') {
      return this.convertToCSV(data);
    }
    
    return JSON.stringify(data, null, 2);
  }

  private convertToCSV(data: AnalyticsData[]): string {
    const headers = Object.keys(data[0] || {}).join(',');
    const rows = data.map(item => 
      Object.values(item).map(value => 
        typeof value === 'object' ? JSON.stringify(value) : value
      ).join(',')
    );
    
    return [headers, ...rows].join('\n');
  }
}

export const analyticsService = new AnalyticsService(); 