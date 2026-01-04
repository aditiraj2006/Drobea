import { NavLink } from 'react-router-dom'
import { useApp } from '../../services/context/AppContext'
import { 
  Home, 
  Shirt, 
  Calendar, 
  Camera, 
  Users, 
  BarChart3, 
  User, 
  Settings,
  ChevronLeft,
  ChevronRight
} from 'lucide-react'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: Home },
  { name: 'Wardrobe', href: '/wardrobe', icon: Shirt },
  { name: 'Outfits', href: '/outfits', icon: Calendar },
  { name: 'Virtual Try-On', href: '/virtual-tryon', icon: Camera },
  { name: 'Social', href: '/social', icon: Users },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
]

const secondaryNavigation = [
  { name: 'Profile', href: '/profile', icon: User },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export default function Sidebar() {
  const { sidebarOpen, toggleSidebar } = useApp()

  return (
    <>
      {/* Mobile backdrop overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={toggleSidebar}
          aria-hidden="true"
        />
      )}

      {/* Sidebar */}
      <div className={`fixed left-0 top-16 bottom-0 z-40 bg-white dark:bg-gray-900 shadow-lg border-r border-gray-200 dark:border-gray-700 transform transition-all duration-300 ease-in-out 
        ${sidebarOpen 
          ? 'w-64 translate-x-0' 
          : 'w-16 -translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Toggle button - Desktop only */}
        <button
          onClick={toggleSidebar}
          className="hidden lg:flex absolute -right-3 top-1/2 transform -translate-y-1/2 h-6 w-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-full items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-primary-600 dark:hover:text-primary-400 transition-all duration-200 shadow-md z-10"
          aria-label={sidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
        >
          {sidebarOpen ? (
            <ChevronLeft className="h-4 w-4" />
          ) : (
            <ChevronRight className="h-4 w-4" />
          )}
        </button>

        <div className="flex flex-col h-full">
          {/* Navigation */}
          <nav className="flex-1 px-2 py-6 space-y-2 overflow-y-auto">
            <div className="space-y-1">
              {navigation.map((item) => (
                <NavLink
                  key={item.name}
                  to={item.href}
                  onClick={() => {
                    // Close sidebar on mobile after navigation
                    if (window.innerWidth < 1024) {
                      toggleSidebar()
                    }
                  }}
                  className={({ isActive }) =>
                    `group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
                      isActive
                        ? 'bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400'
                        : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-gray-100'
                    }`
                  }
                  title={!sidebarOpen ? item.name : undefined}
                >
                  {({ isActive }) => (
                    <>
                      <item.icon
                        className={`flex-shrink-0 h-5 w-5 ${
                          sidebarOpen ? 'mr-3' : 'mx-auto'
                        } ${
                          isActive ? 'text-primary-600 dark:text-primary-400' : 'text-gray-400 dark:text-gray-500 group-hover:text-gray-500 dark:group-hover:text-gray-400'
                        }`}
                      />
                      {sidebarOpen && <span>{item.name}</span>}
                    </>
                  )}
                </NavLink>
              ))}
            </div>

            {/* Divider */}
            <div className="border-t border-gray-200 dark:border-gray-700 my-4" />

            {/* Secondary navigation */}
            <div className="space-y-1">
              {secondaryNavigation.map((item) => (
                <NavLink
                  key={item.name}
                  to={item.href}
                  onClick={() => {
                    // Close sidebar on mobile after navigation
                    if (window.innerWidth < 1024) {
                      toggleSidebar()
                    }
                  }}
                  className={({ isActive }) =>
                    `group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
                      isActive
                        ? 'bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400'
                        : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-gray-100'
                    }`
                  }
                  title={!sidebarOpen ? item.name : undefined}
                >
                  {({ isActive }) => (
                    <>
                      <item.icon
                        className={`flex-shrink-0 h-5 w-5 ${
                          sidebarOpen ? 'mr-3' : 'mx-auto'
                        } ${
                          isActive ? 'text-primary-600 dark:text-primary-400' : 'text-gray-400 dark:text-gray-500 group-hover:text-gray-500 dark:group-hover:text-gray-400'
                        }`}
                      />
                      {sidebarOpen && <span>{item.name}</span>}
                    </>
                  )}
                </NavLink>
              ))}
            </div>
          </nav>

          {/* Footer */}
          {sidebarOpen && (
            <div className="p-4 border-t border-gray-200 dark:border-gray-700">
              <div className="text-xs text-gray-500 dark:text-gray-400 text-center">
                <p>Drobea v1.0.0</p>
                <p className="mt-1">AI-Powered Clothing Navigator</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  )
}
