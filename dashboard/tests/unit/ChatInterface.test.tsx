import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { createStore } from '../../store/store';
import { ChatInterface } from '../../components/ChatInterface';
import { chatService } from '../../services/chat.service';
import userEvent from '@testing-library/user-event';
import { ChatMessage } from '../../types/chat.types';

jest.mock('../../services/chat.service');

describe('ChatInterface Unit Tests', () => {
  let store: ReturnType<typeof createStore>;

  const mockMessages: ChatMessage[] = [
    {
      id: '1',
      content: 'Hello',
      sender: 'user',
      timestamp: new Date(),
      status: 'sent'
    },
    {
      id: '2',
      content: 'Hi there! How can I help you?',
      sender: 'assistant',
      timestamp: new Date(),
      status: 'sent'
    }
  ];

  beforeEach(() => {
    store = createStore();
    jest.clearAllMocks();
    setupMocks();
  });

  const setupMocks = () => {
    (chatService.getMessageHistory as jest.Mock).mockResolvedValue(mockMessages);
    (chatService.sendMessage as jest.Mock).mockImplementation((content) => 
      Promise.resolve({
        id: Date.now().toString(),
        content,
        sender: 'user',
        timestamp: new Date(),
        status: 'sent'
      })
    );
  };

  const renderComponent = () => {
    return render(
      <Provider store={store}>
        <ChatInterface />
      </Provider>
    );
  };

  test('renders chat interface with message history', async () => {
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('Hello')).toBeInTheDocument();
      expect(screen.getByText('Hi there! How can I help you?')).toBeInTheDocument();
    });

    // Verify message timestamps
    mockMessages.forEach(message => {
      const timestamp = message.timestamp.toLocaleTimeString();
      expect(screen.getByText(timestamp)).toBeInTheDocument();
    });
  });

  test('sends new message and updates UI', async () => {
    renderComponent();

    const messageText = 'Test message';
    const input = screen.getByPlaceholderText(/type your message/i);
    
    await userEvent.type(input, messageText);
    fireEvent.click(screen.getByTestId('send-button'));

    // Verify input is cleared
    expect(input).toHaveValue('');

    // Verify message appears in chat
    await waitFor(() => {
      expect(screen.getByText(messageText)).toBeInTheDocument();
    });

    expect(chatService.sendMessage).toHaveBeenCalledWith(messageText);
  });

  test('handles message status indicators', async () => {
    renderComponent();

    // Send new message
    const messageText = 'Status test message';
    const input = screen.getByPlaceholderText(/type your message/i);
    
    await userEvent.type(input, messageText);
    fireEvent.click(screen.getByTestId('send-button'));

    // Check sending status
    expect(screen.getByTestId('message-status-sending')).toBeInTheDocument();

    // Wait for sent status
    await waitFor(() => {
      expect(screen.getByTestId('message-status-sent')).toBeInTheDocument();
    });
  });

  test('handles error states and retries', async () => {
    const error = new Error('Failed to send message');
    (chatService.sendMessage as jest.Mock)
      .mockRejectedValueOnce(error)
      .mockResolvedValueOnce({
        id: '3',
        content: 'Retry message',
        sender: 'user',
        timestamp: new Date(),
        status: 'sent'
      });

    renderComponent();

    // Send message that will fail
    const input = screen.getByPlaceholderText(/type your message/i);
    await userEvent.type(input, 'Retry message');
    fireEvent.click(screen.getByTestId('send-button'));

    // Verify error state
    await waitFor(() => {
      expect(screen.getByText(/Failed to send message/i)).toBeInTheDocument();
      expect(screen.getByTestId('message-status-error')).toBeInTheDocument();
    });

    // Try retry
    fireEvent.click(screen.getByTestId('retry-button'));

    // Verify success after retry
    await waitFor(() => {
      expect(screen.getByTestId('message-status-sent')).toBeInTheDocument();
    });
  });

  test('handles message attachments', async () => {
    renderComponent();

    // Trigger file input
    const file = new File(['test content'], 'test.txt', { type: 'text/plain' });
    const fileInput = screen.getByTestId('file-input');
    
    await userEvent.upload(fileInput, file);

    // Verify file preview
    expect(screen.getByText('test.txt')).toBeInTheDocument();

    // Send message with attachment
    fireEvent.click(screen.getByTestId('send-button'));

    expect(chatService.sendMessage).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        attachment: expect.objectContaining({
          name: 'test.txt',
          type: 'text/plain'
        })
      })
    );
  });

  test('handles message formatting options', async () => {
    renderComponent();

    const input = screen.getByPlaceholderText(/type your message/i);
    
    // Test bold formatting
    fireEvent.click(screen.getByTestId('format-bold'));
    await userEvent.type(input, 'Bold text');
    
    expect(input).toHaveValue('**Bold text**');

    // Test code formatting
    fireEvent.click(screen.getByTestId('format-code'));
    await userEvent.type(input, 'Code text');
    
    expect(input).toHaveValue('**Bold text**`Code text`');
  });

  test('handles chat session management', async () => {
    renderComponent();

    // Clear chat
    fireEvent.click(screen.getByTestId('clear-chat'));
    
    // Verify confirmation dialog
    expect(screen.getByText(/clear all messages/i)).toBeInTheDocument();
    
    // Confirm clear
    fireEvent.click(screen.getByTestId('confirm-clear'));

    await waitFor(() => {
      expect(chatService.clearHistory).toHaveBeenCalled();
      expect(screen.queryByText('Hello')).not.toBeInTheDocument();
    });
  });
});
