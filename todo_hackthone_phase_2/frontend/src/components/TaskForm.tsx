// Task: T042
// Spec: Implementation Plan - Phase 4: User Story 2 - Task Management
// Spec: User Story 2 - Task Management (FR-010: Create task, FR-013: Update task)
// Implementation: TaskForm component for creating and updating tasks with validation

'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { post, put, ApiError, HttpStatus } from '../lib/api/client'


/**
 * Task Interface (from TaskList)
 *
 * Task: T042
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
 * TaskForm Component Props
 *
 * Task: T042
 */
interface TaskFormProps {
  task?: Task | null;  // If provided, form is in edit mode
  onSubmit: () => void;  // Callback after successful submission
  onCancel?: () => void;  // Callback when cancel is clicked
}


/**
 * TaskForm Component
 *
 * Task: T042
 * Spec: FR-010 (create task with title and optional description)
 * FR-013 (update task title and/or description)
 * FR-012 (title minimum 1 character, maximum 200)
 * FR-013 (description maximum 1000 characters)
 *
 * Features:
 * - Create new tasks (T043)
 * - Update existing tasks (T044)
 * - Client-side validation for title and description (T049)
 * - Loading states and error handling (T048)
 * - Protected by authentication
 */
export default function TaskForm({ task, onSubmit, onCancel }: TaskFormProps) {
  const { user } = useAuth()
  const [formData, setFormData] = useState({
    title: '',
    description: ''
  })
  const [errors, setErrors] = useState<{
    title?: string
    description?: string
    general?: string
  }>({})
  const [isLoading, setIsLoading] = useState(false)

  // Initialize form data when task prop changes (edit mode)
  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title,
        description: task.description || ''
      })
    }
  }, [task])

  /**
   * Validate form inputs
   *
   * Task: T049
   * Spec: FR-012 (title minimum 1 character, maximum 200)
   * FR-013 (description maximum 1000 characters)
   */
  const validateForm = (): boolean => {
    const newErrors: typeof errors = {}

    // Title validation: Minimum 1 character, Maximum 200 characters
    if (!formData.title || formData.title.trim().length === 0) {
      newErrors.title = 'Title is required'
    } else if (formData.title.length > 200) {
      newErrors.title = 'Title too long (max 200 characters)'
    }

    // Description validation: Maximum 1000 characters
    if (formData.description && formData.description.length > 1000) {
      newErrors.description = 'Description too long (max 1000 characters)'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  /**
   * Handle form submission
   *
   * Task: T043 (create), T044 (update)
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!user) return

    // Validate form
    if (!validateForm()) {
      return
    }

    setIsLoading(true)
    setErrors({})

    try {
      if (task) {
        // Update existing task (T044)
        const response = await put(`/api/${task.owner_user_id}/tasks/${task.id}`, {
          title: formData.title.trim(),
          description: formData.description.trim() || null
        })

        if (response.data) {
          onSubmit()
        }
      } else {
        // Create new task (T043)
        const response = await post(`/api/${user.id}/tasks`, {
          title: formData.title.trim(),
          description: formData.description.trim() || null
        })

        if (response.data) {
          // Clear form data
          setFormData({ title: '', description: '' })
          onSubmit()
        }
      }
    } catch (error) {
      // Handle API errors (T048)
      if (error instanceof ApiError) {
        switch (error.status) {
          case HttpStatus.BAD_REQUEST:
            setErrors({
              general: 'Invalid input. Please check your task details.'
            })
            break
          case HttpStatus.UNAUTHORIZED:
            setErrors({
              general: 'Please log in to manage tasks.'
            })
            break
          case HttpStatus.FORBIDDEN:
            setErrors({
              general: 'Access denied. You cannot modify other users\' tasks.'
            })
            break
          case HttpStatus.NOT_FOUND:
            setErrors({
              general: 'Task not found. It may have been deleted.'
            })
            break
          case HttpStatus.INTERNAL_SERVER_ERROR:
            setErrors({
              general: 'Server error. Please try again later.'
            })
            break
          default:
            setErrors({
              general: 'An error occurred. Please try again.'
            })
        }
      } else {
        setErrors({
          general: 'Network error. Please check your connection.'
        })
      }
    } finally {
      setIsLoading(false)
    }
  }

  /**
   * Handle input changes
   */
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))

    // Clear error for this field
    setErrors(prev => ({ ...prev, [name]: undefined }))
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Title Field */}
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Title <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.title ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="Enter task title"
          disabled={isLoading}
          maxLength={200}
        />
        <div className="mt-1 flex justify-between text-xs text-gray-500">
          <span>Required</span>
          <span>
            {formData.title.length}/200 characters
          </span>
        </div>
        {errors.title && (
          <p className="mt-1 text-sm text-red-600">{errors.title}</p>
        )}
      </div>

      {/* Description Field */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.description ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="Enter task description (optional)"
          disabled={isLoading}
          rows={4}
          maxLength={1000}
        />
        <div className="mt-1 text-right text-xs text-gray-500">
          {formData.description.length}/1000 characters
        </div>
        {errors.description && (
          <p className="mt-1 text-sm text-red-600">{errors.description}</p>
        )}
      </div>

      {/* General Error Message */}
      {errors.general && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-600">{errors.general}</p>
        </div>
      )}

      {/* Submit and Cancel Buttons */}
      <div className="flex justify-end space-x-3">
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            disabled={isLoading}
            className="px-4 py-2 bg-gray-200 text-gray-700 font-medium rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 disabled:bg-gray-100 disabled:cursor-not-allowed transition-colors"
          >
            Cancel
          </button>
        )}
        <button
          type="submit"
          disabled={isLoading}
          className="px-6 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? 'Saving...' : task ? 'Update Task' : 'Create Task'}
        </button>
      </div>
    </form>
  )
}
