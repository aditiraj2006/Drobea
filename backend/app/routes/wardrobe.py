from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from app.models.user import User
from app.models.wardrobe import (
    WardrobeItem, WardrobeItemCreate, WardrobeItemUpdate, WardrobeItemResponse,
    WardrobeFilter, WardrobeSearch, BulkUploadRequest
)
from app.services.database.mongodb import get_database
from app.services.ai.image_processing import ImageProcessor
from app.services.ai.auto_tagging import AutoTaggingService
from app.utils.auth import get_current_user
from app.utils.validators import validate_file_extension, validate_file_size

router = APIRouter()

# Initialize services
image_processor = ImageProcessor()
auto_tagging = AutoTaggingService()

@router.get("/items", response_model=List[WardrobeItemResponse])
async def get_wardrobe_items(
    category: Optional[str] = Query(None),
    color: Optional[str] = Query(None),
    style: Optional[str] = Query(None),
    season: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's wardrobe items with optional filtering
    """
    try:
        db = get_database()
        
        # Build filter query
        filter_query = {"user_id": current_user.id, "is_active": True}
        
        if category:
            filter_query["ai_tags.category"] = category
        if color:
            filter_query["ai_tags.colors"] = {"$in": [color]}
        if style:
            filter_query["ai_tags.style"] = style
        if season:
            filter_query["ai_tags.season"] = {"$in": [season]}
        
        # Get items with pagination
        skip = (page - 1) * limit
        items = await db.wardrobe_items.find(filter_query).skip(skip).limit(limit).to_list(length=limit)
        
        # Convert to response format
        item_responses = [WardrobeItemResponse(**item) for item in items]
        
        return item_responses
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get wardrobe items: {str(e)}"
        )

@router.post("/items", response_model=WardrobeItemResponse)
async def create_wardrobe_item(
    item_data: WardrobeItemCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new wardrobe item
    """
    try:
        db = get_database()
        
        # Process images
        processed_images = []
        for image in item_data.images:
            # Enhance image
            enhanced_image = await image_processor.enhance_photo(image.original)
            
            # Create thumbnail
            thumbnail = await image_processor.create_thumbnail(enhanced_image)
            
            processed_images.append({
                "original": image.original,
                "processed": enhanced_image,
                "thumbnail": thumbnail,
                "width": image.width,
                "height": image.height,
                "file_size": image.file_size
            })
        
        # Auto-tag the item
        ai_tags = await auto_tagging.analyze_item(processed_images[0]["processed"])
        
        # Create wardrobe item
        wardrobe_item = WardrobeItem(
            user_id=current_user.id,
            images=processed_images,
            ai_tags=ai_tags,
            metadata=item_data.metadata or {},
            organization=item_data.organization or {}
        )
        
        # Save to database
        result = await db.wardrobe_items.insert_one(wardrobe_item.dict(by_alias=True))
        wardrobe_item.id = result.inserted_id
        
        return WardrobeItemResponse(**wardrobe_item.dict(by_alias=True))
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create wardrobe item: {str(e)}"
        )

@router.get("/items/{item_id}", response_model=WardrobeItemResponse)
async def get_wardrobe_item(
    item_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific wardrobe item
    """
    try:
        db = get_database()
        
        item = await db.wardrobe_items.find_one({
            "_id": ObjectId(item_id),
            "user_id": current_user.id
        })
        
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wardrobe item not found"
            )
        
        return WardrobeItemResponse(**item)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get wardrobe item: {str(e)}"
        )

@router.put("/items/{item_id}", response_model=WardrobeItemResponse)
async def update_wardrobe_item(
    item_id: str,
    item_update: WardrobeItemUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update a wardrobe item
    """
    try:
        db = get_database()
        
        # Check if item exists and belongs to user
        existing_item = await db.wardrobe_items.find_one({
            "_id": ObjectId(item_id),
            "user_id": current_user.id
        })
        
        if not existing_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wardrobe item not found"
            )
        
        # Prepare update data
        update_data = item_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        # Update item
        await db.wardrobe_items.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": update_data}
        )
        
        # Get updated item
        updated_item = await db.wardrobe_items.find_one({"_id": ObjectId(item_id)})
        return WardrobeItemResponse(**updated_item)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update wardrobe item: {str(e)}"
        )

@router.delete("/items/{item_id}")
async def delete_wardrobe_item(
    item_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete a wardrobe item
    """
    try:
        db = get_database()
        
        # Soft delete - mark as inactive
        result = await db.wardrobe_items.update_one(
            {"_id": ObjectId(item_id), "user_id": current_user.id},
            {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wardrobe item not found"
            )
        
        return {"message": "Wardrobe item deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete wardrobe item: {str(e)}"
        )

@router.post("/bulk-upload")
async def bulk_upload_items(
    request: BulkUploadRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Bulk upload wardrobe items
    """
    try:
        db = get_database()
        
        uploaded_items = []
        failed_items = []
        
        for item_data in request.items:
            try:
                # Process images
                processed_images = []
                for image in item_data.images:
                    enhanced_image = await image_processor.enhance_photo(image.original)
                    thumbnail = await image_processor.create_thumbnail(enhanced_image)
                    
                    processed_images.append({
                        "original": image.original,
                        "processed": enhanced_image,
                        "thumbnail": thumbnail,
                        "width": image.width,
                        "height": image.height,
                        "file_size": image.file_size
                    })
                
                # Auto-tag if enabled
                if request.auto_process:
                    ai_tags = await auto_tagging.analyze_item(processed_images[0]["processed"])
                else:
                    ai_tags = {
                        "category": "unknown",
                        "subcategory": "unknown",
                        "colors": [],
                        "style": "unknown",
                        "pattern": "unknown",
                        "season": [],
                        "occasion": [],
                        "confidence_score": 0.0
                    }
                
                # Create wardrobe item
                wardrobe_item = WardrobeItem(
                    user_id=current_user.id,
                    images=processed_images,
                    ai_tags=ai_tags,
                    metadata=item_data.metadata or {},
                    organization=item_data.organization or {}
                )
                
                # Save to database
                result = await db.wardrobe_items.insert_one(wardrobe_item.dict(by_alias=True))
                uploaded_items.append(str(result.inserted_id))
                
            except Exception as e:
                failed_items.append({"item": item_data.dict(), "error": str(e)})
        
        return {
            "message": f"Bulk upload completed. {len(uploaded_items)} items uploaded successfully.",
            "uploaded_items": uploaded_items,
            "failed_items": failed_items,
            "total_uploaded": len(uploaded_items),
            "total_failed": len(failed_items)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Bulk upload failed: {str(e)}"
        )

@router.post("/ai/process-image")
async def process_image_with_ai(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Process image with AI for auto-tagging
    """
    try:
        # Validate file
        if not validate_file_extension(file.filename, ["jpg", "jpeg", "png", "webp"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file format. Only JPG, JPEG, PNG, and WEBP are allowed"
            )
        
        # Read file content
        file_content = await file.read()
        if not validate_file_size(len(file_content), 10 * 1024 * 1024):  # 10MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File too large. Maximum size is 10MB"
            )
        
        # Save file temporarily
        import uuid
        filename = f"temp_{uuid.uuid4().hex}.{file.filename.split('.')[-1]}"
        filepath = f"temp_images/{filename}"
        
        import os
        os.makedirs("temp_images", exist_ok=True)
        
        with open(filepath, "wb") as f:
            f.write(file_content)
        
        # Process image
        enhanced_image = await image_processor.enhance_photo(filepath)
        
        # Auto-tag
        ai_tags = await auto_tagging.analyze_item(enhanced_image)
        
        # Extract colors
        colors = await image_processor.extract_dominant_colors(enhanced_image)
        
        return {
            "ai_tags": ai_tags,
            "colors": colors,
            "processed_image": enhanced_image
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image processing failed: {str(e)}"
        )

@router.get("/search")
async def search_wardrobe_items(
    query: str = Query(...),
    filters: Optional[WardrobeFilter] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Search wardrobe items with natural language
    """
    try:
        db = get_database()
        
        # Build search query
        search_query = {"user_id": current_user.id, "is_active": True}
        
        # Add text search
        if query:
            search_query["$text"] = {"$search": query}
        
        # Add filters
        if filters:
            if filters.category:
                search_query["ai_tags.category"] = filters.category
            if filters.colors:
                search_query["ai_tags.colors"] = {"$in": filters.colors}
            if filters.style:
                search_query["ai_tags.style"] = filters.style
            if filters.season:
                search_query["ai_tags.season"] = {"$in": filters.season}
            if filters.occasion:
                search_query["ai_tags.occasion"] = {"$in": filters.occasion}
            if filters.collections:
                search_query["organization.collections"] = {"$in": filters.collections}
            if filters.custom_tags:
                search_query["organization.custom_tags"] = {"$in": filters.custom_tags}
            if filters.favorite is not None:
                search_query["usage_stats.favorite"] = filters.favorite
            if filters.min_rating:
                search_query["usage_stats.rating"] = {"$gte": filters.min_rating}
            if filters.max_rating:
                search_query["usage_stats.rating"] = {"$lte": filters.max_rating}
        
        # Get items with pagination
        skip = (page - 1) * limit
        items = await db.wardrobe_items.find(search_query).skip(skip).limit(limit).to_list(length=limit)
        
        # Convert to response format
        item_responses = [WardrobeItemResponse(**item) for item in items]
        
        return {
            "items": item_responses,
            "total_count": len(item_responses),
            "page": page,
            "limit": limit
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )

@router.get("/categories")
async def get_wardrobe_categories(current_user: User = Depends(get_current_user)):
    """
    Get wardrobe categories and their counts
    """
    try:
        db = get_database()
        
        # Aggregate categories
        pipeline = [
            {"$match": {"user_id": current_user.id, "is_active": True}},
            {"$group": {
                "_id": "$ai_tags.category",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}}
        ]
        
        categories = await db.wardrobe_items.aggregate(pipeline).to_list(length=None)
        
        return {"categories": categories}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get categories: {str(e)}"
        )

@router.get("/colors")
async def get_wardrobe_colors(current_user: User = Depends(get_current_user)):
    """
    Get wardrobe colors and their counts
    """
    try:
        db = get_database()
        
        # Aggregate colors
        pipeline = [
            {"$match": {"user_id": current_user.id, "is_active": True}},
            {"$unwind": "$ai_tags.colors"},
            {"$group": {
                "_id": "$ai_tags.colors",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}}
        ]
        
        colors = await db.wardrobe_items.aggregate(pipeline).to_list(length=None)
        
        return {"colors": colors}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get colors: {str(e)}"
        )
