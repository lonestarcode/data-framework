import React from 'react';
import styles from './styles.module.css';

interface MessageProps {
  message: {
    content: string;
    sender: 'user' | 'assistant';
    timestamp: Date;
    status: 'sending' | 'sent' | 'error';
  };
}

export const Message: React.FC<MessageProps> = ({ message }) => {
  const { content, sender, timestamp, status } = message;

  return (
    <div className={`${styles.messageContainer} ${styles[sender]}`}>
      <div className={styles.messageContent}>
        <p>{content}</p>
        <div className={styles.messageFooter}>
          <span className={styles.timestamp}>
            {timestamp.toLocaleTimeString()}
          </span>
          {status === 'sending' && (
            <span className={styles.status}>Sending...</span>
          )}
          {status === 'error' && (
            <span className={`${styles.status} ${styles.error}`}>
              Failed to send
            </span>
          )}
        </div>
      </div>
    </div>
  );
};
