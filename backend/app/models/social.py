from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from app.models.user import PyObjectId

class Comment(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    content: str
    likes: int = 0
    replies: List[PyObjectId] = []
    is_edited: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Post(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    outfit_id: Optional[PyObjectId] = None
    content: str
    images: List[str] = []
    hashtags: List[str] = []
    mentions: List[PyObjectId] = []
    likes: int = 0
    shares: int = 0
    saves: int = 0
    comments: List[PyObjectId] = []
    views: int = 0
    is_public: bool = True
    is_featured: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PostCreate(BaseModel):
    outfit_id: Optional[PyObjectId] = None
    content: str
    images: Optional[List[str]] = []
    hashtags: Optional[List[str]] = []
    mentions: Optional[List[PyObjectId]] = []
    is_public: bool = True

class PostUpdate(BaseModel):
    content: Optional[str] = None
    images: Optional[List[str]] = None
    hashtags: Optional[List[str]] = None
    is_public: Optional[bool] = None

class PostResponse(BaseModel):
    id: str
    user_id: str
    outfit_id: Optional[str] = None
    content: str
    images: List[str]
    hashtags: List[str]
    mentions: List[str]
    likes: int
    shares: int
    saves: int
    comments: List[str]
    views: int
    is_public: bool
    is_featured: bool
    created_at: datetime
    updated_at: datetime

class FollowRequest(BaseModel):
    user_id: PyObjectId

class FollowResponse(BaseModel):
    user_id: str
    is_following: bool
    followers_count: int
    following_count: int

class SocialFeed(BaseModel):
    posts: List[PostResponse]
    has_more: bool
    next_cursor: Optional[str] = None

class UserProfile(BaseModel):
    id: str
    username: str
    avatar: Optional[str] = None
    bio: Optional[str] = None
    followers_count: int
    following_count: int
    posts_count: int
    is_following: bool = False
    is_verified: bool = False

class Challenge(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    rules: List[str] = []
    hashtags: List[str] = []
    start_date: datetime
    end_date: datetime
    prize: Optional[str] = None
    participants: List[PyObjectId] = []
    submissions: List[PyObjectId] = []
    is_active: bool = True
    created_by: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ChallengeSubmission(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    challenge_id: PyObjectId
    user_id: PyObjectId
    post_id: PyObjectId
    submission_text: Optional[str] = None
    votes: int = 0
    is_winner: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Notification(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    type: str  # like, comment, follow, mention, challenge
    title: str
    message: str
    data: Dict[str, Any] = {}
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
