import { useEffect } from 'react';
import { useActions, useAppSelector } from './useRedux';
import { wsService } from '../services/websocket.service';

export const useAnalytics = (timeRange = '24h') => {
  const { analytics } = useActions();
  const data = useAppSelector(state => state.analytics.data);
  const status = useAppSelector(state => state.analytics.status);
  const error = useAppSelector(state => state.analytics.error);

  useEffect(() => {
    analytics.fetchAnalyticsData(timeRange);

    const unsubscribe = wsService.subscribe('analytics_update', (data) => {
      analytics.updateRealTimeData(data);
    });

    return () => unsubscribe();
  }, [timeRange]);

  return {
    data,
    status,
    error,
    refreshData: () => analytics.fetchAnalyticsData(timeRange),
    setTimeRange: analytics.setTimeRange
  };
};
