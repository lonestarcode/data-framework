import { apiService } from './api.service';
import { wsService } from './websocket.service';
import { FilterRule } from '../types/filter.types';

class FilterService {
  private listeners: Map<string, Set<(data: any) => void>> = new Map();

  constructor() {
    // Subscribe to real-time filter updates
    wsService.subscribe('filter_update', (data) => {
      this.notifyListeners('update', data);
    });
  }

  async getFilters(): Promise<FilterRule[]> {
    return apiService.getFilters();
  }

  async createFilter(filter: Omit<FilterRule, 'id'>): Promise<FilterRule> {
    const newFilter = await apiService.createFilter(filter);
    this.notifyListeners('create', newFilter);
    return newFilter;
  }

  async updateFilter(id: string, updates: Partial<FilterRule>): Promise<FilterRule> {
    const updatedFilter = await apiService.updateFilter(id, updates);
    this.notifyListeners('update', updatedFilter);
    return updatedFilter;
  }

  async deleteFilter(id: string): Promise<void> {
    await apiService.deleteFilter(id);
    this.notifyListeners('delete', id);
  }

  async testFilter(filter: FilterRule) {
    return apiService.testFilter(filter);
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
}

export const filterService = new FilterService(); 