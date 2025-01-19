import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { 
  sendMessage, 
  fetchChatHistory, 
  clearChatHistory 
} from '../actions/chatActions';

interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  status?: 'sending' | 'sent' | 'error';
}

interface ChatState {
  messages: ChatMessage[];
  loading: boolean;
  error: string | null;
  currentSession: string | null;
}

const initialState: ChatState = {
  messages: [],
  loading: false,
  error: null,
  currentSession: null
};

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    setCurrentSession(state, action: PayloadAction<string>) {
      state.currentSession = action.payload;
    },
    addMessage(state, action: PayloadAction<ChatMessage>) {
      state.messages.push(action.payload);
    },
    updateMessageStatus(
      state,
      action: PayloadAction<{ id: string; status: 'sending' | 'sent' | 'error' }>
    ) {
      const message = state.messages.find(m => m.id === action.payload.id);
      if (message) {
        message.status = action.payload.status;
      }
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.loading = false;
        state.messages.push(action.payload);
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to send message';
      })
      .addCase(fetchChatHistory.fulfilled, (state, action) => {
        state.messages = action.payload;
      })
      .addCase(clearChatHistory.fulfilled, (state) => {
        state.messages = [];
      });
  }
});

export const { 
  setCurrentSession, 
  addMessage, 
  updateMessageStatus 
} = chatSlice.actions;

export default chatSlice.reducer;
