import { useEffect, useCallback } from 'react';
import { useActions, useAppSelector } from './useRedux';
import { wsService } from '../services/websocket.service';

export const useChat = () => {
  const { chat } = useActions();
  const messages = useAppSelector(state => state.chat.messages);
  const status = useAppSelector(state => state.chat.status);
  const error = useAppSelector(state => state.chat.error);
  const isTyping = useAppSelector(state => state.chat.isTyping);

  useEffect(() => {
    chat.fetchChatHistory();

    const unsubscribe = wsService.subscribe('chat_message', (data) => {
      chat.addMessage(data);
    });

    return () => unsubscribe();
  }, []);

  const sendMessage = useCallback(async (message) => {
    try {
      await chat.sendMessage(message);
      return true;
    } catch (error) {
      return false;
    }
  }, []);

  return {
    messages,
    status,
    error,
    isTyping,
    sendMessage,
    clearHistory: chat.clearChatHistory,
    refreshHistory: chat.fetchChatHistory
  };
};
