import { apiService } from './api.service';
import { wsService } from './websocket.service';

interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  metadata?: {
    confidence?: number;
    source?: string;
    context?: any;
  };
}

interface ChatSession {
  id: string;
  messages: ChatMessage[];
  startTime: Date;
  lastActivity: Date;
}

class ChatService {
  private currentSession: ChatSession | null = null;
  private messageListeners: Set<(message: ChatMessage) => void> = new Set();
  private statusListeners: Set<(status: string) => void> = new Set();

  constructor() {
    // Subscribe to real-time chat updates
    wsService.subscribe('chat_message', (message: ChatMessage) => {
      this.handleIncomingMessage(message);
    });

    wsService.subscribe('chat_status', (status: string) => {
      this.notifyStatusListeners(status);
    });
  }

  async startNewSession(): Promise<ChatSession> {
    const response = await apiService.post('/chat/sessions');
    this.currentSession = {
      id: response.data.id,
      messages: [],
      startTime: new Date(),
      lastActivity: new Date()
    };
    return this.currentSession;
  }

  async sendMessage(content: string, context?: any): Promise<ChatMessage> {
    if (!this.currentSession) {
      await this.startNewSession();
    }

    const message: Partial<ChatMessage> = {
      content,
      sender: 'user',
      timestamp: new Date(),
      metadata: { context }
    };

    try {
      const response = await apiService.sendChatMessage(content, {
        sessionId: this.currentSession?.id,
        context
      });

      const sentMessage: ChatMessage = {
        ...message,
        id: response.data.id
      } as ChatMessage;

      this.addMessageToSession(sentMessage);
      return sentMessage;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  async getMessageHistory(sessionId?: string): Promise<ChatMessage[]> {
    try {
      const response = await apiService.getChatHistory();
      const messages = response.messages.map(msg => ({
        ...msg,
        timestamp: new Date(msg.timestamp)
      }));

      if (this.currentSession) {
        this.currentSession.messages = messages;
      }

      return messages;
    } catch (error) {
      console.error('Error fetching message history:', error);
      throw error;
    }
  }

  subscribeToMessages(callback: (message: ChatMessage) => void) {
    this.messageListeners.add(callback);
    return () => this.messageListeners.delete(callback);
  }

  subscribeToStatus(callback: (status: string) => void) {
    this.statusListeners.add(callback);
    return () => this.statusListeners.delete(callback);
  }

  private handleIncomingMessage(message: ChatMessage) {
    this.addMessageToSession(message);
    this.notifyMessageListeners(message);
  }

  private addMessageToSession(message: ChatMessage) {
    if (this.currentSession) {
      this.currentSession.messages.push(message);
      this.currentSession.lastActivity = new Date();
    }
  }

  private notifyMessageListeners(message: ChatMessage) {
    this.messageListeners.forEach(listener => listener(message));
  }

  private notifyStatusListeners(status: string) {
    this.statusListeners.forEach(listener => listener(status));
  }

  async exportChatHistory(format: 'pdf' | 'txt' = 'txt'): Promise<Blob> {
    if (!this.currentSession?.messages.length) {
      throw new Error('No messages to export');
    }

    const content = this.currentSession.messages
      .map(msg => `[${msg.timestamp.toLocaleString()}] ${msg.sender}: ${msg.content}`)
      .join('\n\n');

    if (format === 'pdf') {
      // Convert to PDF using a PDF library
      // This is a placeholder - implement actual PDF conversion
      return new Blob([content], { type: 'application/pdf' });
    }

    return new Blob([content], { type: 'text/plain' });
  }

  async clearHistory(): Promise<void> {
    try {
      await apiService.post('/chat/clear-history', {
        sessionId: this.currentSession?.id
      });
      
      if (this.currentSession) {
        this.currentSession.messages = [];
      }
    } catch (error) {
      console.error('Error clearing chat history:', error);
      throw error;
    }
  }
}

export const chatService = new ChatService(); 