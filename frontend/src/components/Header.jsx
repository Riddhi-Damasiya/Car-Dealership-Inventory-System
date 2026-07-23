import { Link, useNavigate } from 'react-router-dom'
import api from '../services/api'

/**
 * Header component with navigation and user info.
 */
function Header() {
  const navigate = useNavigate()
  const isAuthenticated = api.isAuthenticated()
  const user = api.getUser()
  const isAdmin = user?.is_admin || false

  const handleLogout = () => {
    api.logout()
    navigate('/login')
  }

  return (
    <header className="bg-white shadow">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-8">
            <Link to="/" className="text-xl font-bold text-blue-600">
              Car Dealership
            </Link>
            {isAuthenticated && (
              <div className="flex space-x-4">
                <Link
                  to="/dashboard"
                  className="text-gray-700 hover:text-blue-600 transition"
                >
                  Dashboard
                </Link>
                {isAdmin && (
                  <Link
                    to="/admin"
                    className="text-gray-700 hover:text-blue-600 transition"
                  >
                    Admin
                  </Link>
                )}
              </div>
            )}
          </div>
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <span className="text-gray-700">{user?.email}</span>
                <button
                  onClick={handleLogout}
                  className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="text-gray-700 hover:text-blue-600 transition"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>
    </header>
  )
}

export default Header
