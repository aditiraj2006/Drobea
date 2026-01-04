from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import Optional
from bson import ObjectId
from datetime import datetime

from app.models.user import User, UserUpdate, UserResponse
from app.services.database.mongodb import get_database
from app.utils.auth import get_current_user
from app.utils.validators import validate_username, validate_email

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user's profile
    """
    return UserResponse(**current_user.dict(by_alias=True))

@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update user profile
    """
    try:
        db = get_database()
        
        # Validate username if provided
        if user_update.username and not validate_username(user_update.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username format"
            )
        
        # Check if username is already taken
        if user_update.username:
            existing_user = await db.users.find_one({
                "username": user_update.username,
                "_id": {"$ne": current_user.id}
            })
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        # Prepare update data
        update_data = user_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        # Update user
        result = await db.users.update_one(
            {"_id": current_user.id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get updated user
        updated_user = await db.users.find_one({"_id": current_user.id})
        return UserResponse(**updated_user)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profile update failed: {str(e)}"
        )

@router.post("/upload-avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload user avatar
    """
    try:
        # Validate file
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image"
            )
        
        # Read file content
        file_content = await file.read()
        if len(file_content) > 5 * 1024 * 1024:  # 5MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File too large. Maximum size is 5MB"
            )
        
        # Save file (in production, upload to cloud storage)
        import uuid
        filename = f"avatar_{current_user.id}_{uuid.uuid4().hex}.{file.filename.split('.')[-1]}"
        filepath = f"uploads/avatars/{filename}"
        
        import os
        os.makedirs("uploads/avatars", exist_ok=True)
        
        with open(filepath, "wb") as f:
            f.write(file_content)
        
        # Update user profile with avatar URL
        db = get_database()
        await db.users.update_one(
            {"_id": current_user.id},
            {"$set": {"profile.avatar": filepath, "updated_at": datetime.utcnow()}}
        )
        
        return {"message": "Avatar uploaded successfully", "avatar_url": filepath}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Avatar upload failed: {str(e)}"
        )

@router.get("/preferences")
async def get_user_preferences(current_user: User = Depends(get_current_user)):
    """
    Get user preferences
    """
    return {
        "style_preferences": current_user.profile.style_preferences,
        "color_season": current_user.profile.color_season,
        "body_measurements": current_user.profile.body_measurements,
        "privacy_settings": current_user.privacy_settings
    }

@router.put("/preferences")
async def update_user_preferences(
    preferences: dict,
    current_user: User = Depends(get_current_user)
):
    """
    Update user preferences
    """
    try:
        db = get_database()
        
        # Update preferences
        await db.users.update_one(
            {"_id": current_user.id},
            {"$set": {"profile": preferences, "updated_at": datetime.utcnow()}}
        )
        
        return {"message": "Preferences updated successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Preferences update failed: {str(e)}"
        )

@router.get("/stats")
async def get_user_stats(current_user: User = Depends(get_current_user)):
    """
    Get user statistics
    """
    try:
        db = get_database()
        
        # Get wardrobe count
        wardrobe_count = await db.wardrobe_items.count_documents({"user_id": current_user.id})
        
        # Get outfits count
        outfits_count = await db.outfits.count_documents({"user_id": current_user.id})
        
        # Get virtual try-on count
        tryon_count = await db.generation_results.count_documents({"user_id": current_user.id})
        
        # Get social stats
        posts_count = await db.posts.count_documents({"user_id": current_user.id})
        
        return {
            "wardrobe_items": wardrobe_count,
            "outfits": outfits_count,
            "virtual_tryons": tryon_count,
            "posts": posts_count,
            "member_since": current_user.created_at
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user stats: {str(e)}"
        )

@router.delete("/account")
async def delete_account(current_user: User = Depends(get_current_user)):
    """
    Delete user account
    """
    try:
        db = get_database()
        
        # Deactivate account instead of deleting
        await db.users.update_one(
            {"_id": current_user.id},
            {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
        )
        
        return {"message": "Account deactivated successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Account deletion failed: {str(e)}"
        )
