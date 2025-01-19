import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';

interface InputAreaProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  error?: string;
}

export const InputArea: React.FC<InputAreaProps> = ({
  onSendMessage,
  isLoading,
  error
}) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.inputArea}>
      {error && <div className={styles.errorMessage}>{error}</div>}
      <div className={styles.inputContainer}>
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          disabled={isLoading}
          rows={1}
          className={styles.messageInput}
        />
        <button
          type="submit"
          disabled={!message.trim() || isLoading}
          className={styles.sendButton}
        >
          {isLoading ? '...' : 'Send'}
        </button>
      </div>
    </form>
  );
};
