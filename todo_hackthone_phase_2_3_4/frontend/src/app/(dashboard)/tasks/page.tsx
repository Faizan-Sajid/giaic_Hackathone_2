// Task: T047
// Spec: Implementation Plan - Phase 4: User Story 2 - Task Management
// Spec: User Story 2 - Task Management (FR-011: List user's own tasks, FR-010: Create task)
// Implementation: Tasks page UI with ProtectedRoute, TaskList, and TaskForm

'use client'

import { useState } from 'react'
import { useAuth } from '../../../contexts/AuthContext'
import ProtectedRoute from '../../../components/ProtectedRoute'
import TaskList, { Task } from '../../../components/TaskList'
import TaskForm from '../../../components/TaskForm'


/**
 * Tasks Page
 *
 * Task: T047
 * Spec: FR-010 (create task)
 * FR-011 (list user's own tasks)
 * FR-014 (delete task by ID)
 * FR-015 (toggle task completion)
 *
 * Features:
 * - Display user's tasks with TaskList
 * - Create new tasks with TaskForm
 * - Edit existing tasks
 * - Delete tasks with confirmation
 * - Toggle task completion
 * - Protected by authentication
 * - Client-side validation for title and description (T049)
 * - Loading states and error handling (T048)
 */
export default function TasksPage() {
  const { user } = useAuth()
  const [isCreating, setIsCreating] = useState(false)
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [refreshKey, setRefreshKey] = useState(0)

  /**
   * Refresh task list after operations
   */
  function handleRefresh() {
    setRefreshKey(prev => prev + 1)
  }

  /**
   * Handle create task mode
   */
  function handleCreateClick() {
    setEditingTask(null)
    setIsCreating(true)
  }

  /**
   * Handle edit task mode
   */
  function handleEditClick(task: Task) {
    setIsCreating(false)
    setEditingTask(task)
  }

  /**
   * Handle form submission (create or update)
   */
  function handleFormSubmit() {
    setIsCreating(false)
    setEditingTask(null)
    handleRefresh()
  }

  /**
   * Handle form cancel
   */
  function handleFormCancel() {
    setIsCreating(false)
    setEditingTask(null)
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-zinc-950 text-white">
        {/* Header */}
        <header className="bg-zinc-900 border-b border-zinc-800">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-sky-400 to-sky-500 bg-clip-text text-transparent">TaskFlow</h1>
              <p className="text-sm text-zinc-400">Your personal task manager</p>
            </div>

            {/* User Info and Dashboard Link */}
            <div className="flex items-center space-x-4">
              <a
                href="/dashboard"
                className="px-4 py-2 text-sky-400 hover:text-sky-300 font-medium transition-colors rounded-lg border border-zinc-700 hover:border-sky-500/50"
              >
                Dashboard
              </a>
              {user && (
                <div className="text-sm text-zinc-300">
                  <span className="font-medium">{user.email}</span>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Page Title and Actions */}
          <div className="flex justify-between items-center mb-6">
            <div>
              <h2 className="text-2xl font-bold text-white">My Tasks</h2>
              <p className="text-sm text-zinc-400 mt-1">
                Manage your personal task list
              </p>
            </div>

            {!isCreating && !editingTask && (
              <button
                onClick={handleCreateClick}
                className="px-6 py-2 bg-gradient-to-r from-sky-500 to-sky-600 text-white font-medium rounded-lg hover:from-sky-600 hover:to-sky-700 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-offset-2 focus:ring-offset-zinc-900 transition-all duration-200"
              >
                + New Task
              </button>
            )}
          </div>

          {/* Task Form (Create or Edit) */}
          {(isCreating || editingTask) && (
            <div className="bg-zinc-900 rounded-lg border border-zinc-800 p-6 mb-6 hover:shadow-[0_0_15px_rgba(56,189,248,0.2)] transition-all duration-300">
              <h3 className="text-lg font-semibold text-white mb-4">
                {editingTask ? 'Edit Task' : 'Create New Task'}
              </h3>
              <TaskForm
                task={editingTask}
                onSubmit={handleFormSubmit}
                onCancel={handleFormCancel}
              />
            </div>
          )}

          {/* Task List */}
          <div key={refreshKey}>
            <TaskList
              onEdit={handleEditClick}
              onRefresh={handleRefresh}
            />
          </div>
        </main>
      </div>
    </ProtectedRoute>
  )
}
