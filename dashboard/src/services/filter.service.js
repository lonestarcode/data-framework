import { apiService } from './api.service';
import { wsService } from './websocket.service';

class FilterService {
  constructor() {
    this.subscribeToUpdates();
  }

  subscribeToUpdates() {
    wsService.subscribe('filter_update', (data) => {
      // Handle real-time filter updates
      console.log('Received filter update:', data);
      // You can dispatch Redux actions or use callbacks here
    });
  }

  async getFilters() {
    try {
      return await apiService.getFilters();
    } catch (error) {
      console.error('Error fetching filters:', error);
      throw error;
    }
  }

  async createFilter(filter) {
    try {
      const response = await apiService.createFilter(filter);
      wsService.send('filter_created', { filter });
      return response;
    } catch (error) {
      console.error('Error creating filter:', error);
      throw error;
    }
  }

  async updateFilter(id, updates) {
    try {
      const response = await apiService.updateFilter(id, updates);
      wsService.send('filter_updated', { id, updates });
      return response;
    } catch (error) {
      console.error('Error updating filter:', error);
      throw error;
    }
  }

  async deleteFilter(id) {
    try {
      const response = await apiService.deleteFilter(id);
      wsService.send('filter_deleted', { id });
      return response;
    } catch (error) {
      console.error('Error deleting filter:', error);
      throw error;
    }
  }
}

export const filterService = new FilterService();
