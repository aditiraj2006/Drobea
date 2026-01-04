import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './services/context/AuthContext'
import { AppProvider } from './services/context/AppContext'
import { NotificationProvider } from './services/context/NotificationContext'
import Layout from './components/layout/Layout'
import ProtectedRoute from './components/common/ProtectedRoute'
import './styles/globals.css'

// Pages
import Dashboard from './pages/Dashboard'
import Wardrobe from './pages/Wardrobe'
import OutfitPlanner from './pages/OutfitPlanner'
import VirtualTryOn from './pages/VirtualTryOn'
import Social from './pages/Social'
import Analytics from './pages/Analytics'
import Profile from './pages/Profile'
import Settings from './pages/Settings'
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'
import ForgotPassword from './pages/auth/ForgotPassword'

function App() {
  return (
    <AuthProvider>
      <AppProvider>
        <NotificationProvider>
          <div className="min-h-screen bg-gray-50">
            <Routes>
              {/* redirect root to dashboard */}
              <Route path="/" element={<Navigate to="/dashboard" replace />} />

              {/* Public routes */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />

              {/* Protected nested routes under Layout */}
              <Route
                path="/"
                element={
                  <ProtectedRoute>
                    <Layout />
                  </ProtectedRoute>
                }
              >
                <Route index element={<Dashboard />} />
                <Route path="dashboard" element={<Dashboard />} />
                <Route path="wardrobe" element={<Wardrobe />} />
                <Route path="outfits" element={<OutfitPlanner />} />
                <Route path="virtual-tryon" element={<VirtualTryOn />} />
                <Route path="social" element={<Social />} />
                <Route path="analytics" element={<Analytics />} />
                <Route path="profile" element={<Profile />} />
                <Route path="settings" element={<Settings />} />
                <Route path="*" element={<Navigate to="/dashboard" replace />} />
              </Route>
            </Routes>
          </div>
        </NotificationProvider>
      </AppProvider>
    </AuthProvider>
  )
}

export default App
