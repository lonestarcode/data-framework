import React, { useMemo } from 'react';
import {
  Line,
  Bar,
  ComposedChart,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  ResponsiveContainer
} from 'recharts';
import { AnalyticsData } from '../../types/analytics.types';
import styles from './styles.module.css';

interface ChartProps {
  data: AnalyticsData[];
  timeRange: string;
}

export const Chart: React.FC<ChartProps> = ({ data, timeRange }) => {
  const chartData = useMemo(() => {
    // Process data based on timeRange
    return data.map(item => ({
      timestamp: new Date(item.timestamp).toLocaleString(),
      scrapeCount: item.metrics.scrapeCount,
      filterPassRate: item.metrics.filterPassRate * 100,
      avgQualityScore: item.metrics.qualityScore,
      processingTime: item.metrics.processingTime
    }));
  }, [data, timeRange]);

  return (
    <div className={styles.chartContainer}>
      <ResponsiveContainer width="100%" height={400}>
        <ComposedChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="timestamp" 
            scale="time" 
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => {
              const date = new Date(value);
              return timeRange === '1h' 
                ? date.toLocaleTimeString() 
                : date.toLocaleDateString();
            }}
          />
          <YAxis yAxisId="left" />
          <YAxis yAxisId="right" orientation="right" />
          <Tooltip />
          <Legend />
          
          <Bar 
            yAxisId="left"
            dataKey="scrapeCount" 
            fill="#8884d8" 
            name="Scrape Count"
          />
          <Line 
            yAxisId="right"
            type="monotone" 
            dataKey="filterPassRate" 
            stroke="#82ca9d" 
            name="Filter Pass Rate (%)"
          />
          <Line 
            yAxisId="right"
            type="monotone" 
            dataKey="avgQualityScore" 
            stroke="#ffc658" 
            name="Quality Score"
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
};
