import { createAsyncThunk } from '@reduxjs/toolkit';
import { chatService } from '../../services/chat.service';

export const sendMessage = createAsyncThunk(
  'chat/sendMessage',
  async ({ content, context }: { content: string; context?: any }) => {
    const message = await chatService.sendMessage(content, context);
    return message;
  }
);

export const fetchChatHistory = createAsyncThunk(
  'chat/fetchHistory',
  async (sessionId?: string) => {
    const history = await chatService.getMessageHistory(sessionId);
    return history;
  }
);

export const clearChatHistory = createAsyncThunk(
  'chat/clearHistory',
  async () => {
    await chatService.clearHistory();
    return null;
  }
);

export const exportChatHistory = createAsyncThunk(
  'chat/exportHistory',
  async (format: 'pdf' | 'txt') => {
    const blob = await chatService.exportChatHistory(format);
    return blob;
  }
);
