import { Navigate } from 'react-router-dom'
import api from '../services/api'

/**
 * Admin route component that requires admin authentication.
 * Redirects to dashboard if user is not admin.
 */
function AdminRoute({ children }) {
  const isAuthenticated = api.isAuthenticated()
  const user = api.getUser()
  const isAdmin = user?.is_admin || false

  if (!isAuthenticated || !isAdmin) {
    return <Navigate to="/dashboard" replace />
  }

  return children
}

export default AdminRoute
