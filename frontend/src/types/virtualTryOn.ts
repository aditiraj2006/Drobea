export interface VirtualTryOnProfile {
  id: string
  user_id: string
  reference_photos: ReferencePhoto[]
  generation_requests: string[]
  preferences: VirtualTryOnPreferences
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface ReferencePhoto {
  id: string
  pose_type: string
  image_url: string
  pose_data: PoseData
  is_primary: boolean
  created_at: string
}

export interface PoseData {
  landmarks: Record<string, number>[]
  bounding_box: Record<string, number>
  confidence: number
  pose_type: string
}

export interface VirtualTryOnPreferences {
  default_pose: string
  quality_preference: string
  auto_save: boolean
  background_style: string
}

export interface VirtualTryOnRequest {
  outfit_id: string
  pose_type?: string
  quality_preference?: string
  background_style?: string
  enhancement_level?: number
}

export interface VirtualTryOnResponse {
  id: string
  user_id: string
  outfit_id: string
  generated_image: string
  pose_type: string
  quality_rating?: number
  generation_time: number
  ai_service_used: string
  created_at: string
}

export interface BatchGenerationRequest {
  outfit_ids: string[]
  pose_types?: string[]
  quality_preference?: string
}

export interface BatchGenerationResponse {
  batch_id: string
  total_requests: number
  successful_generations: number
  failed_generations: number
  results: VirtualTryOnResponse[]
  created_at: string
}

export interface TryOnRating {
  generation_id: string
  rating: number
  feedback?: string
  quality_aspects?: Record<string, number>
}

export interface TryOnHistory {
  id: string
  user_id: string
  generation_results: string[]
  total_generations: number
  successful_generations: number
  average_rating: number
  favorite_generations: string[]
  created_at: string
  updated_at: string
}
