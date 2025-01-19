import { RootState } from '../store/rootReducer';
import { store } from '../store/store';

export type AppDispatch = typeof store.dispatch;
export type AppThunk<ReturnType = void> = import('@reduxjs/toolkit').ThunkAction<
  ReturnType,
  RootState,
  unknown,
  import('@reduxjs/toolkit').Action<string>
>;

export interface AsyncState {
  loading: boolean;
  error: string | null;
}

export interface PaginatedState<T> extends AsyncState {
  data: T[];
  pagination: {
    page: number;
    pageSize: number;
    totalPages: number;
    totalItems: number;
  };
}

export interface FilterState {
  search: string;
  sortBy: string;
  sortOrder: 'asc' | 'desc';
  filters: Record<string, any>;
} 