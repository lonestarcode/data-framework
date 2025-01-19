import { configureStore } from '@reduxjs/toolkit';
import analyticsReducer from './slices/analyticsSlice';
import filterReducer from './slices/filterSlice';
import chatReducer from './slices/chatSlice';

export const store = configureStore({
  reducer: {
    analytics: analyticsReducer,
    filters: filterReducer,
    chat: chatReducer
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore these action types
        ignoredActions: ['analytics/updateRealTimeData'],
        // Ignore these field paths in all actions
        ignoredActionPaths: ['payload.timestamp'],
        // Ignore these paths in the state
        ignoredPaths: ['analytics.realTimeData.timestamp'],
      },
    }),
});
