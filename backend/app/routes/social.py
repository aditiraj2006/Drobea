from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from app.models.user import User
from app.models.social import (
    Post, PostCreate, PostUpdate, PostResponse, SocialFeed,
    FollowRequest, FollowResponse, UserProfile, Challenge, ChallengeSubmission
)
from app.services.database.mongodb import get_database
from app.utils.auth import get_current_user

router = APIRouter()

@router.get("/feed", response_model=SocialFeed)
async def get_social_feed(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get social feed with posts from followed users
    """
    try:
        db = get_database()
        
        # Get user's following list
        user = await db.users.find_one({"_id": current_user.id})
        following = user.get("social_connections", {}).get("following", [])
        
        # Add current user to see their own posts
        following.append(current_user.id)
        
        # Get posts from followed users
        skip = (page - 1) * limit
        posts = await db.posts.find({
            "user_id": {"$in": following},
            "is_public": True
        }).sort("created_at", -1).skip(skip).limit(limit + 1).to_list(length=limit + 1)
        
        # Check if there are more posts
        has_more = len(posts) > limit
        if has_more:
            posts = posts[:limit]
        
        # Convert to response format
        post_responses = [PostResponse(**post) for post in posts]
        
        return SocialFeed(
            posts=post_responses,
            has_more=has_more,
            next_cursor=str(posts[-1]["_id"]) if posts and has_more else None
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get social feed: {str(e)}"
        )

@router.post("/posts", response_model=PostResponse)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new social post
    """
    try:
        db = get_database()
        
        # Create post
        post = Post(
            user_id=current_user.id,
            outfit_id=post_data.outfit_id,
            content=post_data.content,
            images=post_data.images or [],
            hashtags=post_data.hashtags or [],
            mentions=post_data.mentions or [],
            is_public=post_data.is_public
        )
        
        # Save to database
        result = await db.posts.insert_one(post.dict(by_alias=True))
        post.id = result.inserted_id
        
        return PostResponse(**post.dict(by_alias=True))
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create post: {str(e)}"
        )

@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific post
    """
    try:
        db = get_database()
        
        post = await db.posts.find_one({"_id": ObjectId(post_id)})
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        # Increment view count
        await db.posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$inc": {"views": 1}}
        )
        
        return PostResponse(**post)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get post: {str(e)}"
        )

@router.post("/posts/{post_id}/like")
async def like_post(
    post_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Like a post
    """
    try:
        db = get_database()
        
        # Check if post exists
        post = await db.posts.find_one({"_id": ObjectId(post_id)})
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        # Increment like count
        await db.posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$inc": {"likes": 1}}
        )
        
        return {"message": "Post liked successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to like post: {str(e)}"
        )

@router.post("/posts/{post_id}/share")
async def share_post(
    post_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Share a post
    """
    try:
        db = get_database()
        
        # Check if post exists
        post = await db.posts.find_one({"_id": ObjectId(post_id)})
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        # Increment share count
        await db.posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$inc": {"shares": 1}}
        )
        
        return {"message": "Post shared successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to share post: {str(e)}"
        )

@router.post("/follow/{user_id}")
async def follow_user(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Follow a user
    """
    try:
        db = get_database()
        
        # Check if user exists
        target_user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Add to following list
        await db.users.update_one(
            {"_id": current_user.id},
            {"$addToSet": {"social_connections.following": ObjectId(user_id)}}
        )
        
        # Add to target user's followers
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$addToSet": {"social_connections.followers": current_user.id}}
        )
        
        return {"message": "User followed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to follow user: {str(e)}"
        )

@router.delete("/follow/{user_id}")
async def unfollow_user(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Unfollow a user
    """
    try:
        db = get_database()
        
        # Remove from following list
        await db.users.update_one(
            {"_id": current_user.id},
            {"$pull": {"social_connections.following": ObjectId(user_id)}}
        )
        
        # Remove from target user's followers
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"social_connections.followers": current_user.id}}
        )
        
        return {"message": "User unfollowed successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to unfollow user: {str(e)}"
        )

@router.get("/suggestions")
async def get_follow_suggestions(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user)
):
    """
    Get follow suggestions
    """
    try:
        db = get_database()
        
        # Get users with similar interests or popular users
        suggestions = await db.users.find({
            "_id": {"$ne": current_user.id},
            "is_active": True
        }).limit(limit).to_list(length=limit)
        
        # Convert to response format
        suggestion_responses = []
        for user in suggestions:
            suggestion_responses.append(UserProfile(
                id=str(user["_id"]),
                username=user["username"],
                avatar=user.get("profile", {}).get("avatar"),
                bio=user.get("profile", {}).get("bio"),
                followers_count=len(user.get("social_connections", {}).get("followers", [])),
                following_count=len(user.get("social_connections", {}).get("following", [])),
                posts_count=0,  # Would need to count from posts collection
                is_following=False,  # Would need to check if current user follows them
                is_verified=user.get("is_verified", False)
            ))
        
        return {"suggestions": suggestion_responses}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get follow suggestions: {str(e)}"
        )

@router.get("/challenges")
async def get_challenges(
    current_user: User = Depends(get_current_user)
):
    """
    Get active challenges
    """
    try:
        db = get_database()
        
        challenges = await db.challenges.find({
            "is_active": True,
            "end_date": {"$gte": datetime.utcnow()}
        }).sort("created_at", -1).to_list(length=None)
        
        return {"challenges": challenges}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get challenges: {str(e)}"
        )

@router.post("/challenges/{challenge_id}/submit")
async def submit_challenge(
    challenge_id: str,
    post_id: str,
    submission_text: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Submit entry for a challenge
    """
    try:
        db = get_database()
        
        # Check if challenge exists and is active
        challenge = await db.challenges.find_one({
            "_id": ObjectId(challenge_id),
            "is_active": True
        })
        
        if not challenge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Challenge not found or inactive"
            )
        
        # Check if post exists and belongs to user
        post = await db.posts.find_one({
            "_id": ObjectId(post_id),
            "user_id": current_user.id
        })
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        # Create submission
        submission = ChallengeSubmission(
            challenge_id=ObjectId(challenge_id),
            user_id=current_user.id,
            post_id=ObjectId(post_id),
            submission_text=submission_text
        )
        
        # Save submission
        result = await db.challenge_submissions.insert_one(submission.dict(by_alias=True))
        
        # Add to challenge participants
        await db.challenges.update_one(
            {"_id": ObjectId(challenge_id)},
            {
                "$addToSet": {"participants": current_user.id},
                "$push": {"submissions": result.inserted_id}
            }
        )
        
        return {"message": "Challenge submission successful"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit challenge: {str(e)}"
        )
