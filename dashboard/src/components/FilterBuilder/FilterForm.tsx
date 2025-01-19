import React, { useState } from 'react';
import { FilterRuleType } from '../../types/filter.types';
import styles from './styles.module.css';

interface FilterFormProps {
  onSubmit: (rule: FilterRuleType) => void;
  initialValues?: Partial<FilterRuleType>;
  onCancel?: () => void;
}

export const FilterForm: React.FC<FilterFormProps> = ({
  onSubmit,
  initialValues,
  onCancel
}) => {
  const [formData, setFormData] = useState<FilterRuleType>({
    type: initialValues?.type || 'advisory',
    field: initialValues?.field || '',
    operator: initialValues?.operator || 'contains',
    value: initialValues?.value || '',
    threshold: initialValues?.threshold || 0.5,
    enabled: initialValues?.enabled ?? true
  });

  const [errors, setErrors] = useState<Partial<Record<keyof FilterRuleType, string>>>({});

  const validateForm = (): boolean => {
    const newErrors: Partial<Record<keyof FilterRuleType, string>> = {};

    if (!formData.field) {
      newErrors.field = 'Field is required';
    }

    if (!formData.value) {
      newErrors.value = 'Value is required';
    }

    if (formData.type === 'advisory' && (formData.threshold < 0 || formData.threshold > 1)) {
      newErrors.threshold = 'Threshold must be between 0 and 1';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  const handleChange = (field: keyof FilterRuleType, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
    // Clear error when field is updated
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: undefined
      }));
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.filterForm}>
      <div className={styles.formHeader}>
        <h3>{initialValues ? 'Edit Filter Rule' : 'Create New Filter Rule'}</h3>
      </div>

      <div className={styles.formBody}>
        <div className={styles.formGroup}>
          <label>Filter Type</label>
          <select
            value={formData.type}
            onChange={(e) => handleChange('type', e.target.value)}
            className={styles.select}
          >
            <option value="advisory">Advisory Filter</option>
            <option value="prohibitive">Prohibitive Filter</option>
          </select>
        </div>

        <div className={styles.formGroup}>
          <label>Field</label>
          <select
            value={formData.field}
            onChange={(e) => handleChange('field', e.target.value)}
            className={`${styles.select} ${errors.field ? styles.error : ''}`}
          >
            <option value="">Select Field</option>
            <option value="content">Content</option>
            <option value="title">Title</option>
            <option value="author">Author</option>
            <option value="sentiment">Sentiment</option>
            <option value="reliability">Reliability</option>
            <option value="quality">Quality</option>
          </select>
          {errors.field && <span className={styles.errorText}>{errors.field}</span>}
        </div>

        <div className={styles.formGroup}>
          <label>Operator</label>
          <select
            value={formData.operator}
            onChange={(e) => handleChange('operator', e.target.value)}
            className={styles.select}
          >
            {formData.type === 'advisory' ? (
              <>
                <option value="contains">Contains</option>
                <option value="not_contains">Does Not Contain</option>
                <option value="greater_than">Greater Than</option>
                <option value="less_than">Less Than</option>
              </>
            ) : (
              <>
                <option value="equals">Equals</option>
                <option value="not_equals">Does Not Equal</option>
                <option value="matches">Matches Pattern</option>
              </>
            )}
          </select>
        </div>

        <div className={styles.formGroup}>
          <label>Value</label>
          <input
            type="text"
            value={formData.value}
            onChange={(e) => handleChange('value', e.target.value)}
            className={`${styles.input} ${errors.value ? styles.error : ''}`}
            placeholder="Enter filter value..."
          />
          {errors.value && <span className={styles.errorText}>{errors.value}</span>}
        </div>

        {formData.type === 'advisory' && (
          <div className={styles.formGroup}>
            <label>
              Confidence Threshold: {formData.threshold.toFixed(1)}
            </label>
            <div className={styles.thresholdControl}>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={formData.threshold}
                onChange={(e) => handleChange('threshold', parseFloat(e.target.value))}
                className={styles.rangeInput}
              />
              <span className={styles.thresholdValue}>
                {(formData.threshold * 100).toFixed()}%
              </span>
            </div>
            {errors.threshold && <span className={styles.errorText}>{errors.threshold}</span>}
          </div>
        )}

        <div className={styles.formGroup}>
          <label className={styles.checkboxLabel}>
            <input
              type="checkbox"
              checked={formData.enabled}
              onChange={(e) => handleChange('enabled', e.target.checked)}
              className={styles.checkbox}
            />
            Enable Filter
          </label>
        </div>
      </div>

      <div className={styles.formFooter}>
        {onCancel && (
          <button 
            type="button" 
            onClick={onCancel}
            className={styles.cancelButton}
          >
            Cancel
          </button>
        )}
        <button 
          type="submit"
          className={styles.submitButton}
        >
          {initialValues ? 'Update Filter' : 'Create Filter'}
        </button>
      </div>
    </form>
  );
};
