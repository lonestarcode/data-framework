import React from 'react';
import { Navigate } from 'react-router-dom';

function ProtectedRoute({ children }) {
  // This is a simple implementation. In a real app, you'd want to:
  // 1. Check for a valid auth token
  // 2. Verify the token with your backend
  // 3. Handle token refresh
  // 4. Show loading states while checking auth
  
  const isAuthenticated = true; // Replace with actual auth check

  if (!isAuthenticated) {
    // Redirect to login page if not authenticated
    return <Navigate to="/login" replace />;
  }

  return children;
}

export default ProtectedRoute;
