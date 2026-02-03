'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '../contexts/AuthContext'

export default function HomePageClient() {
  const { user, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading) {
      if (user) {
        // If user is authenticated, redirect to dashboard
        router.replace('/dashboard') // Use replace to prevent back navigation
      } else {
        // If user is not authenticated, redirect to login
        router.replace('/login') // Use replace to prevent back navigation
      }
    }
  }, [user, isLoading, router])

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
        <p className="text-gray-600">Loading...</p>
      </div>
    </div>
  )
}