import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { analyticsService } from '../../services/analytics.service';

export const fetchAnalyticsData = createAsyncThunk(
  'analytics/fetchData',
  async (timeRange) => {
    const response = await analyticsService.getAnalyticsData(timeRange);
    return response;
  }
);

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState: {
    data: [],
    realTimeData: null,
    timeRange: '24h',
    status: 'idle',
    error: null
  },
  reducers: {
    setTimeRange: (state, action) => {
      state.timeRange = action.payload;
    },
    updateRealTimeData: (state, action) => {
      state.realTimeData = action.payload;
      state.data = [...state.data.slice(1), action.payload];
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAnalyticsData.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchAnalyticsData.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.data = action.payload;
        state.error = null;
      })
      .addCase(fetchAnalyticsData.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      });
  }
});

export const { setTimeRange, updateRealTimeData } = analyticsSlice.actions;
export default analyticsSlice.reducer; 