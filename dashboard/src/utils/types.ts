export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

export type ValueOf<T> = T[keyof T];

export type Nullable<T> = T | null;

export type AsyncState<T> = {
  data: T | null;
  loading: boolean;
  error: string | null;
};

export type SortDirection = 'asc' | 'desc';

export type SortConfig = {
  field: string;
  direction: SortDirection;
};

export type FilterConfig = {
  field: string;
  value: any;
  operator: string;
};

export type PaginationConfig = {
  page: number;
  pageSize: number;
  total: number;
};

export type DateRange = {
  startDate: Date;
  endDate: Date;
};
