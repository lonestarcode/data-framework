import { createAsyncThunk } from '@reduxjs/toolkit';
import { analyticsService } from '../../services/analytics.service';
import { AnalyticsData, AnalyticsMetrics } from '../../types/analytics.types';

export const fetchAnalyticsData = createAsyncThunk(
  'analytics/fetchData',
  async (timeRange: string) => {
    const data = await analyticsService.getAnalyticsData(timeRange);
    return data;
  }
);

export const fetchAnalyticsMetrics = createAsyncThunk(
  'analytics/fetchMetrics',
  async () => {
    const metrics = await analyticsService.getMetrics();
    return metrics;
  }
);

export const exportAnalyticsData = createAsyncThunk(
  'analytics/exportData',
  async ({ timeRange, format }: { timeRange: string; format: 'csv' | 'json' }) => {
    const data = await analyticsService.exportData(timeRange, format);
    return data;
  }
);
