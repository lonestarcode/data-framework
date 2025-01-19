import { configureStore, Action, ThunkAction } from '@reduxjs/toolkit';
import { useDispatch } from 'react-redux';
import rootReducer, { RootState } from './rootReducer';
import { wsService } from '../services/websocket.service';
import { updateRealTimeData } from './slices/analyticsSlice';
import { addMessage } from './slices/chatSlice';
import { updateFilterStatus } from './slices/filterSlice';

const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore these action types
        ignoredActions: ['chat/addMessage', 'analytics/updateRealTimeData'],
        // Ignore these field paths in all actions
        ignoredActionPaths: ['payload.timestamp', 'meta.arg.timestamp'],
        // Ignore these paths in the state
        ignoredPaths: ['chat.messages.timestamp'],
      },
      thunk: true,
    }),
  devTools: process.env.NODE_ENV !== 'production',
});

// Setup WebSocket listeners for real-time updates
wsService.subscribe('analytics_update', (data) => {
  store.dispatch(updateRealTimeData(data));
});

wsService.subscribe('chat_message', (message) => {
  store.dispatch(addMessage(message));
});

wsService.subscribe('filter_status', (data) => {
  store.dispatch(updateFilterStatus(data));
});

// Typed hooks
export type AppDispatch = typeof store.dispatch;
export const useAppDispatch = () => useDispatch<AppDispatch>();

export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;

export default store;
