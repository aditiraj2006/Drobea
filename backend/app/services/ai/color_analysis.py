import cv2
import numpy as np
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class ColorAnalysisService:
    def __init__(self):
        pass
    
    async def analyze_personal_colors(self, user_photos: List[str]) -> Dict[str, Any]:
        """
        Analyze user's personal color palette from photos
        """
        try:
            # Load and process photos
            skin_tones = []
            eye_colors = []
            hair_colors = []
            
            for photo_path in user_photos:
                image = cv2.imread(photo_path)
                if image is None:
                    continue
                
                # Extract features
                skin_tone = await self._extract_skin_tone(image)
                eye_color = await self._extract_eye_color(image)
                hair_color = await self._extract_hair_color(image)
                
                if skin_tone:
                    skin_tones.append(skin_tone)
                if eye_color:
                    eye_colors.append(eye_color)
                if hair_color:
                    hair_colors.append(hair_color)
            
            # Analyze color season
            color_season = await self._determine_color_season(skin_tones, eye_colors, hair_colors)
            
            # Generate color recommendations
            color_recommendations = await self._generate_color_recommendations(color_season)
            
            return {
                "color_season": color_season,
                "skin_tones": skin_tones,
                "eye_colors": eye_colors,
                "hair_colors": hair_colors,
                "recommended_colors": color_recommendations,
                "confidence_score": 0.8
            }
            
        except Exception as e:
            logger.error(f"Color analysis failed: {e}")
            return {
                "color_season": "unknown",
                "skin_tones": [],
                "eye_colors": [],
                "hair_colors": [],
                "recommended_colors": [],
                "confidence_score": 0.0
            }
    
    async def _extract_skin_tone(self, image: np.ndarray) -> str:
        """Extract skin tone from image"""
        try:
            # Convert to HSV for better skin detection
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Define skin color range
            lower_skin = np.array([0, 20, 70], dtype=np.uint8)
            upper_skin = np.array([20, 255, 255], dtype=np.uint8)
            
            # Create mask for skin
            mask = cv2.inRange(hsv, lower_skin, upper_skin)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return None
            
            # Get largest contour (likely face)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Get average color of skin region
            mask_skin = np.zeros_like(mask)
            cv2.drawContours(mask_skin, [largest_contour], -1, 255, -1)
            
            mean_color = cv2.mean(image, mask_skin)[:3]
            
            # Classify skin tone
            return self._classify_skin_tone(mean_color)
            
        except Exception as e:
            logger.error(f"Skin tone extraction failed: {e}")
            return None
    
    async def _extract_eye_color(self, image: np.ndarray) -> str:
        """Extract eye color from image"""
        try:
            # This would require face detection and eye region extraction
            # For now, return a placeholder
            return "brown"
            
        except Exception as e:
            logger.error(f"Eye color extraction failed: {e}")
            return None
    
    async def _extract_hair_color(self, image: np.ndarray) -> str:
        """Extract hair color from image"""
        try:
            # This would require face detection and hair region extraction
            # For now, return a placeholder
            return "brown"
            
        except Exception as e:
            logger.error(f"Hair color extraction failed: {e}")
            return None
    
    def _classify_skin_tone(self, rgb_color: tuple) -> str:
        """Classify skin tone based on RGB values"""
        r, g, b = rgb_color
        
        # Simple skin tone classification
        if r > 200 and g > 180 and b > 160:
            return "fair"
        elif r > 180 and g > 160 and b > 140:
            return "light"
        elif r > 160 and g > 140 and b > 120:
            return "medium"
        elif r > 140 and g > 120 and b > 100:
            return "olive"
        elif r > 120 and g > 100 and b > 80:
            return "tan"
        else:
            return "deep"
    
    async def _determine_color_season(self, skin_tones: List[str], eye_colors: List[str], hair_colors: List[str]) -> str:
        """Determine color season based on features"""
        try:
            # Get most common features
            most_common_skin = max(set(skin_tones), key=skin_tones.count) if skin_tones else "medium"
            most_common_eye = max(set(eye_colors), key=eye_colors.count) if eye_colors else "brown"
            most_common_hair = max(set(hair_colors), key=hair_colors.count) if hair_colors else "brown"
            
            # Simple season determination
            if most_common_skin in ["fair", "light"] and most_common_eye in ["blue", "green"]:
                return "spring"
            elif most_common_skin in ["fair", "light"] and most_common_eye in ["brown", "hazel"]:
                return "summer"
            elif most_common_skin in ["medium", "olive"] and most_common_eye in ["brown", "hazel"]:
                return "autumn"
            elif most_common_skin in ["deep", "tan"] and most_common_eye in ["brown", "dark"]:
                return "winter"
            else:
                return "neutral"
                
        except Exception as e:
            logger.error(f"Color season determination failed: {e}")
            return "neutral"
    
    async def _generate_color_recommendations(self, color_season: str) -> List[str]:
        """Generate color recommendations based on color season"""
        color_palettes = {
            "spring": ["coral", "peach", "mint", "lavender", "camel", "cream"],
            "summer": ["powder_blue", "rose", "lavender", "mint", "gray", "white"],
            "autumn": ["burgundy", "mustard", "olive", "rust", "camel", "brown"],
            "winter": ["navy", "emerald", "crimson", "silver", "black", "white"],
            "neutral": ["navy", "gray", "white", "black", "beige", "camel"]
        }
        
        return color_palettes.get(color_season, color_palettes["neutral"])
    
    async def analyze_color_harmony(self, colors: List[str]) -> Dict[str, Any]:
        """Analyze color harmony between colors"""
        try:
            # Simple color harmony analysis
            harmony_type = self._determine_harmony_type(colors)
            complementary_colors = self._get_complementary_colors(colors)
            color_temperature = self._analyze_color_temperature(colors)
            
            return {
                "harmony_type": harmony_type,
                "complementary_colors": complementary_colors,
                "color_temperature": color_temperature,
                "recommendations": self._get_harmony_recommendations(harmony_type)
            }
            
        except Exception as e:
            logger.error(f"Color harmony analysis failed: {e}")
            return {
                "harmony_type": "unknown",
                "complementary_colors": [],
                "color_temperature": "neutral",
                "recommendations": []
            }
    
    def _determine_harmony_type(self, colors: List[str]) -> str:
        """Determine color harmony type"""
        if len(colors) <= 1:
            return "monochromatic"
        
        # Simple harmony classification
        warm_colors = ["red", "orange", "yellow", "pink", "coral", "peach"]
        cool_colors = ["blue", "green", "purple", "teal", "mint", "lavender"]
        
        has_warm = any(color in warm_colors for color in colors)
        has_cool = any(color in cool_colors for color in colors)
        
        if has_warm and not has_cool:
            return "warm_analogous"
        elif has_cool and not has_warm:
            return "cool_analogous"
        elif has_warm and has_cool:
            return "complementary"
        else:
            return "neutral"
    
    def _get_complementary_colors(self, colors: List[str]) -> List[str]:
        """Get complementary colors"""
        complementary_map = {
            "red": "green",
            "blue": "orange",
            "yellow": "purple",
            "green": "red",
            "orange": "blue",
            "purple": "yellow"
        }
        
        complementary = []
        for color in colors:
            if color in complementary_map:
                complementary.append(complementary_map[color])
        
        return complementary
    
    def _analyze_color_temperature(self, colors: List[str]) -> str:
        """Analyze color temperature"""
        warm_colors = ["red", "orange", "yellow", "pink", "coral", "peach"]
        cool_colors = ["blue", "green", "purple", "teal", "mint", "lavender"]
        
        warm_count = sum(1 for color in colors if color in warm_colors)
        cool_count = sum(1 for color in colors if color in cool_colors)
        
        if warm_count > cool_count:
            return "warm"
        elif cool_count > warm_count:
            return "cool"
        else:
            return "neutral"
    
    def _get_harmony_recommendations(self, harmony_type: str) -> List[str]:
        """Get harmony recommendations"""
        recommendations = {
            "monochromatic": ["Add different shades of the same color for depth"],
            "warm_analogous": ["Perfect for creating a cohesive warm look"],
            "cool_analogous": ["Great for a calm and serene appearance"],
            "complementary": ["Bold and striking combination"],
            "neutral": ["Safe and versatile color combination"]
        }
        
        return recommendations.get(harmony_type, ["Consider adding more color variety"])
