export interface ApiResponse<T = any> {
  data?: T
  message?: string
  error?: string
  status: number
}

export interface PaginatedResponse<T = any> {
  data: T[]
  total: number
  page: number
  limit: number
  has_more: boolean
}

export interface ApiError {
  message: string
  status: number
  details?: Record<string, any>
}

export interface UploadResponse {
  url: string
  filename: string
  size: number
  type: string
}

export interface SearchResponse<T = any> {
  results: T[]
  total: number
  query: string
  filters?: Record<string, any>
}

export interface AnalyticsData {
  labels: string[]
  datasets: {
    label: string
    data: number[]
    backgroundColor?: string
    borderColor?: string
  }[]
}

export interface ChartData {
  type: 'line' | 'bar' | 'pie' | 'doughnut'
  data: AnalyticsData
  options?: Record<string, any>
}
