export interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  status?: 'sending' | 'sent' | 'error';
  metadata?: {
    confidence?: number;
    source?: string;
    context?: any;
  };
}

export interface ChatSession {
  id: string;
  messages: ChatMessage[];
  startTime: Date;
  lastActivity: Date;
  metadata?: {
    topic?: string;
    context?: any;
    userPreferences?: {
      language?: string;
      expertiseLevel?: 'beginner' | 'intermediate' | 'expert';
    };
  };
}

export interface ChatError {
  code: string;
  message: string;
  details?: any;
}

export interface ChatSettings {
  notifications: boolean;
  soundEnabled: boolean;
  theme: 'light' | 'dark';
  fontSize: number;
  language: string;
}
