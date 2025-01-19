import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import { apiService } from '../../services/api.service';
import { FilterRule } from '../../types/filter.types';
import { AnalyticsData } from '../../types/analytics.types';

describe('API Integration Tests', () => {
  let mock: MockAdapter;

  beforeEach(() => {
    mock = new MockAdapter(axios);
  });

  afterEach(() => {
    mock.reset();
  });

  describe('Authentication', () => {
    test('adds auth token to requests when present', async () => {
      const token = 'test-token';
      localStorage.setItem('auth_token', token);

      mock.onGet('/api/filters').reply(config => {
        expect(config.headers?.Authorization).toBe(`Bearer ${token}`);
        return [200, []];
      });

      await apiService.getFilters();
    });

    test('handles 401 responses by redirecting to login', async () => {
      const originalLocation = window.location;
      delete window.location;
      window.location = { ...originalLocation, href: '' };

      mock.onGet('/api/filters').reply(401);

      try {
        await apiService.getFilters();
      } catch (error) {
        expect(localStorage.getItem('auth_token')).toBeNull();
        expect(window.location.href).toBe('/login');
      }

      window.location = originalLocation;
    });
  });

  describe('Filters API', () => {
    const mockFilter: FilterRule = {
      id: '1',
      name: 'Test Filter',
      type: 'text',
      field: 'content',
      operator: 'contains',
      value: 'test',
      enabled: true,
      priority: 1,
      category: 'advisory'
    };

    test('creates filter successfully', async () => {
      mock.onPost('/api/filters').reply(200, mockFilter);

      const response = await apiService.createFilter(mockFilter);
      expect(response).toEqual(mockFilter);
    });

    test('handles filter creation errors', async () => {
      mock.onPost('/api/filters').reply(400, {
        code: 'VALIDATION_ERROR',
        message: 'Invalid filter configuration'
      });

      await expect(apiService.createFilter(mockFilter)).rejects.toThrow();
    });
  });

  describe('Analytics API', () => {
    const mockData: AnalyticsData[] = [{
      id: '1',
      timestamp: new Date(),
      scrapeCount: 100,
      filterPassRate: 0.85,
      avgQualityScore: 0.9,
      avgProcessingTime: 150,
      dataRetentionRate: 0.95
    }];

    test('fetches analytics data with correct time range', async () => {
      mock.onGet('/api/analytics/data').reply(config => {
        expect(config.params.timeRange).toBe('24h');
        return [200, mockData];
      });

      const response = await apiService.getAnalyticsData('24h');
      expect(response).toEqual(mockData);
    });

    test('handles network errors gracefully', async () => {
      mock.onGet('/api/analytics/data').networkError();

      await expect(apiService.getAnalyticsData('24h')).rejects.toThrow();
    });
  });

  describe('Chat API', () => {
    test('sends messages with correct format', async () => {
      const message = 'Test message';
      const context = { source: 'test' };

      mock.onPost('/api/chat/message').reply(config => {
        const data = JSON.parse(config.data);
        expect(data.message).toBe(message);
        expect(data.context).toEqual(context);
        return [200, { message: 'Response', metadata: {} }];
      });

      await apiService.sendChatMessage(message, context);
    });
  });
}); 