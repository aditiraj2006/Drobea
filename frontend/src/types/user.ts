export interface User {
  id: string
  email: string
  username: string
  profile: UserProfile
  privacy_settings: PrivacySettings
  social_connections: SocialConnections
  is_active: boolean
  is_verified: boolean
  last_login?: string
  created_at: string
  updated_at: string
}

export interface UserProfile {
  avatar?: string
  bio?: string
  style_preferences: string[]
  body_measurements: Record<string, any>
  color_season?: string
  location?: string
  timezone?: string
}

export interface PrivacySettings {
  profile_visibility: 'public' | 'private' | 'friends'
  wardrobe_visibility: 'public' | 'private' | 'friends'
  outfit_sharing: boolean
  analytics_sharing: boolean
  data_retention_days: number
}

export interface SocialConnections {
  followers: string[]
  following: string[]
  blocked_users: string[]
  friend_requests: string[]
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  username: string
  password: string
  profile?: Partial<UserProfile>
}

export interface Token {
  access_token: string
  token_type: string
  expires_in: number
}

export interface UserStats {
  wardrobe_items: number
  outfits: number
  virtual_tryons: number
  posts: number
  member_since: string
}
