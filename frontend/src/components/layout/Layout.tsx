import { Outlet } from 'react-router-dom'
import { useApp } from '../../services/context/AppContext'
import Navbar from './Navbar'
import Sidebar from './Sidebar'

interface LayoutProps {
  children?: React.ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const { sidebarOpen } = useApp()

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 transition-colors duration-200">
      <Navbar />
      <Sidebar />
      
      <main className={`transition-all duration-300 ease-in-out pt-16 ${
        sidebarOpen ? 'lg:ml-64' : 'lg:ml-16'
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children ?? <Outlet />}
        </div>
      </main>
    </div>
  )
}
