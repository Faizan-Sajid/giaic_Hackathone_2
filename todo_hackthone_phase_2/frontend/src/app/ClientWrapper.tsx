'use client'

import { AuthProvider } from '../contexts/AuthContext'
import { ReactNode } from 'react'
import FloatingChatbot from '../components/chat/FloatingChatbot'

export default function ClientWrapper({ children }: { children: ReactNode }) {
  return (
    <AuthProvider>
      {children}
      <FloatingChatbot />
    </AuthProvider>
  )
}