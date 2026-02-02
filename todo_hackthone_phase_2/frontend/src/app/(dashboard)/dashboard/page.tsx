// Task: T031
// Spec: Implementation Plan - Phase 2.2 Authentication Implementation
// Spec: User Story 1 - Authentication (FR-017: Invalidate JWT on logout)
// Implementation: Dashboard page with logout functionality

'use client'

import { useState, useEffect } from 'react';
import { useAuth } from '../../../contexts/AuthContext'
import ProtectedRoute from '../../../components/ProtectedRoute'
import { get } from '../../../lib/api/client';

/**
 * Task Interface
 */
interface Task {
  id: number;
  owner_user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}


/**
 * Dashboard Page
 *
 * Task: T031
 * Spec: FR-017 (invalidate JWT on logout)
 * SEC-002 (JWT in HTTP-only cookies)
 *
 * Features:
 * - Display user info
 * - Logout button calling POST /api/auth/logout
 * - Redirects to login page on logout
 * - Protected by authentication
 * - NEVER stores JWT in localStorage
 */
export default function DashboardPage() {
  console.log('DASHBOARD PAGE IS RENDERING');
  const { user, logout } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Calculate stats dynamically
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(t => t.completed).length;
  const pendingTasks = tasks.filter(t => !t.completed).length;

  /**
   * Fetch tasks from the API
   */
  const fetchTasks = async (showLoading = false) => {
    if (user) {
      if (showLoading) {
        setIsLoading(true);
      }
      try {
        const response = await get(`/api/${user.id}/tasks`);
        if (response.data) {
          setTasks(response.data as Task[]);
        }
      } catch (error) {
        console.error('Failed to fetch tasks:', error);
      } finally {
        if (showLoading) {
          setIsLoading(false);
        }
      }
    }
  };

  useEffect(() => {
    // Initial fetch with loading state
    fetchTasks(true);

    // Set up polling to refresh tasks every 5 seconds
    const intervalId = setInterval(() => fetchTasks(), 5000);

    // Listen for task update events from chatbot
    const handleTaskUpdate = () => {
      fetchTasks(); // Refresh immediately when tasks are updated via chatbot
    };

    window.addEventListener('tasksUpdated', handleTaskUpdate);

    // Clean up interval and event listener on component unmount
    return () => {
      clearInterval(intervalId);
      window.removeEventListener('tasksUpdated', handleTaskUpdate);
    };
  }, [user]);

  /**
   * Handle logout
   *
   * Task: T031
   * Spec: FR-017 (invalidate JWT on logout)
   *
   * - Calls POST /api/auth/logout to clear HTTP-only JWT cookie
   * - Redirects to login page
   */
  const handleLogout = async () => {
    await logout()
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-zinc-950 text-white">
        {/* Header */}
        <header className="bg-zinc-900 border-b border-zinc-800">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <div className="h-10 w-10 rounded-lg bg-gradient-to-r from-sky-500 to-sky-600 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-sky-400 to-sky-500 bg-clip-text text-transparent">TaskFlow</h1>
                <p className="text-sm text-zinc-400">Your personal task manager</p>
              </div>
            </div>

            {/* User Info and Logout */}
            <div className="flex items-center space-x-4">
              {user && (
                <div className="text-sm text-zinc-300">
                  <span className="font-medium">{user.email}</span>
                </div>
              )}
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-gradient-to-r from-red-500 to-pink-500 text-white text-sm font-medium rounded-lg hover:from-red-600 hover:to-pink-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:ring-offset-zinc-900 transition-all duration-200"
              >
                Sign out
              </button>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Welcome Section */}
          <div className="bg-zinc-900 rounded-2xl p-8 mb-8 border border-zinc-800">
            <div className="flex items-center space-x-4">
              <div className="h-16 w-16 rounded-full bg-gradient-to-r from-sky-500 to-sky-600 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">
                  Welcome back, <span className="text-sky-400">{user?.email?.split('@')[0]}</span>!
                </h2>
                <p className="text-zinc-400 mt-1">
                  Ready to tackle your tasks and boost your productivity?
                </p>
              </div>
            </div>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-zinc-900 rounded-xl p-6 border border-zinc-800 hover:shadow-[0_0_15px_rgba(56,189,248,0.2)] hover:border-sky-500/50 transition-all duration-300">
              <div className="flex items-center">
                <div className="h-12 w-12 rounded-lg bg-sky-500/20 flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-sky-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-zinc-400">Total Tasks</p>
                  <p className="text-2xl font-bold text-white">{totalTasks}</p>
                </div>
              </div>
            </div>

            <div className="bg-zinc-900 rounded-xl p-6 border border-zinc-800 hover:shadow-[0_0_15px_rgba(56,189,248,0.2)] hover:border-sky-500/50 transition-all duration-300">
              <div className="flex items-center">
                <div className="h-12 w-12 rounded-lg bg-green-500/20 flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-zinc-400">Completed</p>
                  <p className="text-2xl font-bold text-white">{completedTasks}</p>
                </div>
              </div>
            </div>

            <div className="bg-zinc-900 rounded-xl p-6 border border-zinc-800 hover:shadow-[0_0_15px_rgba(56,189,248,0.2)] hover:border-sky-500/50 transition-all duration-300">
              <div className="flex items-center">
                <div className="h-12 w-12 rounded-lg bg-yellow-500/20 flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-zinc-400">Pending</p>
                  <p className="text-2xl font-bold text-white">{pendingTasks}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-zinc-900 rounded-2xl p-8 border border-zinc-800">
            <div className="text-center">
              <h3 className="text-xl font-semibold text-white mb-4">Ready to get started?</h3>
              <p className="text-zinc-400 mb-6">
                Manage your tasks efficiently with our powerful task management system.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <a
                  href="/tasks"
                  className="px-6 py-3 bg-gradient-to-r from-sky-500 to-sky-600 text-white font-medium rounded-lg hover:from-sky-600 hover:to-sky-700 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-offset-2 focus:ring-offset-zinc-900 transition-all duration-200"
                >
                  View Tasks
                </a>
                <a
                  href="/tasks"
                  className="px-6 py-3 bg-gradient-to-r from-sky-500 to-sky-600 text-white font-medium rounded-lg hover:from-sky-600 hover:to-sky-700 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-offset-2 focus:ring-offset-zinc-900 transition-all duration-200"
                >
                  <div className="flex items-center justify-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                    Add New Task
                  </div>
                </a>
              </div>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  )
}
