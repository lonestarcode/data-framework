import { apiService } from './api.service';
import { wsService } from './websocket.service';

class ChatService {
  constructor() {
    this.subscribeToUpdates();
  }

  subscribeToUpdates() {
    wsService.subscribe('chat_message', (data) => {
      // Handle real-time message updates
      console.log('Received chat message:', data);
      // You can dispatch Redux actions or use callbacks here
    });
  }

  async getMessageHistory() {
    try {
      return await apiService.getChatHistory();
    } catch (error) {
      console.error('Error fetching chat history:', error);
      throw error;
    }
  }

  async sendMessage(message) {
    try {
      const response = await apiService.sendMessage(message);
      // Optionally notify through WebSocket for real-time updates
      wsService.send('new_message', { message });
      return response;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }
}

export const chatService = new ChatService();
