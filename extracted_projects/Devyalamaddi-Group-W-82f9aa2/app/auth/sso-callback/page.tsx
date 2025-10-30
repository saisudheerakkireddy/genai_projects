"use client"

import { AuthenticateWithRedirectCallback } from '@clerk/nextjs'

export default function SSOCallback() {
  // Handle the redirect callback
  return <AuthenticateWithRedirectCallback />
}
