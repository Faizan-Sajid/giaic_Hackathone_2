import { ReactNode } from 'react'
import './globals.css'

export const metadata = {
  title: 'TaskFlow AI',
  description: 'AI-Powered Task Management System',
}

export default function RootLayout({
  children,
}: {
  children: ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        {children}
      </body>
    </html>
  )
}