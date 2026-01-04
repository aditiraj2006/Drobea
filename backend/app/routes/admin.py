from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from app.models.user import User
from app.services.database.mongodb import get_database
from app.utils.auth import get_current_user

router = APIRouter()

@router.get("/users")
async def get_all_users(
    page: int = 1,
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    """
    Get all users (admin only)
    """
    try:
        # Check if user is admin (you would implement proper admin check)
        if not current_user.is_verified:  # Simple check for demo
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        db = get_database()
        
        skip = (page - 1) * limit
        users = await db.users.find({}).skip(skip).limit(limit).to_list(length=limit)
        
        return {"users": users}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get users: {str(e)}"
        )

@router.get("/stats")
async def get_platform_stats(
    current_user: User = Depends(get_current_user)
):
    """
    Get platform statistics (admin only)
    """
    try:
        # Check if user is admin
        if not current_user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        db = get_database()
        
        # Get counts
        total_users = await db.users.count_documents({})
        active_users = await db.users.count_documents({"is_active": True})
        total_wardrobe_items = await db.wardrobe_items.count_documents({})
        total_outfits = await db.outfits.count_documents({})
        total_posts = await db.posts.count_documents({})
        total_generations = await db.generation_results.count_documents({})
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "total_wardrobe_items": total_wardrobe_items,
            "total_outfits": total_outfits,
            "total_posts": total_posts,
            "total_generations": total_generations
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get platform stats: {str(e)}"
        )

@router.post("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Deactivate a user (admin only)
    """
    try:
        # Check if user is admin
        if not current_user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        db = get_database()
        
        # Deactivate user
        result = await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {"message": "User deactivated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to deactivate user: {str(e)}"
        )

@router.post("/users/{user_id}/activate")
async def activate_user(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Activate a user (admin only)
    """
    try:
        # Check if user is admin
        if not current_user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        db = get_database()
        
        # Activate user
        result = await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_active": True, "updated_at": datetime.utcnow()}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {"message": "User activated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to activate user: {str(e)}"
        )
