import { api } from './client'
import { 
  VirtualTryOnProfile,
  VirtualTryOnRequest,
  VirtualTryOnResponse,
  BatchGenerationRequest,
  BatchGenerationResponse,
  TryOnRating,
  ReferencePhoto
} from '../../types/virtualTryOn'

export const virtualTryOnApi = {
  uploadReferencePhoto: (file: File, poseType: string, isPrimary: boolean = false) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('pose_type', poseType)
    formData.append('is_primary', isPrimary.toString())
    
    return api.post('/virtual-tryon/upload-reference', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
  
  getReferencePhotos: () =>
    api.get<{ reference_photos: ReferencePhoto[]; preferences: any }>('/virtual-tryon/reference-photos'),
    
  deleteReferencePhoto: (photoId: string) =>
    api.delete(`/virtual-tryon/reference-photos/${photoId}`),
    
  generateTryOn: (request: VirtualTryOnRequest) =>
    api.post<VirtualTryOnResponse>('/virtual-tryon/generate', request),
    
  batchGenerate: (request: BatchGenerationRequest) =>
    api.post<BatchGenerationResponse>('/virtual-tryon/batch-generate', request),
    
  getGenerationHistory: (limit: number = 20) =>
    api.get<{ generations: VirtualTryOnResponse[]; total_count: number }>('/virtual-tryon/history', {
      params: { limit }
    }),
    
  rateGeneration: (generationId: string, rating: number, feedback?: string) =>
    api.post('/virtual-tryon/rate', {
      generation_id: generationId,
      rating,
      feedback
    }),
    
  deleteGeneration: (generationId: string) =>
    api.delete(`/virtual-tryon/generations/${generationId}`),
    
  getProfile: () =>
    api.get<VirtualTryOnProfile>('/virtual-tryon/profile'),
    
  updateProfile: (preferences: any) =>
    api.put<VirtualTryOnProfile>('/virtual-tryon/profile', preferences),
}
