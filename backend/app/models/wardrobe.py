from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from app.models.user import PyObjectId

class ImageData(BaseModel):
    original: str
    processed: str
    thumbnail: str
    width: int
    height: int
    file_size: int

class AITags(BaseModel):
    category: str  # top, bottom, dress, shoes, accessories, etc.
    subcategory: str  # t-shirt, jeans, sneakers, etc.
    colors: List[str]  # primary colors detected
    style: str  # casual, formal, ethnic, etc.
    pattern: str  # solid, striped, printed, etc.
    season: List[str]  # spring, summer, fall, winter
    occasion: List[str]  # work, party, casual, formal, etc.
    confidence_score: float = Field(..., ge=0, le=1)

class ItemMetadata(BaseModel):
    brand: Optional[str] = None
    size: Optional[str] = None
    price: Optional[float] = None
    purchase_date: Optional[datetime] = None
    material: Optional[str] = None
    care_instructions: Optional[str] = None
    color_code: Optional[str] = None
    size_fit: Optional[str] = None  # loose, regular, tight

class UsageStats(BaseModel):
    wear_count: int = 0
    last_worn: Optional[datetime] = None
    cost_per_wear: float = 0.0
    favorite: bool = False
    rating: Optional[int] = Field(None, ge=1, le=5)

class Organization(BaseModel):
    collections: List[str] = []
    custom_tags: List[str] = []
    donation_candidate: bool = False
    archive: bool = False

class WardrobeItem(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    images: List[ImageData]
    ai_tags: AITags
    metadata: ItemMetadata = Field(default_factory=ItemMetadata)
    usage_stats: UsageStats = Field(default_factory=UsageStats)
    organization: Organization = Field(default_factory=Organization)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class WardrobeItemCreate(BaseModel):
    images: List[ImageData]
    metadata: Optional[ItemMetadata] = None
    organization: Optional[Organization] = None

class WardrobeItemUpdate(BaseModel):
    metadata: Optional[ItemMetadata] = None
    organization: Optional[Organization] = None
    usage_stats: Optional[UsageStats] = None

class WardrobeItemResponse(BaseModel):
    id: str
    user_id: str
    images: List[ImageData]
    ai_tags: AITags
    metadata: ItemMetadata
    usage_stats: UsageStats
    organization: Organization
    is_active: bool
    created_at: datetime
    updated_at: datetime

class BulkUploadRequest(BaseModel):
    items: List[WardrobeItemCreate]
    auto_process: bool = True

class WardrobeFilter(BaseModel):
    category: Optional[str] = None
    subcategory: Optional[str] = None
    colors: Optional[List[str]] = None
    style: Optional[str] = None
    season: Optional[List[str]] = None
    occasion: Optional[List[str]] = None
    collections: Optional[List[str]] = None
    custom_tags: Optional[List[str]] = None
    favorite: Optional[bool] = None
    min_rating: Optional[int] = None
    max_rating: Optional[int] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    brand: Optional[str] = None
    material: Optional[str] = None
    archive: Optional[bool] = None

class WardrobeSearch(BaseModel):
    query: str
    filters: Optional[WardrobeFilter] = None
    sort_by: str = "created_at"  # created_at, last_worn, wear_count, price
    sort_order: str = "desc"  # asc, desc
    page: int = 1
    limit: int = 20
