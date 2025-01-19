import { useState, useEffect } from 'react';
import axios from 'axios';
import { AnalyticsData, AnalyticsMetrics } from '../types/analytics.types';

export const useAnalytics = (timeRange: string = '24h') => {
  const [data, setData] = useState<AnalyticsData[]>([]);
  const [metrics, setMetrics] = useState<AnalyticsMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [dataResponse, metricsResponse] = await Promise.all([
        axios.get(`/api/analytics/data?timeRange=${timeRange}`),
        axios.get('/api/analytics/metrics')
      ]);

      setData(dataResponse.data);
      setMetrics(metricsResponse.data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch analytics data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 300000); // Refresh every 5 minutes
    return () => clearInterval(interval);
  }, [timeRange]);

  const refreshData = () => {
    fetchData();
  };

  return { data, metrics, loading, error, refreshData };
};
