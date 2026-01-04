import { api } from './client'
import { User, LoginRequest, RegisterRequest, Token, UserStats } from '../../types/user'

export const authApi = {
  login: (credentials: LoginRequest) =>
    api.post<Token>('/auth/login', credentials),
  
  googleAuth: (idToken: string) =>
    api.post<Token>('/auth/google', { id_token: idToken }),
    
  register: (userData: RegisterRequest) =>
    api.post<User>('/auth/register', userData),
    
  logout: () =>
    api.post('/auth/logout'),
    
  refreshToken: () =>
    api.post<Token>('/auth/refresh'),
    
  forgotPassword: (email: string) =>
    api.post('/auth/forgot-password', { email }),
    
  resetPassword: (token: string, newPassword: string) =>
    api.post('/auth/reset-password', { token, new_password: newPassword }),
    
  verifyEmail: (token: string) =>
    api.post('/auth/verify-email', { token }),
    
  getCurrentUser: () =>
    api.get<User>('/auth/me'),
    
  updateProfile: (userData: Partial<User>) =>
    api.put<User>('/users/profile', userData),
    
  uploadAvatar: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/users/upload-avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
    
  getUserStats: () =>
    api.get<UserStats>('/users/stats'),
    
  deleteAccount: () =>
    api.delete('/users/account'),
}
