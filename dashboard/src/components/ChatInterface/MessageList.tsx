import React from 'react';
import { Message } from './Message';
import styles from './styles.module.css';

interface MessageListProps {
  messages: Array<{
    id: string;
    content: string;
    sender: 'user' | 'assistant';
    timestamp: Date;
    status: 'sending' | 'sent' | 'error';
  }>;
}

export const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <div className={styles.messageList}>
      {messages.map(message => (
        <Message
          key={message.id}
          message={message}
        />
      ))}
    </div>
  );
};
