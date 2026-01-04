import { useLocation } from 'react-router-dom'
import { useAuth } from '../../services/context/AuthContext'
import Loading from './Loading'

interface ProtectedRouteProps {
  children: React.ReactNode
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isLoading } = useAuth()
  const location = useLocation()

  // Allow access without authentication (for development/demo)
  // Remove this return statement and uncomment code below to restore auth
  return <>{children}</>

  // Uncomment below to restore authentication requirement:
  // if (isLoading) {
  //   return <Loading />
  // }

  // if (!isAuthenticated) {
  //   return <Navigate to="/login" state={{ from: location }} replace />
  // }

  // return <>{children}</>
}
