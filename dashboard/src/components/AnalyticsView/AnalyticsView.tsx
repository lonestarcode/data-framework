import React, { useState, useEffect } from 'react';
import { Chart } from './Chart';
import { DataGrid } from './DataGrid';
import { MetricsPanel } from './MetricsPanel';
import { useAnalytics } from '../../hooks/useAnalytics';
import styles from './styles.module.css';

export const AnalyticsView: React.FC = () => {
  const { data, metrics, loading, error, refreshData } = useAnalytics();
  const [timeRange, setTimeRange] = useState('24h');
  const [viewType, setViewType] = useState<'chart' | 'grid'>('chart');

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>Analytics Dashboard</h2>
        <div className={styles.controls}>
          <select 
            value={timeRange} 
            onChange={(e) => setTimeRange(e.target.value)}
            className={styles.select}
          >
            <option value="1h">Last Hour</option>
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
          </select>
          <div className={styles.viewToggle}>
            <button 
              className={`${styles.toggleButton} ${viewType === 'chart' ? styles.active : ''}`}
              onClick={() => setViewType('chart')}
            >
              Chart View
            </button>
            <button 
              className={`${styles.toggleButton} ${viewType === 'grid' ? styles.active : ''}`}
              onClick={() => setViewType('grid')}
            >
              Grid View
            </button>
          </div>
          <button 
            onClick={refreshData}
            className={styles.refreshButton}
          >
            Refresh
          </button>
        </div>
      </div>

      <MetricsPanel metrics={metrics} />

      {loading ? (
        <div className={styles.loading}>Loading analytics data...</div>
      ) : error ? (
        <div className={styles.error}>{error}</div>
      ) : (
        <div className={styles.content}>
          {viewType === 'chart' ? (
            <Chart data={data} timeRange={timeRange} />
          ) : (
            <DataGrid data={data} />
          )}
        </div>
      )}
    </div>
  );
};
