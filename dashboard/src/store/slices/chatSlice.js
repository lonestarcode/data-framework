import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { chatService } from '../../services/chat.service';

export const fetchChatHistory = createAsyncThunk(
  'chat/fetchHistory',
  async () => {
    const response = await chatService.getMessageHistory();
    return response;
  }
);

export const sendMessage = createAsyncThunk(
  'chat/sendMessage',
  async (message) => {
    const response = await chatService.sendMessage(message);
    return response;
  }
);

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    messages: [],
    status: 'idle',
    error: null,
    isTyping: false
  },
  reducers: {
    addMessage: (state, action) => {
      state.messages.push(action.payload);
    },
    setTypingStatus: (state, action) => {
      state.isTyping = action.payload;
    },
    clearChatHistory: (state) => {
      state.messages = [];
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch chat history
      .addCase(fetchChatHistory.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchChatHistory.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.messages = action.payload;
        state.error = null;
      })
      .addCase(fetchChatHistory.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      })
      // Send message
      .addCase(sendMessage.pending, (state) => {
        state.isTyping = true;
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.isTyping = false;
        state.messages.push({
          content: action.payload.message,
          sender: 'assistant',
          timestamp: new Date().toISOString()
        });
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.isTyping = false;
        state.error = action.error.message;
      });
  }
});

export const { addMessage, setTypingStatus, clearChatHistory } = chatSlice.actions;
export default chatSlice.reducer;

// Selectors
export const selectAllMessages = (state) => state.chat.messages;
export const selectChatStatus = (state) => state.chat.status;
export const selectChatError = (state) => state.chat.error;
export const selectIsTyping = (state) => state.chat.isTyping; 