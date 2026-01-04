import React, { createContext, useContext, useReducer, useEffect } from 'react'
import { User, LoginRequest, RegisterRequest } from '../../types/user'
import { authApi } from '../api/auth'
import toast from 'react-hot-toast'

interface AuthState {
  user: User | null
  token: string | null
  isLoading: boolean
  isAuthenticated: boolean
}

type AuthAction =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: { user: User; token: string } }
  | { type: 'LOGIN_FAILURE' }
  | { type: 'LOGOUT' }
  | { type: 'UPDATE_USER'; payload: User }
  | { type: 'SET_LOADING'; payload: boolean }

interface AuthContextType extends AuthState {
  login: (credentials: LoginRequest) => Promise<void>
  register: (userData: RegisterRequest) => Promise<void>
  logout: () => void
  updateUser: (user: User) => void
  refreshToken: () => Promise<void>
  setAuthData: (tokenData: { access_token: string; token_type: string; expires_in: number }) => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

const initialState: AuthState = {
  user: null,
  token: localStorage.getItem('token'),
  isLoading: false,
  isAuthenticated: false,
}

function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'LOGIN_START':
      return { ...state, isLoading: true }
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isLoading: false,
        isAuthenticated: true,
      }
    case 'LOGIN_FAILURE':
      return {
        ...state,
        user: null,
        token: null,
        isLoading: false,
        isAuthenticated: false,
      }
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        token: null,
        isLoading: false,
        isAuthenticated: false,
      }
    case 'UPDATE_USER':
      return {
        ...state,
        user: action.payload,
      }
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload,
      }
    default:
      return state
  }
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, initialState)

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token')
    if (token) {
      // Verify token and get user data
      verifyToken()
    }
  }, [])

  const verifyToken = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true })
      const response = await authApi.getCurrentUser()
      if (response.data && state.token) {
        dispatch({
          type: 'LOGIN_SUCCESS',
          payload: { user: response.data, token: state.token },
        })
      } else {
        throw new Error('Invalid response')
      }
    } catch (error) {
      // Token is invalid, clear it
      localStorage.removeItem('token')
      dispatch({ type: 'LOGIN_FAILURE' })
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false })
    }
  }

  const login = async (credentials: LoginRequest) => {
    try {
      dispatch({ type: 'LOGIN_START' })
      const response = await authApi.login(credentials)
      
      if (!response.data?.access_token) {
        throw new Error('Invalid login response')
      }
      
      // Store token
      localStorage.setItem('token', response.data.access_token)
      
      // Get user data
      const userResponse = await authApi.getCurrentUser()
      
      if (!userResponse.data) {
        throw new Error('Failed to get user data')
      }
      
      dispatch({
        type: 'LOGIN_SUCCESS',
        payload: { user: userResponse.data, token: response.data.access_token },
      })
      
      toast.success('Welcome back!')
    } catch (error: any) {
      dispatch({ type: 'LOGIN_FAILURE' })
      toast.error(error.response?.data?.detail || 'Login failed')
      throw error
    }
  }

  const register = async (userData: RegisterRequest) => {
    try {
      dispatch({ type: 'LOGIN_START' })
      await authApi.register(userData)
      
      // Auto-login after registration
      await login({
        email: userData.email,
        password: userData.password,
      })
      
      toast.success('Account created successfully!')
    } catch (error: any) {
      dispatch({ type: 'LOGIN_FAILURE' })
      toast.error(error.response?.data?.detail || 'Registration failed')
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    dispatch({ type: 'LOGOUT' })
    toast.success('Logged out successfully')
  }

  const updateUser = (user: User) => {
    dispatch({ type: 'UPDATE_USER', payload: user })
  }

  const refreshToken = async () => {
    try {
      const response = await authApi.refreshToken()
      
      if (!response.data?.access_token) {
        throw new Error('Invalid refresh response')
      }
      
      localStorage.setItem('token', response.data.access_token)
      
      // Update token in state
      if (state.user) {
        dispatch({
          type: 'LOGIN_SUCCESS',
          payload: { user: state.user, token: response.data.access_token },
        })
      }
    } catch (error) {
      // Refresh failed, logout user
      logout()
    }
  }

  const setAuthData = async (tokenData: { access_token: string; token_type: string; expires_in: number }) => {
    try {
      // Store token
      localStorage.setItem('token', tokenData.access_token)
      
      // Get user data
      const userResponse = await authApi.getCurrentUser()
      
      if (!userResponse.data) {
        throw new Error('Failed to get user data')
      }
      
      dispatch({
        type: 'LOGIN_SUCCESS',
        payload: { user: userResponse.data, token: tokenData.access_token },
      })
    } catch (error: any) {
      dispatch({ type: 'LOGIN_FAILURE' })
      toast.error(error.response?.data?.detail || 'Authentication failed')
      throw error
    }
  }

  const value: AuthContextType = {
    ...state,
    login,
    register,
    logout,
    updateUser,
    refreshToken,
    setAuthData,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
