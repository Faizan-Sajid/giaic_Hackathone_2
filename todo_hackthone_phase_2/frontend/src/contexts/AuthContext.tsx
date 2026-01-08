// # AuthContext Provider
// # Task: T019
// # Spec: Implementation Plan - Phase 2.5 Frontend Foundation

'use client'

import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { get, post } from '../lib/api/client'
import { ApiError } from '../lib/api/client'


/**
 * User Interface (from spec.md data-model.md)
 */
export interface User {
  id: string;
  email: string;
}


/**
 * Session Interface
 * Provides session state and refresh functionality
 *
 * Task: T019
 * Spec: FR-008 (create task), FR-009 (list user's own tasks)
 */
export interface Session {
  user: User | null;
  isLoading: boolean;
  refresh: () => Promise<void>;
  logout: () => Promise<void>;
}


/**
 * Auth Context Type
 */
interface AuthContextType extends Session {
  login: (user: User) => void;
  setUser: (user: User | null) => void;
}


/**
 * Create Auth Context
 */
const AuthContext = createContext<AuthContextType | undefined>(undefined);


/**
 * AuthProvider Component
 *
 * Task: T019
 * Spec: Implementation Plan - Phase 2.5 Frontend Foundation
 * Implementation: React Context API for session state
 *
 * Features:
 * - Provides global auth state accessible by all components
 * - Session data: user, isLoading, refresh function, logout function
 * - NEVER stores JWT in localStorage (security requirement)
 * - JWT is in HTTP-only cookies only (handled by backend)
 * - Automatic session loading on mount
 */
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const [session, setSession] = useState<Session>({
    user: null,
    isLoading: true,
    refresh: async () => { /* Will be updated after initial load */ },
    logout: async () => { /* Will be updated after initial load */ }
  });

  // Define stable functions inside the component to avoid hook rule violations
  const refreshSession = useCallback(async () => {
    await loadSession();
  }, []);

  const logoutUser = useCallback(async () => {
    try {
      // Call logout API to clear HTTP-only cookie
      await post('/api/auth/logout', {});
    } catch (error) {
      console.error('Logout failed:', error);
      // Continue with local logout even if API fails
    } finally {
      // Clear local session state
      setSession(prev => ({
        ...prev,
        user: null,
        isLoading: false,
        refresh: refreshSession,
        logout: logoutUser
      }));

      // Redirect to login page
      router.push('/login');
    }
  }, [router, refreshSession]);

  const login = useCallback((user: User) => {
    setSession(prev => ({
      ...prev,
      user: user,
      isLoading: false,
      refresh: refreshSession,
      logout: logoutUser
    }));
  }, [refreshSession, logoutUser]);

  const setUser = useCallback((user: User | null) => {
    setSession(prev => ({
      ...prev,
      user: user,
      isLoading: false,
      refresh: refreshSession,
      logout: logoutUser
    }));
  }, [refreshSession, logoutUser]);


  /**
   * Fetch session from /api/auth/session
   * Checks if user is authenticated via HTTP-only JWT cookie
   */
  async function loadSession(): Promise<{ user: User | null, authenticated: boolean }> {
    console.log('LOADING SESSION...');
    try {
      // Always set loading to true when starting the session load
      setSession(prev => ({ ...prev, isLoading: true }));

      const response = await get('/api/auth/session');
      console.log('SESSION DATA:', response);

      if (response.data) {
        const responseData = response.data as { user: User | null; authenticated: boolean };
        if (responseData && responseData.authenticated) {
          const userData = responseData.user || null;
          console.log('SESSION VALID - USER DATA:', userData);
          // Atomic state update: user and isLoading: false in the same call
          setSession(prev => ({
            ...prev,
            user: userData,
            isLoading: false,
            refresh: refreshSession,
            logout: logoutUser
          }));
          return { user: userData, authenticated: true };
        } else {
          console.log('SESSION NOT AUTHENTICATED');
          // Atomic state update: user and isLoading: false in the same call
          setSession(prev => ({
            ...prev,
            user: null,
            isLoading: false,
            refresh: refreshSession,
            logout: logoutUser
          }));
          return { user: null, authenticated: false };
        }
      } else {
        console.log('SESSION NOT AUTHENTICATED - NO DATA');
        // Atomic state update: user and isLoading: false in the same call
        setSession(prev => ({
          ...prev,
          user: null,
          isLoading: false,
          refresh: refreshSession,
          logout: logoutUser
        }));
        return { user: null, authenticated: false };
      }
    } catch (error) {
      console.log('SESSION LOAD ERROR:', error);
      // Handle 401 as "not authenticated", not an error
      if (error instanceof ApiError && error.status === 401) {
        // Atomic state update: user and isLoading: false in the same call
        setSession({
          user: null,
          isLoading: false,
          refresh: refreshSession,
          logout: logoutUser
        });
        return { user: null, authenticated: false };
      } else {
        // For network errors and other issues, still set user: null but log appropriately
        if (error instanceof TypeError && error.message.includes('fetch')) {
          // This is likely a network error - atomic state update
          setSession({
            user: null,
            isLoading: false,
            refresh: refreshSession,
            logout: logoutUser
          });
        } else {
          console.error('Failed to load session:', error);
          // Atomic state update: user and isLoading: false in the same call
          setSession(prev => ({
            ...prev,
            user: null,
            isLoading: false,
            refresh: refreshSession,
            logout: logoutUser
          }));
        }
        return { user: null, authenticated: false };
      }
    }
  }

  useEffect(() => {
    // Load session on mount
    loadSession();
  }, []); // Run once on mount

  return (
    <AuthContext.Provider value={{
      ...session,
      login,
      setUser,
      refresh: refreshSession,
      logout: logoutUser
    }}>
      {children}
    </AuthContext.Provider>
  );
}


/**
 * Hook to use Auth Context
 *
 * Usage:
 * const { user, isLoading, refresh, logout } = useAuth();
 *
 * Task: T019
 */
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider');
  }

  return context;
}

