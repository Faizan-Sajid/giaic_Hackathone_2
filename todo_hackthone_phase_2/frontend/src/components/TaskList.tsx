// Task: T041
// Spec: Implementation Plan - Phase 4: User Story 2 - Task Management
// Spec: User Story 2 - Task Management (FR-011: List user's own tasks)
// Implementation: TaskList component displaying user's tasks with title, description, completed status

'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { get, patch, delete as deleteReq, ApiError, HttpStatus } from '../lib/api/client'


/**
 * Task Interface
 *
 * Task: T041
 * Spec: Data Model - Task Entity (data-model.md lines 87-180)
 */
export interface Task {
  id: number;
  owner_user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}


/**
 * TaskList Component Props
 *
 * Task: T041
 */
interface TaskListProps {
  onEdit?: (task: Task) => void;
  onRefresh?: () => void;
}


/**
 * TaskList Component
 *
 * Task: T041
 * Spec: FR-011 (list user's own tasks)
 * FR-015 (toggle task completion)
 * FR-014 (delete task by ID)
 *
 * Features:
 * - Display user's tasks with title, description, completed status
 * - Toggle task completion (T045)
 * - Delete task with confirmation (T046)
 * - Loading states and error handling (T048)
 * - Protected by authentication
 */
export default function TaskList({ onEdit, onRefresh }: TaskListProps) {
  const { user, isLoading: authLoading } = useAuth()
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  /**
   * Load tasks on mount or when user changes
   */
  useEffect(() => {
    loadTasks()
  }, [user])

  /**
   * Load tasks from API
   *
   * Task: T041
   * Spec: FR-011 (list user's own tasks)
   */
  async function loadTasks() {
    if (!user) return

    setIsLoading(true)
    setError(null)

    try {
      const response = await get(`/api/${user.id}/tasks`)

      if (response.data) {
        setTasks(response.data as Task[])
      }
    } catch (error) {
      if (error instanceof ApiError) {
        setError('Failed to load tasks. Please try again.')
      } else {
        setError('Network error. Please check your connection.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  /**
   * Toggle task completion
   *
   * Task: T045
   * Spec: FR-015 (mark task as complete or incomplete)
   */
  async function handleToggleComplete(task: Task) {
    setIsLoading(true)
    setError(null)

    try {
      await patch(`/api/${task.owner_user_id}/tasks/${task.id}/complete`, {})

      // Update local state optimistically
      setTasks(prevTasks =>
        prevTasks.map(t =>
          t.id === task.id ? { ...t, completed: !t.completed } : t
        )
      )

      // Refresh parent component if needed
      if (onRefresh) {
        onRefresh()
      }
    } catch (error) {
      if (error instanceof ApiError) {
        setError('Failed to update task. Please try again.')
      } else {
        setError('Network error. Please check your connection.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  /**
   * Delete task with confirmation
   *
   * Task: T046
   * Spec: FR-014 (delete task by ID)
   */
  async function handleDelete(task: Task) {
    // Check if window is available (client-side only)
    if (typeof window !== 'undefined') {
      const confirmed = window.confirm(
        'Are you sure you want to delete this task?'
      )

      if (!confirmed) return
    }

    setIsLoading(true)
    setError(null)

    try {
      await deleteReq(`/api/${task.owner_user_id}/tasks/${task.id}`)

      // Update local state optimistically
      setTasks(prevTasks => prevTasks.filter(t => t.id !== task.id))

      // Refresh parent component if needed
      if (onRefresh) {
        onRefresh()
      }
    } catch (error) {
      if (error instanceof ApiError) {
        setError('Failed to delete task. Please try again.')
      } else {
        setError('Network error. Please check your connection.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  // Show loading state while checking auth or loading tasks
  if (authLoading || isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-sm text-gray-600">Loading tasks...</p>
        </div>
      </div>
    )
  }

  // Show error state
  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="text-center py-12">
          <svg
            className="mx-auto h-12 w-12 text-red-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">Error</h3>
          <p className="mt-1 text-sm text-gray-500">{error}</p>
          <button
            onClick={loadTasks}
            className="mt-4 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  // Show empty state
  if (tasks.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="text-center py-12">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks yet</h3>
          <p className="mt-1 text-sm text-gray-500">
            Create your first task to get started
          </p>
        </div>
      </div>
    )
  }

  // Show task list
  return (
    <div className="space-y-4">
      {tasks.map(task => (
        <div
          key={task.id}
          className={`bg-white rounded-lg shadow-md p-6 transition-all ${
            task.completed ? 'opacity-60' : ''
          }`}
        >
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-4 flex-1">
              {/* Checkbox */}
              <button
                onClick={() => handleToggleComplete(task)}
                disabled={isLoading}
                className={`mt-1 flex-shrink-0 w-6 h-6 rounded-md border-2 flex items-center justify-center transition-colors ${
                  task.completed
                    ? 'bg-green-500 border-green-500 text-white'
                    : 'border-gray-300 hover:border-blue-500'
                }`}
                aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
              >
                {task.completed && (
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={3}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                )}
              </button>

              {/* Task Content */}
              <div className="flex-1">
                <h3
                  className={`text-lg font-medium ${
                    task.completed ? 'line-through text-gray-500' : 'text-gray-900'
                  }`}
                >
                  {task.title}
                </h3>
                {task.description && (
                  <p
                    className={`mt-1 text-sm ${
                      task.completed ? 'text-gray-400' : 'text-gray-600'
                    }`}
                  >
                    {task.description}
                  </p>
                )}
                <p className="mt-2 text-xs text-gray-500">
                  Created: {new Date(task.created_at).toLocaleString()}
                </p>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex space-x-2 ml-4">
              <button
                onClick={() => onEdit?.(task)}
                disabled={isLoading}
                className="px-3 py-1.5 bg-blue-600 text-white text-sm font-medium rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(task)}
                disabled={isLoading}
                className="px-3 py-1.5 bg-red-600 text-white text-sm font-medium rounded hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
