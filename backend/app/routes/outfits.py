from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from app.models.user import User
from app.models.outfit import (
    Outfit, OutfitCreate, OutfitUpdate, OutfitResponse,
    OutfitGenerationRequest, OutfitCalendarRequest, PackingListRequest
)
from app.services.database.mongodb import get_database
from app.services.ai.outfit_recommender import OutfitRecommender
from app.utils.auth import get_current_user

router = APIRouter()

# Initialize services
outfit_recommender = OutfitRecommender()

@router.get("/", response_model=List[OutfitResponse])
async def get_outfits(
    occasion: Optional[str] = Query(None),
    season: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's outfits with optional filtering
    """
    try:
        db = get_database()
        
        # Build filter query
        filter_query = {"user_id": current_user.id, "is_active": True}
        
        if occasion:
            filter_query["occasion"] = occasion
        if season:
            filter_query["season"] = season
        
        # Get outfits with pagination
        skip = (page - 1) * limit
        outfits = await db.outfits.find(filter_query).skip(skip).limit(limit).to_list(length=limit)
        
        # Convert to response format
        outfit_responses = [OutfitResponse(**outfit) for outfit in outfits]
        
        return outfit_responses
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get outfits: {str(e)}"
        )

@router.post("/", response_model=OutfitResponse)
async def create_outfit(
    outfit_data: OutfitCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new outfit
    """
    try:
        db = get_database()
        
        # Create outfit
        outfit = Outfit(
            user_id=current_user.id,
            name=outfit_data.name,
            description=outfit_data.description,
            items=outfit_data.items,
            occasion=outfit_data.occasion,
            season=outfit_data.season,
            weather_conditions=outfit_data.weather_conditions or [],
            calendar_events=outfit_data.calendar_events or [],
            is_public=outfit_data.is_public
        )
        
        # Save to database
        result = await db.outfits.insert_one(outfit.dict(by_alias=True))
        outfit.id = result.inserted_id
        
        return OutfitResponse(**outfit.dict(by_alias=True))
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create outfit: {str(e)}"
        )

@router.get("/{outfit_id}", response_model=OutfitResponse)
async def get_outfit(
    outfit_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific outfit
    """
    try:
        db = get_database()
        
        outfit = await db.outfits.find_one({
            "_id": ObjectId(outfit_id),
            "user_id": current_user.id
        })
        
        if not outfit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Outfit not found"
            )
        
        return OutfitResponse(**outfit)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get outfit: {str(e)}"
        )

@router.put("/{outfit_id}", response_model=OutfitResponse)
async def update_outfit(
    outfit_id: str,
    outfit_update: OutfitUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update an outfit
    """
    try:
        db = get_database()
        
        # Check if outfit exists and belongs to user
        existing_outfit = await db.outfits.find_one({
            "_id": ObjectId(outfit_id),
            "user_id": current_user.id
        })
        
        if not existing_outfit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Outfit not found"
            )
        
        # Prepare update data
        update_data = outfit_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        # Update outfit
        await db.outfits.update_one(
            {"_id": ObjectId(outfit_id)},
            {"$set": update_data}
        )
        
        # Get updated outfit
        updated_outfit = await db.outfits.find_one({"_id": ObjectId(outfit_id)})
        return OutfitResponse(**updated_outfit)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update outfit: {str(e)}"
        )

@router.delete("/{outfit_id}")
async def delete_outfit(
    outfit_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete an outfit
    """
    try:
        db = get_database()
        
        # Soft delete - mark as inactive
        result = await db.outfits.update_one(
            {"_id": ObjectId(outfit_id), "user_id": current_user.id},
            {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Outfit not found"
            )
        
        return {"message": "Outfit deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete outfit: {str(e)}"
        )

@router.post("/generate")
async def generate_outfit_suggestions(
    request: OutfitGenerationRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate AI-powered outfit suggestions
    """
    try:
        # Get user's wardrobe items
        db = get_database()
        wardrobe_items = await db.wardrobe_items.find({
            "user_id": current_user.id,
            "is_active": True
        }).to_list(length=None)
        
        # Generate outfit suggestions
        suggestions = await outfit_recommender.generate_outfit_suggestions(
            wardrobe_items=wardrobe_items,
            occasion=request.occasion,
            season=request.season,
            weather_conditions=request.weather_conditions or [],
            style_preferences=request.style_preferences or [],
            color_preferences=request.color_preferences or [],
            exclude_items=request.exclude_items or [],
            include_items=request.include_items or []
        )
        
        return {"suggestions": suggestions}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Outfit generation failed: {str(e)}"
        )

@router.get("/calendar")
async def get_outfit_calendar(
    start_date: str = Query(...),
    end_date: str = Query(...),
    current_user: User = Depends(get_current_user)
):
    """
    Get outfit calendar for date range
    """
    try:
        db = get_database()
        
        # Parse dates
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        # Get outfits with calendar events in date range
        outfits = await db.outfits.find({
            "user_id": current_user.id,
            "is_active": True,
            "calendar_events.date": {
                "$gte": start_dt,
                "$lte": end_dt
            }
        }).to_list(length=None)
        
        # Organize by date
        calendar_data = {}
        for outfit in outfits:
            for event in outfit.get("calendar_events", []):
                event_date = event["date"].strftime("%Y-%m-%d")
                if event_date not in calendar_data:
                    calendar_data[event_date] = []
                
                calendar_data[event_date].append({
                    "outfit_id": str(outfit["_id"]),
                    "outfit_name": outfit["name"],
                    "event_name": event["event_name"],
                    "location": event.get("location"),
                    "notes": event.get("notes")
                })
        
        return {"calendar": calendar_data}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get outfit calendar: {str(e)}"
        )

@router.post("/packing-list")
async def create_packing_list(
    request: PackingListRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Create a packing list for a trip
    """
    try:
        # Generate packing suggestions
        packing_suggestions = await outfit_recommender.generate_packing_list(
            destination=request.trip_destination,
            start_date=request.start_date,
            end_date=request.end_date,
            weather_forecast=request.weather_forecast,
            activities=request.activities,
            luggage_size=request.luggage_size
        )
        
        return {"packing_list": packing_suggestions}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Packing list generation failed: {str(e)}"
        )

@router.get("/stats")
async def get_outfit_stats(current_user: User = Depends(get_current_user)):
    """
    Get outfit statistics
    """
    try:
        db = get_database()
        
        # Get total outfits
        total_outfits = await db.outfits.count_documents({
            "user_id": current_user.id,
            "is_active": True
        })
        
        # Get outfits by occasion
        occasion_stats = await db.outfits.aggregate([
            {"$match": {"user_id": current_user.id, "is_active": True}},
            {"$group": {"_id": "$occasion", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]).to_list(length=None)
        
        # Get outfits by season
        season_stats = await db.outfits.aggregate([
            {"$match": {"user_id": current_user.id, "is_active": True}},
            {"$group": {"_id": "$season", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]).to_list(length=None)
        
        # Get most used items
        most_used_items = await db.outfits.aggregate([
            {"$match": {"user_id": current_user.id, "is_active": True}},
            {"$unwind": "$items"},
            {"$group": {"_id": "$items.item_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]).to_list(length=None)
        
        return {
            "total_outfits": total_outfits,
            "occasion_stats": occasion_stats,
            "season_stats": season_stats,
            "most_used_items": most_used_items
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get outfit stats: {str(e)}"
        )
