export interface Outfit {
  id: string
  user_id: string
  name: string
  description?: string
  items: OutfitItem[]
  occasion: string
  season: string
  weather_conditions: string[]
  calendar_events: CalendarEvent[]
  social_stats: SocialStats
  ai_generated: boolean
  rating?: number
  is_public: boolean
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface OutfitItem {
  item_id: string
  category: string
  position?: Record<string, number>
  layer: number
}

export interface CalendarEvent {
  date: string
  event_name: string
  location?: string
  notes?: string
}

export interface SocialStats {
  likes: number
  shares: number
  saves: number
  comments: string[]
  views: number
}

export interface OutfitCreate {
  name: string
  description?: string
  items: OutfitItem[]
  occasion: string
  season: string
  weather_conditions?: string[]
  calendar_events?: CalendarEvent[]
  is_public?: boolean
}

export interface OutfitUpdate {
  name?: string
  description?: string
  items?: OutfitItem[]
  occasion?: string
  season?: string
  weather_conditions?: string[]
  calendar_events?: CalendarEvent[]
  rating?: number
  is_public?: boolean
}

export interface OutfitGenerationRequest {
  occasion: string
  season: string
  weather_conditions?: string[]
  style_preferences?: string[]
  color_preferences?: string[]
  exclude_items?: string[]
  include_items?: string[]
}

export interface OutfitCalendarRequest {
  start_date: string
  end_date: string
  include_events?: boolean
}

export interface PackingListRequest {
  trip_destination: string
  start_date: string
  end_date: string
  weather_forecast?: Record<string, any>
  activities: string[]
  luggage_size: string
}

export interface PackingList {
  id: string
  user_id: string
  trip_name: string
  destination: string
  start_date: string
  end_date: string
  outfits: string[]
  individual_items: string[]
  checklist: Record<string, any>[]
  is_complete: boolean
  created_at: string
  updated_at: string
}
