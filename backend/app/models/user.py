from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        json_schema = handler(core_schema)
        if isinstance(json_schema, dict):
            json_schema.update(type="string")
        return json_schema

class UserProfile(BaseModel):
    avatar: Optional[str] = None
    bio: Optional[str] = None
    style_preferences: List[str] = []
    body_measurements: Dict[str, Any] = {}
    color_season: Optional[str] = None
    location: Optional[str] = None
    timezone: Optional[str] = None

class PrivacySettings(BaseModel):
    profile_visibility: str = "public"  # public, private, friends
    wardrobe_visibility: str = "private"  # public, private, friends
    outfit_sharing: bool = True
    analytics_sharing: bool = False
    data_retention_days: int = 365

class SocialConnections(BaseModel):
    # store object ids as strings for pydantic v2 compatibility
    followers: List[str] = []
    following: List[str] = []
    blocked_users: List[str] = []
    friend_requests: List[str] = []

class User(BaseModel):
    # use string id to avoid custom-type schema generation issues
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password_hash: Optional[str] = None  # Optional for OAuth users
    auth_provider: str = "email"  # "email" or "google"
    firebase_uid: Optional[str] = None  # For Firebase/Google OAuth users
    profile: UserProfile = Field(default_factory=UserProfile)
    privacy_settings: PrivacySettings = Field(default_factory=PrivacySettings)
    social_connections: SocialConnections = Field(default_factory=SocialConnections)
    is_active: bool = True
    is_verified: bool = False
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        # pydantic v2 renamed this setting
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    profile: Optional[UserProfile] = None

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    profile: Optional[UserProfile] = None
    privacy_settings: Optional[PrivacySettings] = None

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    profile: UserProfile
    privacy_settings: PrivacySettings
    social_connections: SocialConnections
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class GoogleAuthRequest(BaseModel):
    id_token: str  # Firebase ID token from Google OAuth

class TokenData(BaseModel):
    email: Optional[str] = None
