import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { createStore } from '../../store/store';
import App from '../../App';
import { analyticsService } from '../../services/analytics.service';
import { filterService } from '../../services/filter.service';
import { chatService } from '../../services/chat.service';

jest.mock('../../services/analytics.service');
jest.mock('../../services/filter.service');
jest.mock('../../services/chat.service');

describe('Dashboard Integration Tests', () => {
  let store: ReturnType<typeof createStore>;

  beforeEach(() => {
    store = createStore();
    setupMocks();
  });

  const setupMocks = () => {
    // Analytics mocks
    (analyticsService.getAnalyticsData as jest.Mock).mockResolvedValue([{
      id: '1',
      timestamp: new Date(),
      scrapeCount: 100,
      filterPassRate: 0.85,
      avgQualityScore: 0.9,
      avgProcessingTime: 150,
      dataRetentionRate: 0.95
    }]);

    // Filter mocks
    (filterService.getFilters as jest.Mock).mockResolvedValue([{
      id: '1',
      name: 'Test Filter',
      type: 'text',
      field: 'content',
      operator: 'contains',
      value: 'test',
      enabled: true,
      priority: 1,
      category: 'advisory'
    }]);

    // Chat mocks
    (chatService.getMessageHistory as jest.Mock).mockResolvedValue([{
      id: '1',
      content: 'Hello',
      sender: 'user',
      timestamp: new Date(),
      status: 'sent'
    }]);
  };

  test('renders main dashboard components', async () => {
    render(
      <Provider store={store}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </Provider>
    );

    // Verify navigation elements
    expect(screen.getByText(/analytics/i)).toBeInTheDocument();
    expect(screen.getByText(/filters/i)).toBeInTheDocument();
    expect(screen.getByText(/chat/i)).toBeInTheDocument();

    // Wait for initial data load
    await waitFor(() => {
      expect(analyticsService.getAnalyticsData).toHaveBeenCalled();
    });
  });

  test('navigates between views', async () => {
    render(
      <Provider store={store}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </Provider>
    );

    // Navigate to Filters
    fireEvent.click(screen.getByText(/filters/i));
    await waitFor(() => {
      expect(filterService.getFilters).toHaveBeenCalled();
    });

    // Navigate to Chat
    fireEvent.click(screen.getByText(/chat/i));
    await waitFor(() => {
      expect(chatService.getMessageHistory).toHaveBeenCalled();
    });
  });

  test('handles real-time updates', async () => {
    const { rerender } = render(
      <Provider store={store}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </Provider>
    );

    // Simulate WebSocket update
    const newAnalyticsData = {
      id: '2',
      timestamp: new Date(),
      scrapeCount: 150,
      filterPassRate: 0.88,
      avgQualityScore: 0.92,
      avgProcessingTime: 145,
      dataRetentionRate: 0.96
    };

    store.dispatch({ 
      type: 'analytics/updateRealTimeData', 
      payload: newAnalyticsData 
    });

    rerender(
      <Provider store={store}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </Provider>
    );

    await waitFor(() => {
      expect(screen.getByText('150')).toBeInTheDocument();
    });
  });

  test('handles error states across components', async () => {
    // Simulate API errors
    (analyticsService.getAnalyticsData as jest.Mock).mockRejectedValue(
      new Error('Failed to fetch analytics')
    );
    (filterService.getFilters as jest.Mock).mockRejectedValue(
      new Error('Failed to fetch filters')
    );

    render(
      <Provider store={store}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </Provider>
    );

    await waitFor(() => {
      expect(screen.getByText(/failed to fetch analytics/i)).toBeInTheDocument();
    });

    // Navigate to Filters to test error handling
    fireEvent.click(screen.getByText(/filters/i));
    await waitFor(() => {
      expect(screen.getByText(/failed to fetch filters/i)).toBeInTheDocument();
    });
  });
}); 