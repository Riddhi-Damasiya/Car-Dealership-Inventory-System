import { Navigate } from 'react-router-dom'
import api from '../services/api'

/**
 * Protected route component that requires authentication.
 * Redirects to login if user is not authenticated.
 */
function ProtectedRoute({ children }) {
  const isAuthenticated = api.isAuthenticated()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return children
}

export default ProtectedRoute
