import { api } from './client'
import { 
  WardrobeItem, 
  WardrobeItemCreate, 
  WardrobeItemUpdate, 
  WardrobeFilter, 
  WardrobeSearch,
  BulkUploadRequest 
} from '../../types/wardrobe'
import { PaginatedResponse, SearchResponse } from '../../types/api'

export const wardrobeApi = {
  getItems: (params?: {
    category?: string
    color?: string
    style?: string
    season?: string
    page?: number
    limit?: number
  }) =>
    api.get<WardrobeItem[]>('/wardrobe/items', { params }),
    
  getItem: (id: string) =>
    api.get<WardrobeItem>(`/wardrobe/items/${id}`),
    
  createItem: (itemData: WardrobeItemCreate) =>
    api.post<WardrobeItem>('/wardrobe/items', itemData),
    
  updateItem: (id: string, itemData: WardrobeItemUpdate) =>
    api.put<WardrobeItem>(`/wardrobe/items/${id}`, itemData),
    
  deleteItem: (id: string) =>
    api.delete(`/wardrobe/items/${id}`),
    
  bulkUpload: (request: BulkUploadRequest) =>
    api.post('/wardrobe/bulk-upload', request),
    
  processImage: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/wardrobe/ai/process-image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
    
  searchItems: (searchParams: WardrobeSearch) =>
    api.post<SearchResponse<WardrobeItem>>('/wardrobe/search', searchParams),
    
  getCategories: () =>
    api.get('/wardrobe/categories'),
    
  getColors: () =>
    api.get('/wardrobe/colors'),
    
  getStyles: () =>
    api.get('/wardrobe/styles'),
    
  getSeasons: () =>
    api.get('/wardrobe/seasons'),
}
