// # ProtectedRoute Component
// # Task: T020
// # Spec: Implementation Plan - Phase 2.5 Frontend Foundation

'use client'

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../contexts/AuthContext';


/**
 * ProtectedRoute Props
 */
interface ProtectedRouteProps {
  children: React.ReactNode;
}


/**
 * ProtectedRoute Component
 *
 * Task: T020
 * Spec: FR-005 (extract and validate user_id from JWT)
 * Spec: FR-006 (require valid JWT for protected endpoints)
 * Implementation: Auth-gated page wrapper
 *
 * Features:
 * - Check auth state before rendering children
 * - Redirect to /login if not authenticated
 * - Show loading spinner while checking session
 * - Protects pages requiring authentication
 *
 * Security Requirements Met:
 * - JWT tokens stored in HTTP-only cookies only (not in localStorage)
 * - Automatic redirect for unauthenticated users
 * - Loading state prevents content flash
 */
export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  console.log('PROTECTED ROUTE - Loading:', isLoading, 'User:', user);

  useEffect(() => {
    // Redirect immediately if not authenticated and loading is complete
    if (!isLoading && !user) {
      console.log('PROTECTED ROUTE - Redirecting to login because no user and not loading');
      router.replace('/login');
    } else if (isLoading) {
      console.log('PROTECTED ROUTE - Still loading, not redirecting');
    } else if (user) {
      console.log('PROTECTED ROUTE - User is authenticated, showing children');
    }
  }, [isLoading, user, router]);

  /**
   * Show loading spinner while checking session
   */
  if (isLoading) {
    console.log('PROTECTED ROUTE - Showing loading spinner');
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 border-t-transparent border-l-transparent"></div>
        <span className="ml-3">Loading...</span>
      </div>
    );
  }

  /**
   * Show children if authenticated
   */
  if (!user) {
    console.log('PROTECTED ROUTE - No user, returning null');
    return null; // Will redirect due to effect above
  }

  console.log('PROTECTED ROUTE - Rendering children');
  return <>{children}</>;
}
