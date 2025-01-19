export type FilterOperator = 
  | 'equals'
  | 'notEquals'
  | 'contains'
  | 'notContains'
  | 'greaterThan'
  | 'lessThan'
  | 'between'
  | 'regex';

export type FilterType = 
  | 'text'
  | 'number'
  | 'date'
  | 'boolean'
  | 'list';

export interface FilterRule {
  id: string;
  name: string;
  description?: string;
  type: FilterType;
  field: string;
  operator: FilterOperator;
  value: any;
  threshold?: number;
  enabled: boolean;
  priority: number;
  category: 'advisory' | 'prohibitive';
  metadata?: {
    createdAt: Date;
    updatedAt: Date;
    createdBy: string;
    version: number;
    performance?: {
      avgProcessingTime: number;
      passRate: number;
      lastTested: Date;
    };
  };
}

export interface FilterValidation {
  isValid: boolean;
  errors: {
    field: string;
    message: string;
  }[];
}

export interface FilterTestResult {
  passRate: number;
  sampleSize: number;
  processingTime: number;
  examples: {
    passed: string[];
    failed: string[];
  };
}
