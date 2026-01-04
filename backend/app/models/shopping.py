from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from app.models.user import PyObjectId

class Product(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    external_id: Optional[str] = None  # ID from external platform
    name: str
    brand: str
    description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    currency: str = "USD"
    images: List[str] = []
    category: str
    subcategory: str
    colors: List[str] = []
    sizes: List[str] = []
    materials: List[str] = []
    care_instructions: Optional[str] = None
    url: str
    platform: str  # amazon, shopify, etc.
    availability: str = "in_stock"  # in_stock, out_of_stock, limited
    rating: Optional[float] = Field(None, ge=0, le=5)
    review_count: int = 0
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class WishlistItem(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    product_id: PyObjectId
    notes: Optional[str] = None
    priority: int = 1  # 1-5, 5 being highest
    target_price: Optional[float] = None
    size_preference: Optional[str] = None
    color_preference: Optional[str] = None
    is_purchased: bool = False
    purchase_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PriceAlert(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    product_id: PyObjectId
    target_price: float
    current_price: float
    price_drop_percentage: float
    is_active: bool = True
    last_checked: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ShoppingList(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    name: str
    description: Optional[str] = None
    items: List[PyObjectId] = []
    total_estimated_cost: float = 0.0
    is_shared: bool = False
    shared_with: List[PyObjectId] = []
    is_complete: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Purchase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    product_id: PyObjectId
    quantity: int = 1
    unit_price: float
    total_price: float
    currency: str = "USD"
    platform: str
    order_id: Optional[str] = None
    purchase_date: datetime
    delivery_date: Optional[datetime] = None
    status: str = "pending"  # pending, confirmed, shipped, delivered, cancelled
    notes: Optional[str] = None
    receipt_image: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ShoppingRecommendation(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    product_id: PyObjectId
    recommendation_type: str  # similar_item, trend, seasonal, price_drop
    confidence_score: float = Field(..., ge=0, le=1)
    reason: str
    is_dismissed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ProductImport(BaseModel):
    url: str
    platform: Optional[str] = None
    auto_extract: bool = True

class WishlistCreate(BaseModel):
    product_id: PyObjectId
    notes: Optional[str] = None
    priority: int = Field(default=1, ge=1, le=5)
    target_price: Optional[float] = None
    size_preference: Optional[str] = None
    color_preference: Optional[str] = None

class ShoppingListCreate(BaseModel):
    name: str
    description: Optional[str] = None
    items: Optional[List[PyObjectId]] = []
    is_shared: bool = False
    shared_with: Optional[List[PyObjectId]] = []
