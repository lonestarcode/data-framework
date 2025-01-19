import React, { useState, useEffect, useRef } from 'react';
import { MessageList } from './MessageList';
import { InputArea } from './InputArea';
import { Message } from './Message';
import { useChat } from '../../hooks/useChat';
import styles from './styles.module.css';

interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  status: 'sending' | 'sent' | 'error';
}

export const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const { sendMessage, isLoading, error } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      content,
      sender: 'user',
      timestamp: new Date(),
      status: 'sending'
    };

    setMessages(prev => [...prev, newMessage]);

    try {
      const response = await sendMessage(content);
      
      setMessages(prev => [
        ...prev.map(msg => 
          msg.id === newMessage.id ? { ...msg, status: 'sent' } : msg
        ),
        {
          id: Date.now().toString(),
          content: response.message,
          sender: 'assistant',
          timestamp: new Date(),
          status: 'sent'
        }
      ]);
    } catch (err) {
      setMessages(prev =>
        prev.map(msg =>
          msg.id === newMessage.id ? { ...msg, status: 'error' } : msg
        )
      );
    }
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.chatHeader}>
        <h2>LLM Assistant</h2>
        {isLoading && <div className={styles.statusIndicator}>Processing...</div>}
      </div>

      <MessageList messages={messages} />
      
      <InputArea 
        onSendMessage={handleSendMessage} 
        isLoading={isLoading}
        error={error}
      />
      
      <div ref={messagesEndRef} />
    </div>
  );
};
