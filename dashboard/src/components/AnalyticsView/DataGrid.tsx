import React, { useState } from 'react';
import { AnalyticsData } from '../../types/analytics.types';
import styles from './styles.module.css';

interface DataGridProps {
  data: AnalyticsData[];
}

export const DataGrid: React.FC<DataGridProps> = ({ data }) => {
  const [sortField, setSortField] = useState<keyof AnalyticsData>('timestamp');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');
  const [page, setPage] = useState(1);
  const rowsPerPage = 10;

  const sortedData = [...data].sort((a, b) => {
    if (sortDirection === 'asc') {
      return a[sortField] > b[sortField] ? 1 : -1;
    }
    return a[sortField] < b[sortField] ? 1 : -1;
  });

  const paginatedData = sortedData.slice(
    (page - 1) * rowsPerPage,
    page * rowsPerPage
  );

  const handleSort = (field: keyof AnalyticsData) => {
    if (field === sortField) {
      setSortDirection(prev => prev === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  return (
    <div className={styles.gridContainer}>
      <table className={styles.table}>
        <thead>
          <tr>
            <th onClick={() => handleSort('timestamp')}>
              Timestamp
              {sortField === 'timestamp' && (
                <span className={styles.sortIndicator}>
                  {sortDirection === 'asc' ? '↑' : '↓'}
                </span>
              )}
            </th>
            <th onClick={() => handleSort('metrics')}>
              Scrape Count
              {sortField === 'metrics' && (
                <span className={styles.sortIndicator}>
                  {sortDirection === 'asc' ? '↑' : '↓'}
                </span>
              )}
            </th>
            <th>Filter Pass Rate</th>
            <th>Quality Score</th>
            <th>Processing Time</th>
          </tr>
        </thead>
        <tbody>
          {paginatedData.map((item, index) => (
            <tr key={index}>
              <td>{new Date(item.timestamp).toLocaleString()}</td>
              <td>{item.metrics.scrapeCount}</td>
              <td>{(item.metrics.filterPassRate * 100).toFixed(1)}%</td>
              <td>{item.metrics.qualityScore.toFixed(2)}</td>
              <td>{item.metrics.processingTime}ms</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className={styles.pagination}>
        <button 
          onClick={() => setPage(p => Math.max(1, p - 1))}
          disabled={page === 1}
        >
          Previous
        </button>
        <span>Page {page} of {Math.ceil(data.length / rowsPerPage)}</span>
        <button 
          onClick={() => setPage(p => Math.min(Math.ceil(data.length / rowsPerPage), p + 1))}
          disabled={page >= Math.ceil(data.length / rowsPerPage)}
        >
          Next
        </button>
      </div>
    </div>
  );
};
