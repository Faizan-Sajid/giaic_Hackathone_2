import ClientWrapper from '../ClientWrapper'
import { ReactNode } from 'react'

export default function DashboardLayout({
  children,
}: {
  children: ReactNode
}) {
  return (
    <ClientWrapper>
      {children}
    </ClientWrapper>
  )
}