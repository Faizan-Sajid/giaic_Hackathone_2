'use client';

import { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Minus } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';

interface Message {
  id: string;
  role: string;
  content: string;
}

export default function FloatingChatbot() {
  const { user, isLoading: authLoading } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [dimensions, setDimensions] = useState({ width: 380, height: 500 });
  const [isResizing, setIsResizing] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const resizeHandleRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  // Handle resizing
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizing || !containerRef.current) return;

      const containerRect = containerRef.current.getBoundingClientRect();
      let newWidth = e.clientX - containerRect.left;
      let newHeight = e.clientY - containerRect.top;

      // Apply constraints
      newWidth = Math.max(320, Math.min(newWidth, 600));
      newHeight = Math.max(400, Math.min(newHeight, 800));

      setDimensions({ width: newWidth, height: newHeight });
    };

    const handleMouseUp = () => {
      setIsResizing(false);
    };

    if (isResizing) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isResizing]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading || !user) return;

    // Add user message to UI immediately
    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputMessage;
    setInputMessage('');
    setIsLoading(true);

    try {
      // Call our backend API using the standard client which handles cookies properly
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${user.id}/chat`, {
        method: 'POST',
        credentials: 'include', // Include HTTP-only cookies
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: currentInput
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update conversation ID if it's the first message
      if (!conversationId) {
        setConversationId(data.conversation_id);
      }

      // Add assistant message to UI
      const assistantMessage = {
        id: `ai-${Date.now()}`,
        role: 'assistant',
        content: data.response
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Process any tool calls if present
      if (data.tool_calls && data.tool_calls.length > 0) {
        // Add a visual indication that tools are being processed
        const toolProcessingMessage = {
          id: `tool-${Date.now()}`,
          role: 'system',
          content: `Processing ${data.tool_calls.length} tool${data.tool_calls.length > 1 ? 's' : ''}...`
        };

        setMessages(prev => [...prev, toolProcessingMessage]);

        // Log tool calls for debugging
        console.log('Tool calls received:', data.tool_calls);

        // Remove the tool processing message after a short delay
        setTimeout(() => {
          setMessages(prev => prev.filter(msg => msg.id !== toolProcessingMessage.id));
        }, 2000);
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to UI
      const errorMessage = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.'
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleResizeMouseDown = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsResizing(true);
  };

  return (
    <>
      {/* Floating Action Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-50 bg-gradient-to-tr from-indigo-600 to-violet-500 text-white p-4 rounded-full shadow-lg hover:shadow-xl hover:from-indigo-700 hover:to-violet-600 transition-all duration-300 hover:scale-110 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 animate-pulse"
          aria-label="Open AI Chatbot"
        >
          <MessageCircle size={24} />
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div
          ref={containerRef}
          className="fixed bottom-24 right-6 z-50 bg-white/90 backdrop-blur-md rounded-2xl shadow-2xl border border-gray-200/50 flex flex-col overflow-hidden"
          style={{
            width: `${dimensions.width}px`,
            height: `${dimensions.height}px`,
            maxWidth: '600px',
            maxHeight: '800px',
            minWidth: '320px',
            minHeight: '400px'
          }}
        >
          {/* Header */}
          <div className="bg-white border-b border-gray-200/50 p-4 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <h3 className="font-medium text-gray-800 text-base">AI Task Assistant</h3>
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            </div>
            <div className="flex space-x-1">
              <button
                onClick={() => {
                  // Minimize functionality can be added here
                }}
                className="text-gray-500 hover:text-gray-700 focus:outline-none p-1 rounded hover:bg-gray-100 transition-colors"
                aria-label="Minimize"
              >
                <Minus size={16} />
              </button>
              <button
                onClick={() => setIsOpen(false)}
                className="text-gray-500 hover:text-red-500 focus:outline-none p-1 rounded hover:bg-gray-100 transition-colors"
                aria-label="Close chat"
              >
                <X size={18} />
              </button>
            </div>
          </div>

          {/* Chat Content */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50/30" style={{ scrollbarWidth: 'thin', scrollbarColor: '#d1d5db transparent' }}>
              {messages.length === 0 ? (
                <div className="text-center text-gray-500 mt-8">
                  <p className="text-gray-600">Hello! I'm your AI assistant for managing your todo tasks.</p>
                  <p className="text-gray-500 text-sm">You can add, list, complete, update, or delete tasks using natural language.</p>
                  <div className="mt-4 grid grid-cols-1 gap-2">
                    <button
                      onClick={() => setInputMessage('Add a task to buy groceries')}
                      className="text-xs bg-indigo-100 hover:bg-indigo-200 text-indigo-800 py-1 px-2 rounded-lg transition-colors"
                    >
                      Add a task to buy groceries
                    </button>
                    <button
                      onClick={() => setInputMessage('List my tasks')}
                      className="text-xs bg-indigo-100 hover:bg-indigo-200 text-indigo-800 py-1 px-2 rounded-lg transition-colors"
                    >
                      List my tasks
                    </button>
                    <button
                      onClick={() => setInputMessage('Complete task #1')}
                      className="text-xs bg-indigo-100 hover:bg-indigo-200 text-indigo-800 py-1 px-2 rounded-lg transition-colors"
                    >
                      Complete task #1
                    </button>
                    <button
                      onClick={() => setInputMessage('Update my task description')}
                      className="text-xs bg-indigo-100 hover:bg-indigo-200 text-indigo-800 py-1 px-2 rounded-lg transition-colors"
                    >
                      Update my task description
                    </button>
                  </div>
                </div>
              ) : (
                messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.role === 'user' ? 'justify-end' : message.role === 'system' ? 'justify-center' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[85%] p-3 ${
                        message.role === 'user'
                          ? 'bg-gradient-to-br from-indigo-500 to-indigo-600 text-white rounded-2xl rounded-tr-none'
                          : message.role === 'system'
                            ? 'bg-gray-200/60 text-gray-600 text-xs italic px-3 py-1 rounded-full'
                            : 'bg-gray-100/80 text-gray-800 rounded-2xl rounded-tl-none'
                      }`}
                    >
                      {message.content}
                    </div>
                  </div>
                ))
              )}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100/80 text-gray-800 rounded-2xl rounded-tl-none p-3 max-w-[85%]">
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse"></div>
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse delay-75"></div>
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse delay-150"></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Form */}
            <form onSubmit={handleSubmit} className="border-t border-gray-200/50 p-3 bg-white/50">
              <div className="flex">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  placeholder="Type your message..."
                  className="flex-1 border border-gray-300 rounded-l-lg p-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white/80"
                  disabled={isLoading}
                />
                <button
                  type="submit"
                  disabled={isLoading || !inputMessage.trim()}
                  className="bg-indigo-500 text-white px-4 rounded-r-lg disabled:opacity-50 text-sm hover:bg-indigo-600 transition-colors"
                >
                  Send
                </button>
              </div>
            </form>
          </div>

          {/* Resize Handle */}
          <div
            ref={resizeHandleRef}
            className="absolute bottom-0 right-0 w-4 h-4 cursor-se-resize bg-gray-400/50 hover:bg-gray-500/70 rounded-bl-lg transition-colors"
            onMouseDown={handleResizeMouseDown}
            aria-label="Resize chat window"
          />
        </div>
      )}
    </>
  );
}