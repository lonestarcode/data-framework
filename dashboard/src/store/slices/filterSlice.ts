import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { FilterRule } from '../../types/filter.types';
import {
  fetchFilters,
  createFilter,
  updateFilter,
  deleteFilter,
  testFilter
} from '../actions/filterActions';

interface FilterState {
  filters: FilterRule[];
  loading: boolean;
  error: string | null;
  testResults: Record<string, {
    passRate: number;
    sampleSize: number;
    processingTime: number;
  }>;
}

const initialState: FilterState = {
  filters: [],
  loading: false,
  error: null,
  testResults: {}
};

const filterSlice = createSlice({
  name: 'filters',
  initialState,
  reducers: {
    clearTestResults(state) {
      state.testResults = {};
    },
    updateFilterStatus(state, action: PayloadAction<{ id: string; enabled: boolean }>) {
      const filter = state.filters.find(f => f.id === action.payload.id);
      if (filter) {
        filter.enabled = action.payload.enabled;
      }
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchFilters.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchFilters.fulfilled, (state, action) => {
        state.loading = false;
        state.filters = action.payload;
      })
      .addCase(fetchFilters.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch filters';
      })
      .addCase(createFilter.fulfilled, (state, action) => {
        state.filters.push(action.payload);
      })
      .addCase(updateFilter.fulfilled, (state, action) => {
        const index = state.filters.findIndex(f => f.id === action.payload.id);
        if (index !== -1) {
          state.filters[index] = action.payload;
        }
      })
      .addCase(deleteFilter.fulfilled, (state, action) => {
        state.filters = state.filters.filter(f => f.id !== action.payload);
      })
      .addCase(testFilter.fulfilled, (state, action) => {
        state.testResults[action.payload.filter.id] = action.payload.results;
      });
  }
});

export const { clearTestResults, updateFilterStatus } = filterSlice.actions;

export default filterSlice.reducer;
