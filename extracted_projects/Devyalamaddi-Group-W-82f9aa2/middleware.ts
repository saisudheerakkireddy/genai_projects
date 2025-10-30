import { clerkMiddleware } from '@clerk/nextjs/server'
import { NextResponse } from 'next/server'

export default clerkMiddleware(async (auth, req) => {
  // Get user session information
  const { userId, sessionId } = await auth()
  const url = req.nextUrl.pathname
  
  // Skip protection for auth routes, static files, and the root route
  if (url === '/' ||
      url.startsWith('/auth') || 
      url.startsWith('/_next') || 
      url.match(/\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)$/)) {
    return NextResponse.next()
  }
  
  // Explicit session checking
  if (!userId || !sessionId) {
    // No valid session - redirect to auth
    console.log(`No session found for ${url}, redirecting to /auth`)
    return NextResponse.redirect(new URL('/auth', req.url))
  }
  
  console.log(`Valid session found: userId=${userId}, sessionId=${sessionId?.slice(0, 10)}...`)
  return NextResponse.next()
})

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
  ],
}
