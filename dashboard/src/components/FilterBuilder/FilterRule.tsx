import React from 'react';
import { FilterRuleType } from '../../types/filter.types';
import styles from './styles.module.css';

interface FilterRuleProps {
  rule: FilterRuleType;
  onUpdate: (updates: Partial<FilterRuleType>) => void;
  onDelete: () => void;
}

export const FilterRule: React.FC<FilterRuleProps> = ({
  rule,
  onUpdate,
  onDelete
}) => {
  const fields = [
    'content',
    'title',
    'author',
    'date',
    'sentiment',
    'reliability',
    'quality'
  ];

  const operators = {
    advisory: [
      { value: 'contains', label: 'Contains' },
      { value: 'not_contains', label: 'Does Not Contain' },
      { value: 'greater_than', label: 'Greater Than' },
      { value: 'less_than', label: 'Less Than' }
    ],
    prohibitive: [
      { value: 'equals', label: 'Equals' },
      { value: 'not_equals', label: 'Does Not Equal' },
      { value: 'matches', label: 'Matches Pattern' }
    ]
  };

  return (
    <div className={styles.ruleContainer}>
      <div className={styles.ruleHeader}>
        <select
          value={rule.type}
          onChange={(e) => onUpdate({ type: e.target.value as 'advisory' | 'prohibitive' })}
          className={styles.typeSelect}
        >
          <option value="advisory">Advisory Filter</option>
          <option value="prohibitive">Prohibitive Filter</option>
        </select>
        <button 
          onClick={onDelete}
          className={styles.deleteButton}
          aria-label="Delete rule"
        >
          ×
        </button>
      </div>

      <div className={styles.ruleBody}>
        <div className={styles.fieldGroup}>
          <label>Field</label>
          <select
            value={rule.field}
            onChange={(e) => onUpdate({ field: e.target.value })}
          >
            <option value="">Select Field</option>
            {fields.map(field => (
              <option key={field} value={field}>
                {field.charAt(0).toUpperCase() + field.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <div className={styles.fieldGroup}>
          <label>Operator</label>
          <select
            value={rule.operator}
            onChange={(e) => onUpdate({ operator: e.target.value })}
          >
            {operators[rule.type].map(op => (
              <option key={op.value} value={op.value}>
                {op.label}
              </option>
            ))}
          </select>
        </div>

        <div className={styles.fieldGroup}>
          <label>Value</label>
          <input
            type="text"
            value={rule.value}
            onChange={(e) => onUpdate({ value: e.target.value })}
            placeholder="Enter value..."
          />
        </div>

        {rule.type === 'advisory' && (
          <div className={styles.fieldGroup}>
            <label>Threshold</label>
            <div className={styles.thresholdContainer}>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={rule.threshold || 0.5}
                onChange={(e) => onUpdate({ threshold: parseFloat(e.target.value) })}
              />
              <span className={styles.thresholdValue}>
                {(rule.threshold || 0.5).toFixed(1)}
              </span>
            </div>
          </div>
        )}
      </div>

      {rule.type === 'advisory' && (
        <div className={styles.ruleFooter}>
          <div className={styles.confidenceIndicator}>
            Confidence Threshold: {((rule.threshold || 0.5) * 100).toFixed()}%
          </div>
        </div>
      )}
    </div>
  );
};
