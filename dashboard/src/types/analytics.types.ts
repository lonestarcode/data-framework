export interface AnalyticsData {
  id: string;
  timestamp: Date;
  scrapeCount: number;
  filterPassRate: number;
  avgQualityScore: number;
  avgProcessingTime: number;
  dataRetentionRate: number;
}

export interface AnalyticsMetrics {
  totalScrapes: number;
  filterPassRate: number;
  avgQualityScore: number;
  avgProcessingTime: number;
  scrapeRateChange: number;
  filterRateChange: number;
  qualityScoreChange: number;
  processingTimeChange: number;
  advisoryFilterCount: number;
  prohibitiveFilterCount: number;
  dataRetentionRate: number;
  systemMetrics: {
    cpuUsage: number;
    memoryUsage: number;
    errorRate: number;
  };
}

export interface TimeSeriesData {
  timestamp: Date;
  value: number;
  category?: string;
}

export interface AnalyticsFilter {
  timeRange: string;
  metrics: string[];
  groupBy?: string;
  aggregation?: 'sum' | 'avg' | 'min' | 'max';
}
