// Task: T018
// Spec: Implementation Plan - Phase 2.5 Frontend Foundation
// Implementation: API client utility with cookie support

/**
 * API Client Utility
 *
 * Task: T018
 * Spec: FR-008 (create task), FR-009 (list user's own tasks)
 * Implementation: HTTP client with credentials support and error handling
 *
 * Features:
 * - Automatic cookie inclusion (for JWT tokens)
 * - Type-safe request/response interfaces
 * - Error handling for common HTTP status codes
 * - Automatic correlation ID generation
 * - User-friendly error messages
 */

// API Base URL from environment
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';


/**
 * HTTP Status Codes for API responses
 */
enum HttpStatus {
  OK = 200,
  CREATED = 201,
  BAD_REQUEST = 400,
  UNAUTHORIZED = 401,
  FORBIDDEN = 403,
  NOT_FOUND = 404,
  CONFLICT = 409,
  INTERNAL_SERVER_ERROR = 500,
}


/**
 * Standard API Response structure
 */
interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  correlation_id?: string;
}


/**
 * Task Interface (from spec.md data-model.md)
 */
export interface Task {
  id: number;
  owner_user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}


/**
 * User Interface (from spec.md data-model.md)
 */
export interface User {
  id: string;
  email: string;
}


/**
 * Session Interface (from auth endpoints)
 */
export interface Session {
  user: User | null;
  authenticated: boolean;
}


/**
 * Generate correlation ID for request tracing
 */
function generateCorrelationId(): string {
  return `req-${Date.now()}-${Math.random().toString(36).substring(2, 15)}`;
}


/**
 * API Error class for handling HTTP errors
 */
class ApiError extends Error {
  status: number;
  correlationId: string;

  constructor(message: string, status: number, correlationId: string) {
    super(message);
    this.status = status;
    this.correlationId = correlationId;
  }
}


/**
 * Handle API errors and return user-friendly messages
 */
function handleApiError(
  response: Response,
  correlationId: string
): ApiError {
  const status = response.status;

  let message = 'An error occurred';

  // Map HTTP status codes to user-friendly messages
  switch (status) {
    case HttpStatus.BAD_REQUEST:
      message = 'Invalid input';
      break;
    case HttpStatus.UNAUTHORIZED:
      message = 'Please log in to continue';
      break;
    case HttpStatus.FORBIDDEN:
      message = 'Access denied';
      break;
    case HttpStatus.NOT_FOUND:
      message = 'Resource not found';
      break;
    case HttpStatus.CONFLICT:
      message = 'Resource conflict (duplicate email, etc.)';
      break;
    case HttpStatus.INTERNAL_SERVER_ERROR:
      message = 'Server error. Please try again later.';
      break;
    default:
      message = `Request failed with status ${status}`;
  }

  return new ApiError(message, status, correlationId);
}


/**
 * Generic GET request
 */
async function get<T>(
  endpoint: string,
  userId?: string
): Promise<ApiResponse<T>> {
  const correlationId = generateCorrelationId();
  const url = `${API_BASE_URL}${endpoint}`;

  console.log(`[GET] ${url}`, { correlationId });

  try {
    const response = await fetch(url, {
      method: 'GET',
      credentials: 'include', // CRITICAL: Include HTTP-only cookies
      headers: {
        'Content-Type': 'application/json',
        'X-Correlation-ID': correlationId,
      },
    });

    if (!response.ok) {
      // Special handling for session endpoint to return proper data instead of throwing
      if (endpoint === '/api/auth/session' && response.status === 401) {
        const result: ApiResponse<T> = {
          data: { user: null, authenticated: false } as any,
          correlation_id: correlationId
        };
        console.log(`[GET] ${endpoint} returned 401 - not authenticated`, { correlationId, status: response.status });
        return result;
      }
      throw handleApiError(response, correlationId);
    }

    const responseData = await response.json();

    // Wrap the response data in the ApiResponse structure
    const result: ApiResponse<T> = {
      data: responseData,
      correlation_id: correlationId
    };

    console.log(`[GET] Success: ${endpoint}`, { correlationId, status: response.status });

    return result;
  } catch (error) {
    console.error(`[GET] Error: ${endpoint}`, { correlationId, error });
    throw error instanceof ApiError ? error : new ApiError('Network error', HttpStatus.INTERNAL_SERVER_ERROR, correlationId);
  }
}


/**
 * Generic POST request
 */
async function post<T>(
  endpoint: string,
  body: any,
  userId?: string
): Promise<ApiResponse<T>> {
  const correlationId = generateCorrelationId();
  const url = `${API_BASE_URL}${endpoint}`;

  console.log(`[POST] ${url}`, { correlationId, body });

  try {
    const response = await fetch(url, {
      method: 'POST',
      credentials: 'include', // CRITICAL: Include HTTP-only cookies
      headers: {
        'Content-Type': 'application/json',
        'X-Correlation-ID': correlationId,
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw handleApiError(response, correlationId);
    }

    const responseData = await response.json();

    // Wrap the response data in the ApiResponse structure
    const result: ApiResponse<T> = {
      data: responseData,
      correlation_id: correlationId
    };

    console.log(`[POST] Success: ${endpoint}`, { correlationId, status: response.status });

    return result;
  } catch (error) {
    console.error('[POST] Error:', endpoint, { correlationId, error });
    throw error instanceof ApiError ? error : new ApiError('Network error', HttpStatus.INTERNAL_SERVER_ERROR, correlationId);
  }
}


/**
 * Generic PUT request
 */
async function put<T>(
  endpoint: string,
  body: any,
  userId?: string
): Promise<ApiResponse<T>> {
  const correlationId = generateCorrelationId();
  const url = `${API_BASE_URL}${endpoint}`;

  console.log(`[PUT] ${url}`, { correlationId, body });

  try {
    const response = await fetch(url, {
      method: 'PUT',
      credentials: 'include', // CRITICAL: Include HTTP-only cookies
      headers: {
        'Content-Type': 'application/json',
        'X-Correlation-ID': correlationId,
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw handleApiError(response, correlationId);
    }

    const responseData = await response.json();

    // Wrap the response data in the ApiResponse structure
    const result: ApiResponse<T> = {
      data: responseData,
      correlation_id: correlationId
    };

    console.log(`[PUT] Success: ${endpoint}`, { correlationId, status: response.status });

    return result;
  } catch (error) {
    console.error(`[PUT] Error: ${endpoint}`, { correlationId, error });
    throw error instanceof ApiError ? error : new ApiError('Network error', HttpStatus.INTERNAL_SERVER_ERROR, correlationId);
  }
}


/**
 * Generic DELETE request
 */
async function del<T>(
  endpoint: string,
  userId?: string
): Promise<ApiResponse<T>> {
  const correlationId = generateCorrelationId();
  const url = `${API_BASE_URL}${endpoint}`;

  console.log(`[DELETE] ${url}`, { correlationId });

  try {
    const response = await fetch(url, {
      method: 'DELETE',
      credentials: 'include', // CRITICAL: Include HTTP-only cookies
      headers: {
        'X-Correlation-ID': correlationId,
      },
    });

    if (!response.ok) {
      throw handleApiError(response, correlationId);
    }

    const responseData = await response.json();

    // Wrap the response data in the ApiResponse structure
    const result: ApiResponse<T> = {
      data: responseData,
      correlation_id: correlationId
    };

    console.log(`[DELETE] Success: ${endpoint}`, { correlationId, status: response.status });

    return result;
  } catch (error) {
    console.error(`[DELETE] Error: ${endpoint}`, { correlationId, error });
    throw error instanceof ApiError ? error : new ApiError('Network error', HttpStatus.INTERNAL_SERVER_ERROR, correlationId);
  }
}


/**
 * Generic PATCH request
 */
async function patch<T>(
  endpoint: string,
  body?: any,
  userId?: string
): Promise<ApiResponse<T>> {
  const correlationId = generateCorrelationId();
  const url = `${API_BASE_URL}${endpoint}`;

  console.log(`[PATCH] ${url}`, { correlationId, body });

  try {
    const response = await fetch(url, {
      method: 'PATCH',
      credentials: 'include', // CRITICAL: Include HTTP-only cookies
      headers: {
        'Content-Type': 'application/json',
        'X-Correlation-ID': correlationId,
      },
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!response.ok) {
      throw handleApiError(response, correlationId);
    }

    const responseData = await response.json();

    // Wrap the response data in the ApiResponse structure
    const result: ApiResponse<T> = {
      data: responseData,
      correlation_id: correlationId
    };

    console.log(`[PATCH] Success: ${endpoint}`, { correlationId, status: response.status });

    return result;
  } catch (error) {
    console.error(`[PATCH] Error: ${endpoint}`, { correlationId, error });
    throw error instanceof ApiError ? error : new ApiError('Network error', HttpStatus.INTERNAL_SERVER_ERROR, correlationId);
  }
}


// Export all functions and types
export {
  get,
  post,
  put,
  del as delete,
  patch,
  ApiError,
  HttpStatus,
  generateCorrelationId,
};
