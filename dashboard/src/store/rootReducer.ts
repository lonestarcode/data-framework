import { combineReducers } from '@reduxjs/toolkit';
import analyticsReducer from './slices/analyticsSlice';
import filterReducer from './slices/filterSlice';
import chatReducer from './slices/chatSlice';

const rootReducer = combineReducers({
  analytics: analyticsReducer,
  filters: filterReducer,
  chat: chatReducer,
});

export type RootState = ReturnType<typeof rootReducer>;
export default rootReducer;
