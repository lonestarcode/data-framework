export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080/api';
export const WS_BASE_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8080/ws';

export const TIME_RANGES = {
  HOUR: '1h',
  DAY: '24h',
  WEEK: '7d',
  MONTH: '30d'
} as const;

export const FILTER_TYPES = {
  TEXT: 'text',
  NUMBER: 'number',
  DATE: 'date',
  BOOLEAN: 'boolean',
  LIST: 'list'
} as const;

export const FILTER_OPERATORS = {
  EQUALS: 'equals',
  NOT_EQUALS: 'notEquals',
  CONTAINS: 'contains',
  NOT_CONTAINS: 'notContains',
  GREATER_THAN: 'greaterThan',
  LESS_THAN: 'lessThan',
  BETWEEN: 'between',
  REGEX: 'regex'
} as const;

export const ERROR_CODES = {
  NETWORK_ERROR: 'NETWORK_ERROR',
  UNAUTHORIZED: 'UNAUTHORIZED',
  FORBIDDEN: 'FORBIDDEN',
  NOT_FOUND: 'NOT_FOUND',
  VALIDATION_ERROR: 'VALIDATION_ERROR'
} as const;

export const CHART_COLORS = {
  PRIMARY: '#3182ce',
  SECONDARY: '#805ad5',
  SUCCESS: '#48bb78',
  WARNING: '#ecc94b',
  DANGER: '#e53e3e',
  GRAY: '#718096'
} as const;

export const PAGINATION = {
  DEFAULT_PAGE: 1,
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [10, 25, 50, 100]
} as const;
