import { useState, useCallback } from 'react';
import axios from 'axios';

interface ChatResponse {
  message: string;
  metadata?: {
    confidence: number;
    source?: string;
  };
}

export const useChat = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(async (message: string): Promise<ChatResponse> => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/chat/message', {
        message,
        context: {
          timestamp: new Date().toISOString(),
          source: 'dashboard'
        }
      });

      return response.data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { sendMessage, isLoading, error };
};
