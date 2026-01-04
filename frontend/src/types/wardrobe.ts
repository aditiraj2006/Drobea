export interface WardrobeItem {
  id: string
  user_id: string
  images: ImageData[]
  ai_tags: AITags
  metadata: ItemMetadata
  usage_stats: UsageStats
  organization: Organization
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface ImageData {
  original: string
  processed: string
  thumbnail: string
  width: number
  height: number
  file_size: number
}

export interface AITags {
  category: string
  subcategory: string
  colors: string[]
  style: string
  pattern: string
  season: string[]
  occasion: string[]
  confidence_score: number
}

export interface ItemMetadata {
  brand?: string
  size?: string
  price?: number
  purchase_date?: string
  material?: string
  care_instructions?: string
  color_code?: string
  size_fit?: string
}

export interface UsageStats {
  wear_count: number
  last_worn?: string
  cost_per_wear: number
  favorite: boolean
  rating?: number
}

export interface Organization {
  collections: string[]
  custom_tags: string[]
  donation_candidate: boolean
  archive: boolean
}

export interface WardrobeItemCreate {
  images: ImageData[]
  metadata?: Partial<ItemMetadata>
  organization?: Partial<Organization>
}

export interface WardrobeItemUpdate {
  metadata?: Partial<ItemMetadata>
  organization?: Partial<Organization>
  usage_stats?: Partial<UsageStats>
}

export interface WardrobeFilter {
  category?: string
  subcategory?: string
  colors?: string[]
  style?: string
  season?: string[]
  occasion?: string[]
  collections?: string[]
  custom_tags?: string[]
  favorite?: boolean
  min_rating?: number
  max_rating?: number
  price_min?: number
  price_max?: number
  brand?: string
  material?: string
  archive?: boolean
}

export interface WardrobeSearch {
  query: string
  filters?: WardrobeFilter
  sort_by: string
  sort_order: 'asc' | 'desc'
  page: number
  limit: number
}

export interface BulkUploadRequest {
  items: WardrobeItemCreate[]
  auto_process: boolean
}
