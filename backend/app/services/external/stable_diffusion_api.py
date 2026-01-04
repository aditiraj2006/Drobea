import aiohttp
import asyncio
import base64
import os
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class StableDiffusionClient:
    def __init__(self):
        self.api_url = os.getenv("STABLE_DIFFUSION_API_URL", "http://localhost:7860")
        self.api_key = os.getenv("STABLE_DIFFUSION_API_KEY")
        self.headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
    
    async def generate_virtual_tryon(
        self, 
        user_photo: str, 
        outfit_description: str, 
        pose_data: Dict[str, Any],
        quality_preference: str = "high"
    ) -> Dict[str, Any]:
        """
        Generate virtual try-on image using Stable Diffusion API
        """
        try:
            # Load and encode user photo
            with open(user_photo, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Create prompt for Stable Diffusion
            prompt = self._create_sd_prompt(outfit_description, pose_data)
            
            # Prepare API request
            payload = {
                "prompt": prompt,
                "negative_prompt": self._get_negative_prompt(),
                "init_images": [image_data],
                "width": self._get_image_width(quality_preference),
                "height": self._get_image_height(quality_preference),
                "num_inference_steps": self._get_inference_steps(quality_preference),
                "guidance_scale": 7.5,
                "strength": 0.8,
                "seed": -1,
                "sampler_name": "DPM++ 2M Karras",
                "controlnet_units": [
                    {
                        "input_image": image_data,
                        "module": "openpose",
                        "model": "control_v11p_sd15_openpose",
                        "weight": 1.0,
                        "resize_mode": 1,
                        "lowvram": False,
                        "processor_res": 512,
                        "threshold_a": 64,
                        "threshold_b": 64,
                        "guidance_start": 0.0,
                        "guidance_end": 1.0,
                        "pixel_perfect": True
                    }
                ]
            }
            
            # Make API request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/sdapi/v1/img2img",
                    json=payload,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=300)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        # Process the result
                        if result.get("images"):
                            generated_image = result["images"][0]
                            
                            # Save generated image
                            generated_path = await self._save_generated_image(generated_image)
                            
                            return {
                                "generated_image": generated_path,
                                "quality_score": self._calculate_quality_score(result),
                                "generation_time": result.get("info", {}).get("duration", 0),
                                "ai_service": "stable_diffusion",
                                "metadata": {
                                    "model": "stable_diffusion_1.5",
                                    "quality_preference": quality_preference,
                                    "pose_type": pose_data.get("pose_type", "standing"),
                                    "inference_steps": payload["num_inference_steps"],
                                    "guidance_scale": payload["guidance_scale"]
                                }
                            }
                        else:
                            raise Exception("No images generated")
                    else:
                        error_text = await response.text()
                        raise Exception(f"API request failed: {response.status} - {error_text}")
                        
        except Exception as e:
            logger.error(f"Stable Diffusion generation failed: {e}")
            raise
    
    def _create_sd_prompt(self, outfit_description: str, pose_data: Dict[str, Any]) -> str:
        """Create optimized prompt for Stable Diffusion"""
        pose_type = pose_data.get("pose_type", "standing")
        
        # Base prompt components
        base_prompt = "photorealistic, high quality, detailed, professional photography"
        pose_prompt = self._get_pose_prompt(pose_type)
        outfit_prompt = f"person wearing {outfit_description}"
        quality_prompt = "8k resolution, sharp focus, perfect lighting, natural shadows"
        
        # Combine prompts
        full_prompt = f"{base_prompt}, {pose_prompt}, {outfit_prompt}, {quality_prompt}"
        
        return full_prompt
    
    def _get_pose_prompt(self, pose_type: str) -> str:
        """Get pose-specific prompt for Stable Diffusion"""
        pose_prompts = {
            "standing": "person standing upright, full body visible, natural pose",
            "standing_front": "person standing facing camera, full body visible, confident pose",
            "standing_side": "person standing in profile, side view, elegant pose",
            "walking": "person walking naturally, dynamic pose, movement captured",
            "sitting": "person sitting naturally, relaxed pose, good posture",
            "dynamic_front": "person in dynamic pose facing camera, energetic stance",
            "dynamic_side": "person in dynamic pose side view, athletic stance"
        }
        
        return pose_prompts.get(pose_type, "person in natural pose")
    
    def _get_negative_prompt(self) -> str:
        """Get negative prompt to avoid unwanted elements"""
        return ("blurry, low quality, distorted, deformed, ugly, bad anatomy, "
                "bad proportions, extra limbs, missing limbs, mutated hands, "
                "poorly drawn hands, poorly drawn face, mutation, deformed, "
                "bad anatomy, bad proportions, extra limbs, cloned face, "
                "disfigured, out of frame, ugly, extra limbs, bad anatomy, "
                "gross proportions, malformed limbs, missing arms, missing legs, "
                "extra arms, extra legs, mutated hands, fused fingers, "
                "too many fingers, long neck, cross-eyed, mutated, "
                "bad anatomy, bad proportions, gross proportions, "
                "text, watermark, signature, username, artist name")
    
    def _get_image_width(self, quality_preference: str) -> int:
        """Get image width based on quality preference"""
        quality_settings = {
            "low": 512,
            "medium": 768,
            "high": 1024,
            "ultra": 1536
        }
        return quality_settings.get(quality_preference, 1024)
    
    def _get_image_height(self, quality_preference: str) -> int:
        """Get image height based on quality preference"""
        quality_settings = {
            "low": 512,
            "medium": 768,
            "high": 1024,
            "ultra": 1536
        }
        return quality_settings.get(quality_preference, 1024)
    
    def _get_inference_steps(self, quality_preference: str) -> int:
        """Get number of inference steps based on quality preference"""
        quality_settings = {
            "low": 20,
            "medium": 30,
            "high": 50,
            "ultra": 100
        }
        return quality_settings.get(quality_preference, 50)
    
    def _calculate_quality_score(self, result: Dict[str, Any]) -> float:
        """Calculate quality score based on generation parameters"""
        info = result.get("info", {})
        
        # Base score from inference steps
        inference_steps = info.get("steps", 20)
        base_score = min(inference_steps / 100.0, 1.0)
        
        # Adjust based on guidance scale
        guidance_scale = info.get("cfg_scale", 7.5)
        if 7.0 <= guidance_scale <= 8.0:
            base_score += 0.1
        
        # Adjust based on image dimensions
        width = info.get("width", 512)
        height = info.get("height", 512)
        if width >= 1024 and height >= 1024:
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    async def _save_generated_image(self, image_data: str) -> str:
        """Save generated image to file"""
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            
            # Save to file
            import uuid
            filename = f"generated_{uuid.uuid4().hex}.png"
            filepath = f"generated_images/{filename}"
            
            # Create directory if it doesn't exist
            os.makedirs("generated_images", exist_ok=True)
            
            with open(filepath, 'wb') as f:
                f.write(image_bytes)
            
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to save generated image: {e}")
            raise
    
    async def generate_outfit_variations(
        self, 
        base_outfit: str, 
        variations: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple variations of an outfit
        """
        try:
            results = []
            
            for variation in variations:
                # Create variation prompt
                prompt = f"{base_outfit}, {variation}, photorealistic, high quality"
                
                payload = {
                    "prompt": prompt,
                    "negative_prompt": self._get_negative_prompt(),
                    "width": 1024,
                    "height": 1024,
                    "num_inference_steps": 50,
                    "guidance_scale": 7.5,
                    "seed": -1
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.api_url}/sdapi/v1/txt2img",
                        json=payload,
                        headers=self.headers,
                        timeout=aiohttp.ClientTimeout(total=300)
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            
                            if result.get("images"):
                                generated_image = result["images"][0]
                                generated_path = await self._save_generated_image(generated_image)
                                
                                results.append({
                                    "variation": variation,
                                    "image_path": generated_path,
                                    "quality_score": self._calculate_quality_score(result)
                                })
            
            return results
            
        except Exception as e:
            logger.error(f"Outfit variation generation failed: {e}")
            raise
    
    async def upscale_image(self, image_path: str, scale_factor: int = 2) -> str:
        """
        Upscale image using Stable Diffusion upscaler
        """
        try:
            # Load and encode image
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            payload = {
                "image": image_data,
                "scale": scale_factor,
                "upscaler": "R-ESRGAN 4x+",
                "upscaling_resize": scale_factor
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/sdapi/v1/extra-single-image",
                    json=payload,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=300)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        if result.get("image"):
                            upscaled_image = result["image"]
                            
                            # Save upscaled image
                            upscaled_path = image_path.replace('.', f'_upscaled_{scale_factor}x.')
                            with open(upscaled_path, 'wb') as f:
                                f.write(base64.b64decode(upscaled_image))
                            
                            return upscaled_path
                        else:
                            raise Exception("No upscaled image returned")
                    else:
                        error_text = await response.text()
                        raise Exception(f"Upscaling failed: {response.status} - {error_text}")
                        
        except Exception as e:
            logger.error(f"Image upscaling failed: {e}")
            raise
