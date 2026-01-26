'use client';

import { useAuth } from '../../../contexts/AuthContext';

/**
 * Chat Page - Main chat interface for the Todo AI Chatbot
 *
 * Task: TASK-013
 * Spec: Implements Custom Resizable Floating Chatbot that connects to the chat API
 */
export default function ChatPage() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Todo AI Assistant</h1>
          <p className="text-gray-600">Chat with your AI assistant to manage your todo tasks</p>
        </div>

        <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-6">
          <div className="text-center py-12">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Your AI Assistant is Available</h2>
            <p className="text-gray-600 mb-6">
              The AI assistant is now available as a floating chatbot that stays with you across all pages.
            </p>
            <div className="inline-flex items-center justify-center bg-blue-50 rounded-lg p-4">
              <div className="bg-blue-600 text-white p-3 rounded-full mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
              <p className="text-blue-800">Look for the chat bubble in the bottom-right corner!</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}