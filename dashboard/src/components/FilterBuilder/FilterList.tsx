import React from 'react';
import { FilterRule } from './FilterRule';
import { FilterRuleType } from '../../types/filter.types';
import styles from './styles.module.css';

interface FilterListProps {
  rules: FilterRuleType[];
  onUpdateRule: (index: number, updates: Partial<FilterRuleType>) => void;
  onDeleteRule: (index: number) => void;
}

export const FilterList: React.FC<FilterListProps> = ({
  rules,
  onUpdateRule,
  onDeleteRule
}) => {
  return (
    <div className={styles.filterList}>
      {rules.length === 0 ? (
        <div className={styles.emptyState}>
          No filters configured. Click "Add Filter Rule" to begin.
        </div>
      ) : (
        rules.map((rule, index) => (
          <FilterRule
            key={index}
            rule={rule}
            onUpdate={(updates) => onUpdateRule(index, updates)}
            onDelete={() => onDeleteRule(index)}
          />
        ))
      )}
    </div>
  );
};
