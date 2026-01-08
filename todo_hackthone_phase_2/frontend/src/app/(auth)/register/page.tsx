// Task: T027
// Spec: Implementation Plan - Phase 2.2 Authentication Implementation
// Spec: User Story 1 - Authentication (FR-001: User Registration)
// Implementation: Registration page

'use client'

import Link from 'next/link'
import RegisterForm from '../../../components/auth/RegisterForm'


/**
 * Registration Page
 *
 * Task: T027
 * Spec: FR-001 (user registration with email and password)
 * FR-005 (password minimum 8 characters)
 * FR-016 (prevent duplicate email)
 *
 * Features:
 * - Registration form
 * - Link to login page
 * - User-friendly layout
 * - NEVER stores JWT in localStorage
 */
export default function RegisterPage() {
  return (
    <div className="max-w-md w-full space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900">
          Create your account
        </h1>
        <p className="mt-2 text-sm text-gray-600">
          Join TaskFlow to manage your tasks efficiently
        </p>
      </div>

      {/* Registration Form Card */}
      <div className="bg-white p-8 rounded-lg shadow-md">
        <RegisterForm />

          {/* Link to Login */}
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Already have an account?{' '}
              <Link
                href="/login"
                className="font-medium text-blue-600 hover:text-blue-500"
              >
                Sign in
              </Link>
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-xs text-gray-500">
          <p>Your data is secure and encrypted</p>
        </div>
      </div>
    // </div>
  )
}
