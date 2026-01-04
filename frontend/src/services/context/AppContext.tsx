import React, { createContext, useContext, useReducer, useEffect } from 'react'
import { useAuth } from './AuthContext'

interface AppState {
  theme: 'light' | 'dark'
  sidebarOpen: boolean
  notifications: Notification[]
  isLoading: boolean
  currentPage: string
}

type AppAction =
  | { type: 'SET_THEME'; payload: 'light' | 'dark' }
  | { type: 'TOGGLE_SIDEBAR' }
  | { type: 'SET_SIDEBAR'; payload: boolean }
  | { type: 'ADD_NOTIFICATION'; payload: Notification }
  | { type: 'REMOVE_NOTIFICATION'; payload: string }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_CURRENT_PAGE'; payload: string }

interface Notification {
  id: string
  type: 'info' | 'success' | 'warning' | 'error'
  title: string
  message: string
  timestamp: Date
  read: boolean
}

interface AppContextType extends AppState {
  toggleTheme: () => void
  toggleSidebar: () => void
  setSidebar: (open: boolean) => void
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => void
  removeNotification: (id: string) => void
  markNotificationAsRead: (id: string) => void
  setLoading: (loading: boolean) => void
  setCurrentPage: (page: string) => void
}

const AppContext = createContext<AppContextType | undefined>(undefined)

const initialState: AppState = {
  theme: (localStorage.getItem('theme') as 'light' | 'dark') || 'light',
  sidebarOpen: localStorage.getItem('sidebarOpen') !== null 
    ? localStorage.getItem('sidebarOpen') === 'true'
    : true, // Default to open
  notifications: [],
  isLoading: false,
  currentPage: 'dashboard',
}

function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'SET_THEME':
      return { ...state, theme: action.payload }
    case 'TOGGLE_SIDEBAR':
      return { ...state, sidebarOpen: !state.sidebarOpen }
    case 'SET_SIDEBAR':
      return { ...state, sidebarOpen: action.payload }
    case 'ADD_NOTIFICATION':
      return {
        ...state,
        notifications: [...state.notifications, action.payload],
      }
    case 'REMOVE_NOTIFICATION':
      return {
        ...state,
        notifications: state.notifications.filter(n => n.id !== action.payload),
      }
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload }
    case 'SET_CURRENT_PAGE':
      return { ...state, currentPage: action.payload }
    default:
      return state
  }
}

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, initialState)
  const { user } = useAuth()

  useEffect(() => {
    // Apply theme to document
    document.documentElement.classList.toggle('dark', state.theme === 'dark')
    localStorage.setItem('theme', state.theme)
  }, [state.theme])

  useEffect(() => {
    // Save sidebar state
    localStorage.setItem('sidebarOpen', state.sidebarOpen.toString())
  }, [state.sidebarOpen])

  useEffect(() => {
    // Load notifications when user changes
    if (user) {
      loadNotifications()
    }
  }, [user])

  const loadNotifications = async () => {
    // This would typically fetch from an API
    // For now, we'll use mock data
    const mockNotifications: Notification[] = [
      {
        id: '1',
        type: 'info',
        title: 'Welcome to Drobea!',
        message: 'Start by uploading your first clothing item to your wardrobe.',
        timestamp: new Date(),
        read: false,
      },
    ]
    
    mockNotifications.forEach(notification => {
      dispatch({ type: 'ADD_NOTIFICATION', payload: notification })
    })
  }

  const toggleTheme = () => {
    const newTheme = state.theme === 'light' ? 'dark' : 'light'
    dispatch({ type: 'SET_THEME', payload: newTheme })
  }

  const toggleSidebar = () => {
    dispatch({ type: 'TOGGLE_SIDEBAR' })
  }

  const setSidebar = (open: boolean) => {
    dispatch({ type: 'SET_SIDEBAR', payload: open })
  }

  const addNotification = (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => {
    const newNotification: Notification = {
      ...notification,
      id: Date.now().toString(),
      timestamp: new Date(),
      read: false,
    }
    dispatch({ type: 'ADD_NOTIFICATION', payload: newNotification })
  }

  const removeNotification = (id: string) => {
    dispatch({ type: 'REMOVE_NOTIFICATION', payload: id })
  }

  const markNotificationAsRead = (id: string) => {
    // This would typically update the notification in the backend
    // For now, we'll just remove it from the local state
    removeNotification(id)
  }

  const setLoading = (loading: boolean) => {
    dispatch({ type: 'SET_LOADING', payload: loading })
  }

  const setCurrentPage = (page: string) => {
    dispatch({ type: 'SET_CURRENT_PAGE', payload: page })
  }

  const value: AppContextType = {
    ...state,
    toggleTheme,
    toggleSidebar,
    setSidebar,
    addNotification,
    removeNotification,
    markNotificationAsRead,
    setLoading,
    setCurrentPage,
  }

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useApp() {
  const context = useContext(AppContext)
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider')
  }
  return context
}
