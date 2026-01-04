from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from app.models.user import PyObjectId

class WearAnalytics(BaseModel):
    total_items: int = 0
    items_worn: int = 0
    total_wears: int = 0
    average_wears_per_item: float = 0.0
    most_worn_item: Optional[str] = None
    least_worn_item: Optional[str] = None
    unused_items: int = 0

class CostAnalytics(BaseModel):
    total_investment: float = 0.0
    average_cost_per_wear: float = 0.0
    highest_cost_per_wear: float = 0.0
    lowest_cost_per_wear: float = 0.0
    total_savings: float = 0.0
    most_cost_effective_item: Optional[str] = None

class ColorAnalytics(BaseModel):
    most_used_colors: List[Dict[str, Any]] = []
    least_used_colors: List[Dict[str, Any]] = []
    color_distribution: Dict[str, int] = {}
    seasonal_color_trends: Dict[str, Dict[str, int]] = {}

class StyleAnalytics(BaseModel):
    most_used_styles: List[Dict[str, Any]] = []
    style_distribution: Dict[str, int] = {}
    occasion_style_mapping: Dict[str, str] = {}
    seasonal_style_trends: Dict[str, Dict[str, int]] = {}

class SustainabilityMetrics(BaseModel):
    carbon_footprint: float = 0.0  # in kg CO2
    water_usage: float = 0.0  # in liters
    waste_generated: float = 0.0  # in kg
    circularity_score: float = 0.0  # 0-1 scale
    donation_recommendations: int = 0
    swap_recommendations: int = 0

class UsageTrends(BaseModel):
    daily_usage: Dict[str, int] = {}  # date -> wear_count
    weekly_usage: Dict[str, int] = {}  # week -> wear_count
    monthly_usage: Dict[str, int] = {}  # month -> wear_count
    seasonal_usage: Dict[str, int] = {}  # season -> wear_count
    peak_usage_days: List[str] = []
    low_usage_days: List[str] = []

class OutfitAnalytics(BaseModel):
    total_outfits: int = 0
    outfits_created_this_month: int = 0
    most_used_outfit: Optional[str] = None
    favorite_outfit: Optional[str] = None
    ai_generated_outfits: int = 0
    user_created_outfits: int = 0
    outfit_rating_average: float = 0.0

class SocialAnalytics(BaseModel):
    total_posts: int = 0
    total_likes_received: int = 0
    total_followers: int = 0
    total_following: int = 0
    engagement_rate: float = 0.0
    most_liked_post: Optional[str] = None
    posts_this_month: int = 0

class VirtualTryOnAnalytics(BaseModel):
    total_generations: int = 0
    successful_generations: int = 0
    failed_generations: int = 0
    average_generation_time: float = 0.0
    average_quality_rating: float = 0.0
    most_used_pose: str = "standing"
    favorite_generations: int = 0

class AnalyticsDashboard(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    period: str  # daily, weekly, monthly, yearly
    wear_analytics: WearAnalytics = Field(default_factory=WearAnalytics)
    cost_analytics: CostAnalytics = Field(default_factory=CostAnalytics)
    color_analytics: ColorAnalytics = Field(default_factory=ColorAnalytics)
    style_analytics: StyleAnalytics = Field(default_factory=StyleAnalytics)
    sustainability_metrics: SustainabilityMetrics = Field(default_factory=SustainabilityMetrics)
    usage_trends: UsageTrends = Field(default_factory=UsageTrends)
    outfit_analytics: OutfitAnalytics = Field(default_factory=OutfitAnalytics)
    social_analytics: SocialAnalytics = Field(default_factory=SocialAnalytics)
    virtual_tryon_analytics: VirtualTryOnAnalytics = Field(default_factory=VirtualTryOnAnalytics)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class AnalyticsRequest(BaseModel):
    period: str = "monthly"  # daily, weekly, monthly, yearly
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    include_sustainability: bool = True
    include_social: bool = True
    include_virtual_tryon: bool = True

class TrendData(BaseModel):
    date: str
    value: float
    label: str

class ChartData(BaseModel):
    labels: List[str]
    datasets: List[Dict[str, Any]]
    type: str  # line, bar, pie, doughnut

class AnalyticsInsight(BaseModel):
    type: str  # recommendation, warning, achievement
    title: str
    message: str
    action_required: bool = False
    action_text: Optional[str] = None
    priority: str = "medium"  # low, medium, high
    category: str  # sustainability, cost, usage, style
