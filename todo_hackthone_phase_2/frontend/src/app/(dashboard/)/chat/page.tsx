'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '../../../contexts/AuthContext';
import ChatKitComponent from '../../../components/chat/ChatKitComponent';
import ProtectedRoute from '../../../components/ProtectedRoute';

/**
 * Chat Page - Main chat interface for the Todo AI Assistant
 *
 * Task: TASK-013
 * Spec: Implementation of ChatKit UI for natural language todo management
 */
export default function ChatPage() {
  const { user, isLoading } = useAuth();
  const [mounted, setMounted] = useState(false);

  // Ensure component is mounted on client side
  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted || isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4">
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-900">Todo AI Assistant</h1>
            <p className="text-gray-600 mt-2">
              Interact with your AI assistant to manage your tasks using natural language
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            <ChatKitComponent />
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}