import asyncio
import base64
import io
from typing import List, Dict, Any, Optional
from PIL import Image
import google.generativeai as genai
import aiohttp
import json
import os
from app.models.virtual_tryon import VirtualTryOnRequest, GenerationResult, PoseData
from app.services.external.gemini_api import GeminiClient
from app.services.external.stable_diffusion_api import StableDiffusionClient
from app.services.ai.pose_detection import PoseDetector
from app.services.ai.image_processing import ImageProcessor
import logging

logger = logging.getLogger(__name__)

class VirtualTryOnService:
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.sd_client = StableDiffusionClient()
        self.pose_detector = PoseDetector()
        self.image_processor = ImageProcessor()
        
    async def generate_outfit_on_user(
        self, 
        user_photo: str, 
        outfit_items: List[Dict[str, Any]], 
        pose_type: str = "standing",
        quality_preference: str = "high"
    ) -> Dict[str, Any]:
        """
        Generate virtual try-on image using AI services
        """
        try:
            # Step 1: Analyze user pose and body proportions
            pose_data = await self.pose_detector.analyze_pose(user_photo)
            
            # Step 2: Process and enhance user photo
            processed_photo = await self.image_processor.enhance_photo(user_photo)
            
            # Step 3: Create detailed outfit description
            outfit_description = self._create_outfit_prompt(outfit_items, pose_type)
            
            # Step 4: Generate AI image with primary service (Gemini)
            try:
                result = await self.gemini_client.generate_virtual_tryon(
                    user_photo=processed_photo,
                    outfit_description=outfit_description,
                    pose_data=pose_data,
                    quality_preference=quality_preference
                )
                
                if result.get("quality_score", 0) >= 0.8:
                    return result
                    
            except Exception as e:
                logger.warning(f"Gemini generation failed: {e}, trying Stable Diffusion")
                
            # Step 5: Fallback to Stable Diffusion
            result = await self.sd_client.generate_virtual_tryon(
                user_photo=processed_photo,
                outfit_description=outfit_description,
                pose_data=pose_data,
                quality_preference=quality_preference
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Virtual try-on generation failed: {e}")
            raise
    
    def _create_outfit_prompt(self, outfit_items: List[Dict[str, Any]], pose_type: str) -> str:
        """Create detailed outfit description for AI generation"""
        outfit_details = []
        
        for item in outfit_items:
            category = item.get("category", "")
            subcategory = item.get("subcategory", "")
            color = item.get("color", "")
            style = item.get("style", "")
            pattern = item.get("pattern", "")
            
            item_desc = f"{color} {pattern} {style} {subcategory}"
            if category:
                item_desc = f"{category}: {item_desc}"
            
            outfit_details.append(item_desc)
        
        outfit_text = ", ".join(outfit_details)
        
        prompt = f"""
        Generate a photorealistic image of the person in the reference photo wearing this complete outfit:
        
        OUTFIT DETAILS:
        {outfit_text}
        
        CRITICAL REQUIREMENTS:
        1. Preserve the person's exact facial features, body shape, skin tone, and hair
        2. Maintain the identical pose, lighting, and background as the reference photo
        3. Ensure all clothing items fit naturally and realistically on the body
        4. Preserve accurate fabric textures, colors, and patterns from the outfit items
        5. Generate high-resolution, photorealistic output without any artificial look
        6. Maintain consistent shadows and lighting across the entire image
        7. Ensure proper clothing draping and natural folds
        8. Preserve all accessories and their proper placement
        
        Reference pose type: {pose_type}
        Image style: Photorealistic, natural lighting, high detail
        
        Do not alter the person's identity or physical characteristics in any way.
        """
        
        return prompt
    
    async def batch_generate(
        self, 
        user_photo: str, 
        outfit_requests: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate multiple virtual try-on images in batch"""
        results = []
        
        for request in outfit_requests:
            try:
                result = await self.generate_outfit_on_user(
                    user_photo=user_photo,
                    outfit_items=request["outfit_items"],
                    pose_type=request.get("pose_type", "standing"),
                    quality_preference=request.get("quality_preference", "high")
                )
                results.append({
                    "request_id": request.get("id"),
                    "result": result,
                    "success": True
                })
            except Exception as e:
                logger.error(f"Batch generation failed for request {request.get('id')}: {e}")
                results.append({
                    "request_id": request.get("id"),
                    "result": None,
                    "success": False,
                    "error": str(e)
                })
        
        return results
    
    async def rate_generation_quality(
        self, 
        generation_id: str, 
        rating: int, 
        feedback: Optional[str] = None
    ) -> bool:
        """Rate the quality of a generated image"""
        try:
            # Update the generation result with rating
            from app.services.database.mongodb import get_database
            db = get_database()
            
            await db.generation_results.update_one(
                {"_id": generation_id},
                {
                    "$set": {
                        "quality_rating": rating / 5.0,  # Convert to 0-1 scale
                        "feedback": feedback,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to rate generation: {e}")
            return False
    
    async def get_generation_history(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get user's virtual try-on generation history"""
        try:
            from app.services.database.mongodb import get_database
            from bson import ObjectId
            
            db = get_database()
            
            results = await db.generation_results.find(
                {"user_id": ObjectId(user_id)}
            ).sort("created_at", -1).limit(limit).to_list(length=limit)
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to get generation history: {e}")
            return []
    
    async def delete_generation(self, generation_id: str, user_id: str) -> bool:
        """Delete a specific generation result"""
        try:
            from app.services.database.mongodb import get_database
            from bson import ObjectId
            
            db = get_database()
            
            result = await db.generation_results.delete_one({
                "_id": ObjectId(generation_id),
                "user_id": ObjectId(user_id)
            })
            
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Failed to delete generation: {e}")
            return False
