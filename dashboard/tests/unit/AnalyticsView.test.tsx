import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { createStore } from '../../store/store';
import { AnalyticsView } from '../../components/AnalyticsView';
import { analyticsService } from '../../services/analytics.service';
import { TimeRanges } from '../../utils/constants';
import userEvent from '@testing-library/user-event';
import { AnalyticsData, AnalyticsMetrics } from '../../types/analytics.types';

jest.mock('../../services/analytics.service');

describe('AnalyticsView Unit Tests', () => {
  let store: ReturnType<typeof createStore>;

  const mockAnalyticsData: AnalyticsData = {
    id: '1',
    timestamp: new Date(),
    scrapeCount: 100,
    filterPassRate: 0.85,
    avgQualityScore: 0.92,
    avgProcessingTime: 150,
    dataRetentionRate: 0.95
  };

  const mockMetrics: AnalyticsMetrics = {
    totalScrapes: 1000,
    filterPassRate: 0.85,
    avgQualityScore: 0.9,
    avgProcessingTime: 145,
    scrapeRateChange: 0.05,
    filterRateChange: 0.02,
    qualityScoreChange: 0.03,
    processingTimeChange: -0.01,
    advisoryFilterCount: 10,
    prohibitiveFilterCount: 5,
    dataRetentionRate: 0.95,
    systemMetrics: {
      cpuUsage: 0.65,
      memoryUsage: 0.75,
      errorRate: 0.02
    }
  };

  beforeEach(() => {
    store = createStore();
    jest.clearAllMocks();
    setupMocks();
  });

  const setupMocks = () => {
    (analyticsService.getAnalyticsData as jest.Mock).mockResolvedValue([mockAnalyticsData]);
    (analyticsService.getMetrics as jest.Mock).mockResolvedValue(mockMetrics);
  };

  const renderComponent = () => {
    return render(
      <Provider store={store}>
        <AnalyticsView />
      </Provider>
    );
  };

  test('renders initial analytics dashboard state', async () => {
    renderComponent();

    // Check loading state
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();

    // Wait for data to load
    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    });

    // Verify metrics are displayed
    expect(screen.getByText('1,000')).toBeInTheDocument(); // Total scrapes
    expect(screen.getByText('90%')).toBeInTheDocument(); // Quality score
    expect(screen.getByText('85%')).toBeInTheDocument(); // Filter pass rate
  });

  test('handles time range selection', async () => {
    renderComponent();

    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    });

    // Select different time range
    const timeRangeSelect = screen.getByTestId('time-range-select');
    await userEvent.selectOptions(timeRangeSelect, TimeRanges.WEEK);

    expect(analyticsService.getAnalyticsData).toHaveBeenCalledWith('7d');
  });

  test('updates charts with real-time data', async () => {
    const { rerender } = renderComponent();

    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    });

    // Simulate real-time update
    const newData: AnalyticsData = {
      ...mockAnalyticsData,
      id: '2',
      scrapeCount: 150,
      avgQualityScore: 0.94
    };

    (analyticsService.getAnalyticsData as jest.Mock).mockResolvedValue([newData]);

    // Trigger refresh
    fireEvent.click(screen.getByTestId('refresh-button'));

    await waitFor(() => {
      expect(screen.getByText('150')).toBeInTheDocument();
      expect(screen.getByText('94%')).toBeInTheDocument();
    });
  });

  test('handles data export functionality', async () => {
    renderComponent();

    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    });

    // Open export modal
    fireEvent.click(screen.getByTestId('export-button'));

    // Select export format
    const formatSelect = screen.getByTestId('export-format-select');
    await userEvent.selectOptions(formatSelect, 'csv');

    // Click export
    fireEvent.click(screen.getByTestId('confirm-export-button'));

    expect(analyticsService.exportData).toHaveBeenCalledWith(
      expect.any(String),
      'csv'
    );
  });

  test('displays error state correctly', async () => {
    const error = new Error('Failed to fetch analytics data');
    (analyticsService.getAnalyticsData as jest.Mock).mockRejectedValue(error);

    renderComponent();

    await waitFor(() => {
      expect(screen.getByText(/Failed to fetch analytics data/i)).toBeInTheDocument();
    });

    // Test retry functionality
    const retryButton = screen.getByText(/retry/i);
    fireEvent.click(retryButton);

    expect(analyticsService.getAnalyticsData).toHaveBeenCalledTimes(2);
  });

  test('handles metric card interactions', async () => {
    renderComponent();

    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    });

    // Click on metric card to show detailed view
    fireEvent.click(screen.getByTestId('metric-card-quality-score'));

    // Verify detailed metrics modal
    expect(screen.getByTestId('metric-detail-modal')).toBeInTheDocument();
    expect(screen.getByText(/Quality Score Trend/i)).toBeInTheDocument();
  });

  test('applies correct date formatting', async () => {
    renderComponent();

    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    });

    const dateStr = mockAnalyticsData.timestamp.toLocaleDateString();
    expect(screen.getByText(dateStr)).toBeInTheDocument();
  });

  test('handles system metrics display', async () => {
    renderComponent();

    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    });

    expect(screen.getByText('65%')).toBeInTheDocument(); // CPU Usage
    expect(screen.getByText('75%')).toBeInTheDocument(); // Memory Usage
    expect(screen.getByText('2%')).toBeInTheDocument(); // Error Rate
  });
});
