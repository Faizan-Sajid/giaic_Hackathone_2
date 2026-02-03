/**
 * Loading Skeleton Component for Vercel Deployment
 * Provides better UX and improves LCP metrics
 */

'use client'

export default function LoadingSkeleton() {
  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      {/* Header Skeleton */}
      <header className="bg-zinc-900 border-b border-zinc-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="animate-pulse">
            <div className="h-6 w-24 bg-zinc-700 rounded mb-2"></div>
            <div className="h-4 w-32 bg-zinc-700 rounded"></div>
          </div>
          <div className="animate-pulse">
            <div className="h-10 w-24 bg-zinc-700 rounded-lg"></div>
          </div>
        </div>
      </header>

      {/* Main Content Skeleton */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section Skeleton */}
        <div className="bg-zinc-900 rounded-2xl p-8 mb-8 border border-zinc-800 animate-pulse">
          <div className="flex items-center space-x-4">
            <div className="h-16 w-16 rounded-full bg-zinc-700"></div>
            <div>
              <div className="h-6 w-64 bg-zinc-700 rounded mb-2"></div>
              <div className="h-4 w-80 bg-zinc-700 rounded"></div>
            </div>
          </div>
        </div>

        {/* Stats Cards Skeleton */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {[1, 2, 3].map((item) => (
            <div
              key={item}
              className="bg-zinc-900 rounded-xl p-6 border border-zinc-800 animate-pulse"
            >
              <div className="flex items-center">
                <div className="h-12 w-12 rounded-lg bg-zinc-700 flex items-center justify-center"></div>
                <div className="ml-4">
                  <div className="h-4 w-24 bg-zinc-700 rounded mb-2"></div>
                  <div className="h-8 w-16 bg-zinc-700 rounded"></div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Quick Actions Skeleton */}
        <div className="bg-zinc-900 rounded-2xl p-8 border border-zinc-800 animate-pulse">
          <div className="text-center">
            <div className="h-6 w-48 bg-zinc-700 rounded mx-auto mb-4"></div>
            <div className="h-4 w-64 bg-zinc-700 rounded mx-auto mb-6"></div>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <div className="h-12 w-32 bg-zinc-700 rounded-lg"></div>
              <div className="h-12 w-32 bg-zinc-700 rounded-lg"></div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}