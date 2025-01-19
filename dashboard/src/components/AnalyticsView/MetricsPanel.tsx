import React from 'react';
import { AnalyticsMetrics } from '../../types/analytics.types';
import styles from './styles.module.css';

interface MetricsPanelProps {
  metrics: AnalyticsMetrics;
}

export const MetricsPanel: React.FC<MetricsPanelProps> = ({ metrics }) => {
  const metricCards = [
    {
      title: 'Total Scrapes',
      value: metrics.totalScrapes.toLocaleString(),
      change: metrics.scrapeRateChange,
      icon: '📊'
    },
    {
      title: 'Filter Pass Rate',
      value: `${(metrics.filterPassRate * 100).toFixed(1)}%`,
      change: metrics.filterRateChange,
      icon: '🎯'
    },
    {
      title: 'Avg Quality Score',
      value: metrics.avgQualityScore.toFixed(2),
      change: metrics.qualityScoreChange,
      icon: '⭐'
    },
    {
      title: 'Processing Time',
      value: `${metrics.avgProcessingTime}ms`,
      change: metrics.processingTimeChange,
      icon: '⚡'
    }
  ];

  return (
    <div className={styles.metricsPanel}>
      {metricCards.map((card, index) => (
        <div key={index} className={styles.metricCard}>
          <div className={styles.metricIcon}>{card.icon}</div>
          <div className={styles.metricContent}>
            <h3 className={styles.metricTitle}>{card.title}</h3>
            <div className={styles.metricValue}>{card.value}</div>
            {card.change !== undefined && (
              <div className={`${styles.metricChange} ${
                card.change > 0 
                  ? styles.positive 
                  : card.change < 0 
                    ? styles.negative 
                    : ''
              }`}>
                {card.change > 0 ? '↑' : card.change < 0 ? '↓' : '–'}
                {Math.abs(card.change).toFixed(1)}%
              </div>
            )}
          </div>
        </div>
      ))}

      <div className={styles.metricDetails}>
        <div className={styles.detailSection}>
          <h4>Filter Performance</h4>
          <div className={styles.detailGrid}>
            <div className={styles.detailItem}>
              <span>Advisory Filters</span>
              <span>{metrics.advisoryFilterCount}</span>
            </div>
            <div className={styles.detailItem}>
              <span>Prohibitive Filters</span>
              <span>{metrics.prohibitiveFilterCount}</span>
            </div>
            <div className={styles.detailItem}>
              <span>Data Retention</span>
              <span>{(metrics.dataRetentionRate * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>

        <div className={styles.detailSection}>
          <h4>System Health</h4>
          <div className={styles.detailGrid}>
            <div className={styles.detailItem}>
              <span>CPU Usage</span>
              <span>{metrics.systemMetrics.cpuUsage}%</span>
            </div>
            <div className={styles.detailItem}>
              <span>Memory Usage</span>
              <span>{metrics.systemMetrics.memoryUsage}%</span>
            </div>
            <div className={styles.detailItem}>
              <span>Error Rate</span>
              <span>{(metrics.systemMetrics.errorRate * 100).toFixed(2)}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
