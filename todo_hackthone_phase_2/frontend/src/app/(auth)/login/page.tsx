// Task: T028
// Spec: Implementation Plan - Phase 2.2 Authentication Implementation
// Spec: User Story 1 - Authentication (FR-003: User Login)
// Implementation: Login page

'use client'

import { Suspense } from 'react'
import { useSearchParams } from 'next/navigation'
import Link from 'next/link'
import LoginForm from '../../../components/auth/LoginForm'


/**
 * Login Content - Wrapped component that uses useSearchParams
 *
 * This component uses useSearchParams() which requires Suspense boundary
 */
function LoginContent() {
  const searchParams = useSearchParams()
  const registered = searchParams.get('registered') === 'true'

  return (
    <div className="max-w-md w-full space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900">
          Sign in to your account
        </h1>
        <p className="mt-2 text-sm text-gray-600">
          Welcome back to TaskFlow
        </p>
      </div>

      {/* Registration Success Message */}
      {registered && (
        <div className="bg-green-50 border border-green-200 rounded-md p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg
                className="h-5 w-5 text-green-400"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-green-800">
                Account created successfully! Please sign in.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Login Form Card */}
      <div className="bg-white p-8 rounded-lg shadow-md">
        <LoginForm />

        {/* Link to Register */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Don't have an account?{' '}
            <Link
              href="/register"
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              Create account
            </Link>
          </p>
        </div>
      </div>

      {/* Footer */}
      <div className="text-center text-xs text-gray-500">
        <p>By signing in, you agree to our Terms of Service</p>
      </div>
    </div>
  )
}

/**
 * Login Page
 *
 * Task: T028
 * Spec: FR-003 (login with email and password)
 * FR-004 (JWT token issuance on successful authentication)
 *
 * Features:
 * - Login form
 * - Link to registration page
 * - Success message for new registrations
 * - User-friendly layout
 * - NEVER stores JWT in localStorage
 *
 * Uses Suspense boundary to allow useSearchParams() in LoginContent
 */
export default function LoginPage() {
  return (
    <Suspense fallback={<div className="max-w-md w-full text-center py-8">Loading...</div>}>
      <LoginContent />
    </Suspense>
  )
}
