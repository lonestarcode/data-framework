import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AnalyticsData, AnalyticsMetrics } from '../../types/analytics.types';
import { 
  fetchAnalyticsData, 
  fetchAnalyticsMetrics 
} from '../actions/analyticsActions';

interface AnalyticsState {
  data: AnalyticsData[];
  metrics: AnalyticsMetrics | null;
  loading: boolean;
  error: string | null;
  timeRange: string;
}

const initialState: AnalyticsState = {
  data: [],
  metrics: null,
  loading: false,
  error: null,
  timeRange: '24h'
};

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {
    setTimeRange(state, action: PayloadAction<string>) {
      state.timeRange = action.payload;
    },
    updateRealTimeData(state, action: PayloadAction<AnalyticsData>) {
      state.data = [...state.data, action.payload];
    },
    clearAnalyticsData(state) {
      state.data = [];
      state.metrics = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAnalyticsData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAnalyticsData.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload;
      })
      .addCase(fetchAnalyticsData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch analytics data';
      })
      .addCase(fetchAnalyticsMetrics.fulfilled, (state, action) => {
        state.metrics = action.payload;
      });
  }
});

export const { 
  setTimeRange, 
  updateRealTimeData, 
  clearAnalyticsData 
} = analyticsSlice.actions;

export default analyticsSlice.reducer;
