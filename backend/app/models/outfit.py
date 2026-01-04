from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from app.models.user import PyObjectId

class CalendarEvent(BaseModel):
    date: datetime
    event_name: str
    location: Optional[str] = None
    notes: Optional[str] = None

class SocialStats(BaseModel):
    likes: int = 0
    shares: int = 0
    saves: int = 0
    comments: List[PyObjectId] = []
    views: int = 0

class OutfitItem(BaseModel):
    item_id: PyObjectId
    category: str
    position: Optional[Dict[str, float]] = None  # x, y coordinates for UI
    layer: int = 0  # for layering items

class Outfit(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    name: str
    description: Optional[str] = None
    items: List[OutfitItem]
    occasion: str
    season: str
    weather_conditions: List[str] = []
    calendar_events: List[CalendarEvent] = []
    social_stats: SocialStats = Field(default_factory=SocialStats)
    ai_generated: bool = False
    rating: Optional[int] = Field(None, ge=1, le=5)
    is_public: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class OutfitCreate(BaseModel):
    name: str
    description: Optional[str] = None
    items: List[OutfitItem]
    occasion: str
    season: str
    weather_conditions: Optional[List[str]] = []
    calendar_events: Optional[List[CalendarEvent]] = []
    is_public: bool = False

class OutfitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    items: Optional[List[OutfitItem]] = None
    occasion: Optional[str] = None
    season: Optional[str] = None
    weather_conditions: Optional[List[str]] = None
    calendar_events: Optional[List[CalendarEvent]] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    is_public: Optional[bool] = None

class OutfitResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    items: List[OutfitItem]
    occasion: str
    season: str
    weather_conditions: List[str]
    calendar_events: List[CalendarEvent]
    social_stats: SocialStats
    ai_generated: bool
    rating: Optional[int] = None
    is_public: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

class OutfitGenerationRequest(BaseModel):
    occasion: str
    season: str
    weather_conditions: Optional[List[str]] = []
    style_preferences: Optional[List[str]] = []
    color_preferences: Optional[List[str]] = []
    exclude_items: Optional[List[PyObjectId]] = []
    include_items: Optional[List[PyObjectId]] = []

class OutfitCalendarRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    include_events: bool = True

class PackingListRequest(BaseModel):
    trip_destination: str
    start_date: datetime
    end_date: datetime
    weather_forecast: Optional[Dict[str, Any]] = None
    activities: List[str] = []
    luggage_size: str = "medium"  # small, medium, large

class PackingList(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    trip_name: str
    destination: str
    start_date: datetime
    end_date: datetime
    outfits: List[PyObjectId] = []
    individual_items: List[PyObjectId] = []
    checklist: List[Dict[str, Any]] = []
    is_complete: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
