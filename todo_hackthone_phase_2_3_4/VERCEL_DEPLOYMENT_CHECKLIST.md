# Vercel Deployment Checklist for TaskFlow Todo App

## Pre-Deployment Checklist

### 1. Build Configuration
- [x] **Frontend:** `npm run build` command is compatible (already configured in package.json)
- [x] **Next.js Configuration:** Optimized for Vercel with standalone output, security headers, and performance settings
- [ ] **Backend:** Ready for deployment (ensure it's deployed separately or integrated with Vercel Functions)

### 2. Environment Variables Setup

#### Frontend Environment Variables (NEXT_PUBLIC_*)
- [ ] `NEXT_PUBLIC_API_URL` - Deployed backend API URL (e.g., `https://your-backend-app.vercel.app` or your backend domain)

#### Backend Environment Variables
- [ ] `DATABASE_URL` - Production database connection string (PostgreSQL recommended)
- [ ] `JWT_SECRET` - Secure JWT secret key (32+ characters)
- [ ] `JWT_ALGORITHM` - JWT algorithm (default: `HS256`)
- [ ] `FRONTEND_URL` - Deployed frontend URL (e.g., `https://your-frontend-app.vercel.app`)
- [ ] `GEMINI_API_KEY` - Google Gemini API key for AI chat functionality
- [ ] `DB_POOL_SIZE` - Database connection pool size (default: `10`)
- [ ] `DB_MAX_OVERFLOW` - Maximum database overflow connections (default: `10`)
- [ ] `BCRYPT_ROUNDS` - Number of bcrypt hashing rounds (default: `12`)
- [ ] `ENVIRONMENT` - Environment type (`production`, `staging`)
- [ ] `LOG_LEVEL` - Logging level (`INFO`, `ERROR`)

### 3. Code-Level Optimizations Applied

#### Fixed SSR/Client-Side Issues
- [x] **TaskList.tsx:** Added `typeof window !== 'undefined'` check before `window.confirm()` usage
- [x] **FloatingChatbot.tsx:** Added `typeof window === 'undefined'` guard in useEffect for document listeners
- [x] **RegisterForm.tsx:** Added `typeof window !== 'undefined'` check before `window.location.assign()`
- [x] **LoginForm.tsx:** Added `typeof window !== 'undefined'` check before `window.location.assign()`

#### Next.js Configuration Optimized
- [x] **Output:** Set to `standalone` for optimized Vercel deployment
- [x] **Security Headers:** Added HSTS, XSS protection, frame options, etc.
- [x] **Performance:** Enabled `reactStrictMode` and `swcMinify`
- [x] **Images:** Optimized for WebP format with 30-day cache TTL
- [x] **Experimental:** Safe experimental features only

### 4. Absolute Paths Check
- [x] All paths in the frontend are relative to the Next.js app root
- [x] API calls use environment variables for base URLs
- [x] No hardcoded absolute paths that would break in Vercel environment

### 5. Static Analysis & Linting
- [x] TypeScript configuration is properly set for Next.js 15
- [x] No TypeScript compilation errors expected
- [x] ESLint configuration inherited from Next.js (no custom linting issues introduced)

### 6. CORS Configuration for Production
- [x] **Backend CORS:** Updated to allow production frontend URL
- [x] **Frontend API calls:** Use `NEXT_PUBLIC_API_URL` environment variable

### 7. Database Configuration
- [x] **Production Database:** PostgreSQL connection string ready
- [x] **Connection Pooling:** Properly configured for production scale
- [x] **Environment Variables:** DB pool settings configurable via environment

### 8. Deployment Steps

#### Frontend Deployment
1. Push code to GitHub repository
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Build command: `npm run build`
5. Output directory: `out` (for standalone) or let Vercel detect automatically
6. Root directory: `/frontend`

#### Backend Deployment Options
Choose one of the following:
- **Option A:** Deploy to separate hosting (recommended for this setup)
- **Option B:** Deploy as Vercel Functions (requires significant refactoring)
- **Option C:** Use Vercel with a different framework setup

### 9. Post-Deployment Checks
- [ ] Verify all API endpoints are accessible
- [ ] Test user registration and login flows
- [ ] Verify task CRUD operations work
- [ ] Test AI chat functionality
- [ ] Check that environment variables are properly loaded
- [ ] Verify SSL certificates are working
- [ ] Test responsive design on various devices

### 10. Security Considerations
- [x] **JWT Secrets:** Never exposed in frontend code
- [x] **HTTP-only Cookies:** Used for authentication tokens
- [x] **CORS Policy:** Restricted to specific domains only
- [x] **Headers:** Security headers implemented in Next.js config
- [ ] **Rate Limiting:** Consider implementing if not already done

### 11. Performance Optimizations
- [x] **Image Optimization:** WebP format enabled
- [x] **Caching:** 30-day TTL for static assets
- [x] **Bundle Size:** SWC minification enabled
- [ ] **CDN:** Automatic with Vercel deployment

### 12. Monitoring & Error Tracking
- [ ] Set up error monitoring (e.g., Sentry integration)
- [ ] Configure performance monitoring
- [ ] Set up alerts for critical errors

## Expected Build Output
- Frontend should build successfully with `npm run build`
- No SSR errors related to window/document usage
- Optimized bundles for production
- Standalone output ready for Vercel deployment

## Troubleshooting Common Issues
1. **Build fails with "window is not defined"**: Double-check all client-side only operations have proper guards
2. **API calls fail**: Verify NEXT_PUBLIC_API_URL is correctly set in Vercel environment
3. **Authentication fails**: Check that CORS settings allow the production domain
4. **Database connection issues**: Ensure DATABASE_URL is properly configured in backend environment