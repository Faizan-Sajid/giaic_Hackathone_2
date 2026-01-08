// Task: T030
// Spec: Implementation Plan - Phase 2.2 Authentication Implementation
// Spec: User Story 1 - Authentication (FR-003: User Login)
// Implementation: Login form component with validation

'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { post, ApiError, HttpStatus, User } from '../../lib/api/client'
import { useAuth } from '../../contexts/AuthContext'


/**
 * Login Form Component
 *
 * Task: T030
 * Spec: FR-003 (login with email and password)
 * FR-004 (JWT token issuance on successful authentication)
 * SEC-002 (JWT in HTTP-only cookies)
 *
 * Features:
 * - Email and password input
 * - Loading state
 * - Error handling with user-friendly messages
 * - Redirects to tasks page on success
 * - Refreshes auth context on success
 * - NEVER stores JWT in localStorage
 */
export default function LoginForm() {
  const router = useRouter()
  const { login } = useAuth()
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [errors, setErrors] = useState<{
    email?: string
    password?: string
    general?: string
  }>({})
  const [isLoading, setIsLoading] = useState(false)

  /**
   * Validate form inputs
   */
  const validateForm = (): boolean => {
    const newErrors: typeof errors = {}

    // Email validation
    if (!formData.email) {
      newErrors.email = 'Email is required'
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Invalid email format'
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  /**
   * Handle form submission
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // Validate form
    if (!validateForm()) {
      return
    }

    setIsLoading(true)
    setErrors({})

    try {
      // Call login API
      const response = await post('/api/auth/login', {
        email: formData.email,
        password: formData.password
      })

      console.log('=== LOGIN DEBUG ===');
      console.log('Response object:', response);
      console.log('Response.data:', response.data);
      console.log('Type of response:', typeof response);
      console.log('Type of response.data:', typeof response.data);
      console.log('Keys in response:', Object.keys(response));

      // Handle response with proper typing
      const responseData = response.data;

      // Type guard to check if response data has the expected structure
      if (responseData && typeof responseData === 'object' && 'id' in responseData && 'email' in responseData) {
        console.log("Login successful, setting user in context...");
        console.log('FULL RESPONSE:', response);

        // Extract user data based on backend response structure
        const userData: User = {
          id: (responseData as any).id as string,
          email: (responseData as any).email as string
        };

        console.log('EXTRACTED USER DATA:', userData);
        login(userData); // Set user in context immediately
        console.log('USER CONTEXT UPDATED');
        console.log('ABOUT TO REDIRECT TO /dashboard');

        // Add small delay to allow browser to settle the cookie
        setTimeout(() => {
          // Use window.location.assign('/dashboard') instead of router.push
          window.location.assign('/dashboard'); // Force a hard browser refresh
        }, 300);
      } else {
        console.error('Login response data is missing required fields');
        console.error('Full response was:', response);
        setErrors({
          general: 'Login failed: invalid response from server'
        });
      }
    } catch (error) {
      // Handle API errors
      if (error instanceof ApiError) {
        switch (error.status) {
          case HttpStatus.BAD_REQUEST:
            setErrors({
              general: 'Invalid input. Please check your email and password.'
            })
            break
          case HttpStatus.UNAUTHORIZED:
            setErrors({
              general: 'Invalid email or password'
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
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))

    // Clear error for this field
    setErrors(prev => ({ ...prev, [name]: undefined }))
  }

  return (
    <div className="w-full max-w-md">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-xl shadow-lg space-y-6">
        {/* Header */}
        <div className="text-center">
          <div className="mx-auto h-16 w-16 rounded-full bg-blue-100 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h2 className="mt-4 text-2xl font-bold text-gray-900">Welcome back</h2>
          <p className="mt-1 text-sm text-gray-600">Sign in to your account</p>
        </div>

        {/* Email Field */}
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
            Email address
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
              errors.email ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="Enter your email"
            disabled={isLoading}
            autoComplete="email"
          />
          {errors.email && (
            <p className="mt-1 text-sm text-red-600 flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {errors.email}
            </p>
          )}
        </div>

        {/* Password Field */}
        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
            Password
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
              errors.password ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="Enter your password"
            disabled={isLoading}
            autoComplete="current-password"
          />
          {errors.password && (
            <p className="mt-1 text-sm text-red-600 flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {errors.password}
            </p>
          )}
        </div>

        {/* Remember Me & Forgot Password */}
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <input
              id="remember-me"
              name="remember-me"
              type="checkbox"
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-700">
              Remember me
            </label>
          </div>
          <div className="text-sm">
            <a href="#" className="font-medium text-blue-600 hover:text-blue-500">
              Forgot your password?
            </a>
          </div>
        </div>

        {/* General Error Message */}
        {errors.general && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16zM8.707 7.293a1 1 0 0 0-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 1 0 1.414 1.414L10 11.414l1.293 1.293a1 1 0 0 0 1.414-1.414L11.414 10l1.293-1.293a1 1 0 0 0-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">{errors.general}</h3>
              </div>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-3 px-4 rounded-lg hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-[1.02]"
        >
          {isLoading ? (
            <div className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Signing in...
            </div>
          ) : (
            <span className="flex items-center justify-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
              </svg>
              Sign in to your account
            </span>
          )}
        </button>

        {/* Sign up link */}
        <div className="text-center text-sm text-gray-600">
          Don't have an account?{' '}
          <a href="/register" className="font-medium text-blue-600 hover:text-blue-500">
            Sign up
          </a>
        </div>
      </form>
    </div>
  )
}