import ClientWrapper from '../ClientWrapper'
import { ReactNode } from 'react'

export default function AuthLayout({
  children,
}: {
  children: ReactNode
}) {
  return (
    <ClientWrapper>
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
        {children}
      </div>
    </ClientWrapper>
  )
}