import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { updateFilters } from '../../store/slices/filterSlice';
import styles from './styles.module.css';

interface FilterRule {
  type: 'advisory' | 'prohibitive';
  field: string;
  operator: 'contains' | 'equals' | 'greater_than' | 'less_than';
  value: string;
  threshold?: number;
}

export const FilterBuilder: React.FC = () => {
  const [rules, setRules] = useState<FilterRule[]>([]);
  const [metrics, setMetrics] = useState<any>(null);
  const dispatch = useDispatch();

  const addRule = () => {
    setRules([...rules, {
      type: 'advisory',
      field: '',
      operator: 'contains',
      value: '',
      threshold: 0.5
    }]);
  };

  const updateRule = (index: number, updates: Partial<FilterRule>) => {
    const newRules = rules.map((rule, i) => 
      i === index ? { ...rule, ...updates } : rule
    );
    setRules(newRules);
    dispatch(updateFilters(newRules));
  };

  const testFilters = async () => {
    try {
      const response = await fetch('/api/filters/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rules })
      });
      const data = await response.json();
      setMetrics(data.metrics);
    } catch (error) {
      console.error('Error testing filters:', error);
    }
  };

  return (
    <div className={styles.container}>
      <h2>Scraping Filter Configuration</h2>
      
      <div className={styles.ruleList}>
        {rules.map((rule, index) => (
          <div key={index} className={styles.ruleCard}>
            <select
              value={rule.type}
              onChange={(e) => updateRule(index, { type: e.target.value as 'advisory' | 'prohibitive' })}
            >
              <option value="advisory">Advisory</option>
              <option value="prohibitive">Prohibitive</option>
            </select>

            <input
              type="text"
              placeholder="Field"
              value={rule.field}
              onChange={(e) => updateRule(index, { field: e.target.value })}
            />

            <select
              value={rule.operator}
              onChange={(e) => updateRule(index, { operator: e.target.value as any })}
            >
              <option value="contains">Contains</option>
              <option value="equals">Equals</option>
              <option value="greater_than">Greater Than</option>
              <option value="less_than">Less Than</option>
            </select>

            <input
              type="text"
              placeholder="Value"
              value={rule.value}
              onChange={(e) => updateRule(index, { value: e.target.value })}
            />

            {rule.type === 'advisory' && (
              <input
                type="number"
                placeholder="Threshold"
                value={rule.threshold}
                onChange={(e) => updateRule(index, { threshold: parseFloat(e.target.value) })}
                min="0"
                max="1"
                step="0.1"
              />
            )}
          </div>
        ))}
      </div>

      <div className={styles.actions}>
        <button onClick={addRule}>Add Filter Rule</button>
        <button onClick={testFilters}>Test Filters</button>
      </div>

      {metrics && (
        <div className={styles.metrics}>
          <h3>Filter Performance</h3>
          <div>Data Retention Rate: {metrics.retentionRate}%</div>
          <div>Processing Speed: {metrics.processingSpeed}ms</div>
          <div>Quality Score: {metrics.qualityScore}</div>
        </div>
      )}
    </div>
  );
};
