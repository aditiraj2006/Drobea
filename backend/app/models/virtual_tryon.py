from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from app.models.user import PyObjectId

class PoseData(BaseModel):
    landmarks: List[Dict[str, float]]
    bounding_box: Dict[str, float]
    confidence: float
    pose_type: str  # standing, walking, sitting, etc.

class ReferencePhoto(BaseModel):
    pose_type: str
    image_url: str
    pose_data: PoseData
    is_primary: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GenerationRequest(BaseModel):
    outfit_id: PyObjectId
    pose_type: str
    prompt_used: str
    ai_service: str  # gemini, stable_diffusion, dall_e
    quality_preference: str = "high"  # low, medium, high, ultra

class GenerationResult(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    generation_request: GenerationRequest
    generated_image: str
    quality_rating: Optional[float] = Field(None, ge=0, le=1)
    generation_time: float  # in seconds
    processing_cost: Optional[float] = None
    metadata: Dict[str, Any] = {}
    is_successful: bool = True
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class VirtualTryOnProfile(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    reference_photos: List[ReferencePhoto] = []
    generation_requests: List[PyObjectId] = []
    preferences: Dict[str, Any] = {
        "default_pose": "standing",
        "quality_preference": "high",
        "auto_save": True,
        "background_style": "original"
    }
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class VirtualTryOnRequest(BaseModel):
    outfit_id: PyObjectId
    pose_type: str = "standing"
    quality_preference: str = "high"
    background_style: str = "original"  # original, transparent, studio
    enhancement_level: int = Field(default=1, ge=0, le=3)

class VirtualTryOnResponse(BaseModel):
    id: str
    user_id: str
    outfit_id: str
    generated_image: str
    pose_type: str
    quality_rating: Optional[float] = None
    generation_time: float
    ai_service_used: str
    created_at: datetime

class BatchGenerationRequest(BaseModel):
    outfit_ids: List[PyObjectId]
    pose_types: List[str] = ["standing"]
    quality_preference: str = "high"

class BatchGenerationResponse(BaseModel):
    batch_id: str
    total_requests: int
    successful_generations: int
    failed_generations: int
    results: List[VirtualTryOnResponse]
    created_at: datetime

class TryOnRating(BaseModel):
    generation_id: PyObjectId
    rating: int = Field(..., ge=1, le=5)
    feedback: Optional[str] = None
    quality_aspects: Dict[str, int] = {}  # realism, fit, color_accuracy, etc.

class TryOnHistory(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    generation_results: List[PyObjectId] = []
    total_generations: int = 0
    successful_generations: int = 0
    average_rating: float = 0.0
    favorite_generations: List[PyObjectId] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
