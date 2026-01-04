from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from app.models.user import User
from app.models.virtual_tryon import (
    VirtualTryOnRequest, VirtualTryOnResponse, BatchGenerationRequest, 
    BatchGenerationResponse, TryOnRating, ReferencePhoto, PoseData
)
from app.services.ai.virtual_tryon_service import VirtualTryOnService
from app.services.ai.pose_detection import PoseDetector
from app.services.ai.image_processing import ImageProcessor
from app.services.database.mongodb import get_database
from app.utils.auth import get_current_user
from app.utils.validators import validate_file_extension, validate_file_size

router = APIRouter()

# Initialize services
virtual_tryon_service = VirtualTryOnService()
pose_detector = PoseDetector()
image_processor = ImageProcessor()

@router.post("/upload-reference", response_model=dict)
async def upload_reference_photo(
    pose_type: str = Form(...),
    is_primary: bool = Form(False),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload reference photo for virtual try-on
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
        filename = f"reference_{uuid.uuid4().hex}.{file.filename.split('.')[-1]}"
        filepath = f"temp_images/{filename}"
        
        import os
        os.makedirs("temp_images", exist_ok=True)
        
        with open(filepath, "wb") as f:
            f.write(file_content)
        
        # Process image
        enhanced_image = await image_processor.enhance_photo(filepath)
        
        # Analyze pose
        pose_data = await pose_detector.analyze_pose(enhanced_image)
        
        # Save to database
        db = get_database()
        
        # Get or create virtual try-on profile
        profile = await db.virtual_tryon_profiles.find_one({"user_id": current_user.id})
        
        if not profile:
            profile = {
                "user_id": current_user.id,
                "reference_photos": [],
                "generation_requests": [],
                "preferences": {
                    "default_pose": "standing",
                    "quality_preference": "high",
                    "auto_save": True,
                    "background_style": "original"
                },
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            result = await db.virtual_tryon_profiles.insert_one(profile)
            profile["_id"] = result.inserted_id
        
        # Create reference photo data
        reference_photo = ReferencePhoto(
            pose_type=pose_type,
            image_url=enhanced_image,
            pose_data=PoseData(**pose_data),
            is_primary=is_primary
        )
        
        # Update profile with new reference photo
        await db.virtual_tryon_profiles.update_one(
            {"_id": profile["_id"]},
            {
                "$push": {"reference_photos": reference_photo.dict()},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        return {
            "message": "Reference photo uploaded successfully",
            "photo_id": str(reference_photo.id),
            "pose_type": pose_type,
            "pose_data": pose_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Reference photo upload failed: {str(e)}"
        )

@router.get("/reference-photos")
async def get_reference_photos(current_user: User = Depends(get_current_user)):
    """
    Get user's reference photos
    """
    try:
        db = get_database()
        
        profile = await db.virtual_tryon_profiles.find_one({"user_id": current_user.id})
        
        if not profile:
            return {"reference_photos": []}
        
        return {
            "reference_photos": profile.get("reference_photos", []),
            "preferences": profile.get("preferences", {})
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get reference photos: {str(e)}"
        )

@router.delete("/reference-photos/{photo_id}")
async def delete_reference_photo(
    photo_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete a reference photo
    """
    try:
        db = get_database()
        
        # Remove photo from profile
        result = await db.virtual_tryon_profiles.update_one(
            {"user_id": current_user.id},
            {
                "$pull": {"reference_photos": {"id": ObjectId(photo_id)}},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reference photo not found"
            )
        
        return {"message": "Reference photo deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete reference photo: {str(e)}"
        )

@router.post("/generate", response_model=VirtualTryOnResponse)
async def generate_virtual_tryon(
    request: VirtualTryOnRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate virtual try-on image
    """
    try:
        db = get_database()
        
        # Get user's virtual try-on profile
        profile = await db.virtual_tryon_profiles.find_one({"user_id": current_user.id})
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No reference photos found. Please upload reference photos first."
            )
        
        # Get reference photo for the requested pose
        reference_photos = profile.get("reference_photos", [])
        reference_photo = None
        
        for photo in reference_photos:
            if photo.get("pose_type") == request.pose_type:
                reference_photo = photo
                break
        
        if not reference_photo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No reference photo found for pose type: {request.pose_type}"
            )
        
        # Get outfit items
        outfit = await db.outfits.find_one({"_id": ObjectId(request.outfit_id)})
        if not outfit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Outfit not found"
            )
        
        # Get outfit item details
        outfit_items = []
        for item in outfit.get("items", []):
            item_detail = await db.wardrobe_items.find_one({"_id": item["item_id"]})
            if item_detail:
                outfit_items.append({
                    "category": item_detail.get("ai_tags", {}).get("category", ""),
                    "subcategory": item_detail.get("ai_tags", {}).get("subcategory", ""),
                    "color": item_detail.get("ai_tags", {}).get("colors", [""])[0],
                    "style": item_detail.get("ai_tags", {}).get("style", ""),
                    "pattern": item_detail.get("ai_tags", {}).get("pattern", "")
                })
        
        # Generate virtual try-on
        result = await virtual_tryon_service.generate_outfit_on_user(
            user_photo=reference_photo["image_url"],
            outfit_items=outfit_items,
            pose_type=request.pose_type,
            quality_preference=request.quality_preference
        )
        
        # Save generation result
        generation_result = {
            "user_id": current_user.id,
            "outfit_id": ObjectId(request.outfit_id),
            "pose_type": request.pose_type,
            "generated_image": result["generated_image"],
            "quality_rating": result.get("quality_score", 0.0),
            "generation_time": result.get("generation_time", 0.0),
            "ai_service_used": result.get("ai_service", "unknown"),
            "metadata": result.get("metadata", {}),
            "is_successful": True,
            "created_at": datetime.utcnow()
        }
        
        generation_id = await db.generation_results.insert_one(generation_result)
        
        # Update profile with generation request
        await db.virtual_tryon_profiles.update_one(
            {"user_id": current_user.id},
            {
                "$push": {"generation_requests": generation_id.inserted_id},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        return VirtualTryOnResponse(
            id=str(generation_id.inserted_id),
            user_id=str(current_user.id),
            outfit_id=str(request.outfit_id),
            generated_image=result["generated_image"],
            pose_type=request.pose_type,
            quality_rating=result.get("quality_score"),
            generation_time=result.get("generation_time", 0.0),
            ai_service_used=result.get("ai_service", "unknown"),
            created_at=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Virtual try-on generation failed: {str(e)}"
        )

@router.post("/batch-generate", response_model=BatchGenerationResponse)
async def batch_generate_virtual_tryon(
    request: BatchGenerationRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate multiple virtual try-on images in batch
    """
    try:
        # Get user's reference photos
        db = get_database()
        profile = await db.virtual_tryon_profiles.find_one({"user_id": current_user.id})
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No reference photos found. Please upload reference photos first."
            )
        
        # Get primary reference photo
        reference_photos = profile.get("reference_photos", [])
        primary_photo = None
        
        for photo in reference_photos:
            if photo.get("is_primary", False):
                primary_photo = photo
                break
        
        if not primary_photo:
            primary_photo = reference_photos[0] if reference_photos else None
        
        if not primary_photo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No reference photos available"
            )
        
        # Prepare batch requests
        batch_requests = []
        for outfit_id in request.outfit_ids:
            for pose_type in request.pose_types:
                batch_requests.append({
                    "outfit_id": str(outfit_id),
                    "pose_type": pose_type,
                    "quality_preference": request.quality_preference
                })
        
        # Generate batch results
        results = []
        successful_generations = 0
        failed_generations = 0
        
        for batch_request in batch_requests:
            try:
                # Get outfit items
                outfit = await db.outfits.find_one({"_id": ObjectId(batch_request["outfit_id"])})
                if not outfit:
                    failed_generations += 1
                    continue
                
                # Get outfit item details
                outfit_items = []
                for item in outfit.get("items", []):
                    item_detail = await db.wardrobe_items.find_one({"_id": item["item_id"]})
                    if item_detail:
                        outfit_items.append({
                            "category": item_detail.get("ai_tags", {}).get("category", ""),
                            "subcategory": item_detail.get("ai_tags", {}).get("subcategory", ""),
                            "color": item_detail.get("ai_tags", {}).get("colors", [""])[0],
                            "style": item_detail.get("ai_tags", {}).get("style", ""),
                            "pattern": item_detail.get("ai_tags", {}).get("pattern", "")
                        })
                
                # Generate virtual try-on
                result = await virtual_tryon_service.generate_outfit_on_user(
                    user_photo=primary_photo["image_url"],
                    outfit_items=outfit_items,
                    pose_type=batch_request["pose_type"],
                    quality_preference=batch_request["quality_preference"]
                )
                
                # Save generation result
                generation_result = {
                    "user_id": current_user.id,
                    "outfit_id": ObjectId(batch_request["outfit_id"]),
                    "pose_type": batch_request["pose_type"],
                    "generated_image": result["generated_image"],
                    "quality_rating": result.get("quality_score", 0.0),
                    "generation_time": result.get("generation_time", 0.0),
                    "ai_service_used": result.get("ai_service", "unknown"),
                    "metadata": result.get("metadata", {}),
                    "is_successful": True,
                    "created_at": datetime.utcnow()
                }
                
                generation_id = await db.generation_results.insert_one(generation_result)
                
                results.append(VirtualTryOnResponse(
                    id=str(generation_id.inserted_id),
                    user_id=str(current_user.id),
                    outfit_id=str(batch_request["outfit_id"]),
                    generated_image=result["generated_image"],
                    pose_type=batch_request["pose_type"],
                    quality_rating=result.get("quality_score"),
                    generation_time=result.get("generation_time", 0.0),
                    ai_service_used=result.get("ai_service", "unknown"),
                    created_at=datetime.utcnow()
                ))
                
                successful_generations += 1
                
            except Exception as e:
                failed_generations += 1
                continue
        
        return BatchGenerationResponse(
            batch_id=str(ObjectId()),
            total_requests=len(batch_requests),
            successful_generations=successful_generations,
            failed_generations=failed_generations,
            results=results,
            created_at=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch generation failed: {str(e)}"
        )

@router.get("/history")
async def get_generation_history(
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    """
    Get user's virtual try-on generation history
    """
    try:
        history = await virtual_tryon_service.get_generation_history(str(current_user.id), limit)
        
        return {
            "generations": history,
            "total_count": len(history)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get generation history: {str(e)}"
        )

@router.post("/rate")
async def rate_generation_quality(
    generation_id: str,
    rating: int,
    feedback: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Rate the quality of a generated image
    """
    try:
        if rating < 1 or rating > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rating must be between 1 and 5"
            )
        
        success = await virtual_tryon_service.rate_generation_quality(
            generation_id=generation_id,
            rating=rating,
            feedback=feedback
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Generation not found"
            )
        
        return {"message": "Rating submitted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit rating: {str(e)}"
        )

@router.delete("/generations/{generation_id}")
async def delete_generation(
    generation_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete a specific generation result
    """
    try:
        success = await virtual_tryon_service.delete_generation(
            generation_id=generation_id,
            user_id=str(current_user.id)
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Generation not found"
            )
        
        return {"message": "Generation deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete generation: {str(e)}"
        )
