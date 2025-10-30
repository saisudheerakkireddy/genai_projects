"use client"
import { useUser } from '@clerk/nextjs'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

interface RoleProtectorProps {
  children: React.ReactNode
  allowedRoles: string[]
  redirectTo?: string
}

export function RoleProtector({ children, allowedRoles, redirectTo = '/role-select' }: RoleProtectorProps) {
  const { user, isLoaded } = useUser()
  const router = useRouter()

  useEffect(() => {
    if (isLoaded && user) {
      const userRole = user.publicMetadata?.role as string
      const localStorageRole = typeof window !== 'undefined' ? localStorage.getItem('userRole') : null
      const effectiveRole = userRole || localStorageRole
      
      if (!effectiveRole) {
        // No role set, redirect to role selection
        router.push('/role-select')
        return
      }
      
      if (!allowedRoles.includes(effectiveRole)) {
        // User doesn't have permission for this route
        router.push(redirectTo)
        return
      }
    }
  }, [user, isLoaded, allowedRoles, redirectTo, router])

  // Show loading while checking auth state
  if (!isLoaded) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  // Show nothing if user is not authenticated (Clerk middleware will handle redirect)
  if (!user) {
    return null
  }

  const userRole = user?.publicMetadata?.role as string
  const localStorageRole = typeof window !== 'undefined' ? localStorage.getItem('userRole') : null
  const effectiveRole = userRole || localStorageRole
  
  // Show nothing if user doesn't have the right role
  if (!effectiveRole || !allowedRoles.includes(effectiveRole)) {
    return null
  }

  return <>{children}</>
}
