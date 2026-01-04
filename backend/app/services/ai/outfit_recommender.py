from typing import Dict, Any, List, Optional
import random
import logging

logger = logging.getLogger(__name__)

class OutfitRecommender:
    def __init__(self):
        pass
    
    async def generate_outfit_suggestions(
        self,
        wardrobe_items: List[Dict[str, Any]],
        occasion: str,
        season: str,
        weather_conditions: List[str] = None,
        style_preferences: List[str] = None,
        color_preferences: List[str] = None,
        exclude_items: List[str] = None,
        include_items: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate outfit suggestions based on wardrobe items and preferences
        """
        try:
            suggestions = []
            
            # Filter items based on preferences
            filtered_items = self._filter_items(
                wardrobe_items, occasion, season, weather_conditions,
                style_preferences, color_preferences, exclude_items, include_items
            )
            
            # Group items by category
            categorized_items = self._categorize_items(filtered_items)
            
            # Generate outfit combinations
            for i in range(5):  # Generate 5 suggestions
                outfit = await self._create_outfit_combination(
                    categorized_items, occasion, season, weather_conditions
                )
                if outfit:
                    suggestions.append(outfit)
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Outfit suggestion generation failed: {e}")
            return []
    
    def _filter_items(
        self,
        wardrobe_items: List[Dict[str, Any]],
        occasion: str,
        season: str,
        weather_conditions: List[str],
        style_preferences: List[str],
        color_preferences: List[str],
        exclude_items: List[str],
        include_items: List[str]
    ) -> List[Dict[str, Any]]:
        """Filter wardrobe items based on preferences"""
        filtered = []
        
        for item in wardrobe_items:
            # Skip excluded items
            if exclude_items and str(item["_id"]) in exclude_items:
                continue
            
            # Must include specified items
            if include_items and str(item["_id"]) not in include_items:
                continue
            
            # Filter by occasion
            if occasion and not self._matches_occasion(item, occasion):
                continue
            
            # Filter by season
            if season and not self._matches_season(item, season):
                continue
            
            # Filter by weather
            if weather_conditions and not self._matches_weather(item, weather_conditions):
                continue
            
            # Filter by style preferences
            if style_preferences and not self._matches_style(item, style_preferences):
                continue
            
            # Filter by color preferences
            if color_preferences and not self._matches_colors(item, color_preferences):
                continue
            
            filtered.append(item)
        
        return filtered
    
    def _categorize_items(self, items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize items by type"""
        categorized = {
            "tops": [],
            "bottoms": [],
            "dresses": [],
            "shoes": [],
            "accessories": [],
            "outerwear": []
        }
        
        for item in items:
            category = item.get("ai_tags", {}).get("category", "unknown")
            if category in categorized:
                categorized[category].append(item)
            else:
                categorized["accessories"].append(item)
        
        return categorized
    
    async def _create_outfit_combination(
        self,
        categorized_items: Dict[str, List[Dict[str, Any]]],
        occasion: str,
        season: str,
        weather_conditions: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Create a single outfit combination"""
        try:
            outfit_items = []
            
            # Choose dress or top+bottom combination
            if categorized_items["dresses"] and random.random() < 0.3:
                # Choose a dress
                dress = random.choice(categorized_items["dresses"])
                outfit_items.append({
                    "item_id": str(dress["_id"]),
                    "category": "dress",
                    "name": dress.get("ai_tags", {}).get("subcategory", "dress")
                })
            else:
                # Choose top and bottom
                if categorized_items["tops"]:
                    top = random.choice(categorized_items["tops"])
                    outfit_items.append({
                        "item_id": str(top["_id"]),
                        "category": "top",
                        "name": top.get("ai_tags", {}).get("subcategory", "top")
                    })
                
                if categorized_items["bottoms"]:
                    bottom = random.choice(categorized_items["bottoms"])
                    outfit_items.append({
                        "item_id": str(bottom["_id"]),
                        "category": "bottom",
                        "name": bottom.get("ai_tags", {}).get("subcategory", "bottom")
                    })
            
            # Add shoes
            if categorized_items["shoes"]:
                shoes = random.choice(categorized_items["shoes"])
                outfit_items.append({
                    "item_id": str(shoes["_id"]),
                    "category": "shoes",
                    "name": shoes.get("ai_tags", {}).get("subcategory", "shoes")
                })
            
            # Add outerwear if needed
            if weather_conditions and any(condition in ["cold", "rainy", "windy"] for condition in weather_conditions):
                if categorized_items["outerwear"]:
                    outerwear = random.choice(categorized_items["outerwear"])
                    outfit_items.append({
                        "item_id": str(outerwear["_id"]),
                        "category": "outerwear",
                        "name": outerwear.get("ai_tags", {}).get("subcategory", "outerwear")
                    })
            
            # Add accessories
            if categorized_items["accessories"] and random.random() < 0.5:
                accessory = random.choice(categorized_items["accessories"])
                outfit_items.append({
                    "item_id": str(accessory["_id"]),
                    "category": "accessory",
                    "name": accessory.get("ai_tags", {}).get("subcategory", "accessory")
                })
            
            if not outfit_items:
                return None
            
            # Generate outfit name and description
            outfit_name = self._generate_outfit_name(outfit_items, occasion)
            description = self._generate_outfit_description(outfit_items, occasion, season)
            
            return {
                "outfit_id": f"outfit_{random.randint(1000, 9999)}",
                "name": outfit_name,
                "description": description,
                "items": outfit_items,
                "occasion": occasion,
                "season": season,
                "weather_conditions": weather_conditions or [],
                "confidence_score": random.uniform(0.7, 0.95)
            }
            
        except Exception as e:
            logger.error(f"Outfit combination creation failed: {e}")
            return None
    
    def _matches_occasion(self, item: Dict[str, Any], occasion: str) -> bool:
        """Check if item matches occasion"""
        item_occasions = item.get("ai_tags", {}).get("occasion", [])
        return occasion in item_occasions or not item_occasions
    
    def _matches_season(self, item: Dict[str, Any], season: str) -> bool:
        """Check if item matches season"""
        item_seasons = item.get("ai_tags", {}).get("season", [])
        return season in item_seasons or not item_seasons
    
    def _matches_weather(self, item: Dict[str, Any], weather_conditions: List[str]) -> bool:
        """Check if item matches weather conditions"""
        # Simple weather matching logic
        item_category = item.get("ai_tags", {}).get("category", "")
        
        if "cold" in weather_conditions and item_category in ["outerwear", "dress"]:
            return True
        if "rainy" in weather_conditions and item_category == "shoes":
            return True
        
        return True  # Default to true for most items
    
    def _matches_style(self, item: Dict[str, Any], style_preferences: List[str]) -> bool:
        """Check if item matches style preferences"""
        item_style = item.get("ai_tags", {}).get("style", "")
        return item_style in style_preferences or not style_preferences
    
    def _matches_colors(self, item: Dict[str, Any], color_preferences: List[str]) -> bool:
        """Check if item matches color preferences"""
        item_colors = item.get("ai_tags", {}).get("colors", [])
        return any(color in color_preferences for color in item_colors) or not color_preferences
    
    def _generate_outfit_name(self, items: List[Dict[str, Any]], occasion: str) -> str:
        """Generate outfit name"""
        occasion_names = {
            "work": "Professional",
            "casual": "Casual",
            "formal": "Formal",
            "party": "Party",
            "sport": "Sporty"
        }
        
        base_name = occasion_names.get(occasion, "Stylish")
        
        # Add descriptive words based on items
        if any(item["category"] == "dress" for item in items):
            return f"{base_name} Dress Look"
        elif any(item["category"] == "blazer" for item in items):
            return f"{base_name} Blazer Outfit"
        else:
            return f"{base_name} Ensemble"
    
    def _generate_outfit_description(self, items: List[Dict[str, Any]], occasion: str, season: str) -> str:
        """Generate outfit description"""
        descriptions = {
            "work": "Perfect for the office and business meetings",
            "casual": "Great for weekend outings and casual gatherings",
            "formal": "Elegant and sophisticated for special occasions",
            "party": "Fun and stylish for parties and social events",
            "sport": "Comfortable and practical for active pursuits"
        }
        
        base_description = descriptions.get(occasion, "A stylish and well-coordinated look")
        season_note = f" Perfect for {season} weather."
        
        return base_description + season_note
    
    async def generate_packing_list(
        self,
        destination: str,
        start_date: str,
        end_date: str,
        weather_forecast: Optional[Dict[str, Any]] = None,
        activities: List[str] = None,
        luggage_size: str = "medium"
    ) -> Dict[str, Any]:
        """Generate packing list for a trip"""
        try:
            # Calculate trip duration
            from datetime import datetime
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            duration = (end_dt - start_dt).days + 1
            
            # Generate packing suggestions based on duration and activities
            packing_items = []
            
            # Basic clothing items
            packing_items.extend(self._get_basic_clothing_items(duration, weather_forecast))
            
            # Activity-specific items
            if activities:
                packing_items.extend(self._get_activity_items(activities))
            
            # Destination-specific items
            packing_items.extend(self._get_destination_items(destination))
            
            # Create checklist
            checklist = self._create_packing_checklist(packing_items, luggage_size)
            
            return {
                "destination": destination,
                "duration_days": duration,
                "luggage_size": luggage_size,
                "packing_items": packing_items,
                "checklist": checklist,
                "tips": self._get_packing_tips(destination, duration, weather_forecast)
            }
            
        except Exception as e:
            logger.error(f"Packing list generation failed: {e}")
            return {
                "destination": destination,
                "duration_days": 0,
                "luggage_size": luggage_size,
                "packing_items": [],
                "checklist": [],
                "tips": []
            }
    
    def _get_basic_clothing_items(self, duration: int, weather_forecast: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get basic clothing items for the trip"""
        items = []
        
        # Calculate quantities based on duration
        tops_count = min(duration + 1, 7)
        bottoms_count = min(duration // 2 + 1, 4)
        underwear_count = duration + 2
        socks_count = duration + 1
        
        items.extend([
            {"item": "Tops/T-shirts", "quantity": tops_count, "category": "clothing"},
            {"item": "Bottoms (pants/skirts)", "quantity": bottoms_count, "category": "clothing"},
            {"item": "Underwear", "quantity": underwear_count, "category": "underwear"},
            {"item": "Socks", "quantity": socks_count, "category": "underwear"},
            {"item": "Pajamas", "quantity": 1, "category": "sleepwear"},
            {"item": "Comfortable shoes", "quantity": 1, "category": "shoes"},
            {"item": "Dress shoes", "quantity": 1, "category": "shoes"},
        ])
        
        # Add weather-specific items
        if weather_forecast:
            if weather_forecast.get("temperature", 20) < 15:
                items.append({"item": "Warm jacket", "quantity": 1, "category": "outerwear"})
            if "rain" in weather_forecast.get("condition", "").lower():
                items.append({"item": "Rain jacket/umbrella", "quantity": 1, "category": "accessories"})
        
        return items
    
    def _get_activity_items(self, activities: List[str]) -> List[Dict[str, Any]]:
        """Get items specific to planned activities"""
        items = []
        
        for activity in activities:
            if activity.lower() in ["swimming", "beach"]:
                items.append({"item": "Swimwear", "quantity": 1, "category": "swimwear"})
                items.append({"item": "Beach towel", "quantity": 1, "category": "accessories"})
            elif activity.lower() in ["hiking", "outdoor"]:
                items.append({"item": "Hiking boots", "quantity": 1, "category": "shoes"})
                items.append({"item": "Outdoor jacket", "quantity": 1, "category": "outerwear"})
            elif activity.lower() in ["dining", "restaurant"]:
                items.append({"item": "Dress shirt/blouse", "quantity": 1, "category": "clothing"})
                items.append({"item": "Dress pants/skirt", "quantity": 1, "category": "clothing"})
        
        return items
    
    def _get_destination_items(self, destination: str) -> List[Dict[str, Any]]:
        """Get items specific to destination"""
        items = []
        
        # Add destination-specific items based on location
        if any(city in destination.lower() for city in ["tropical", "beach", "island"]):
            items.append({"item": "Sunglasses", "quantity": 1, "category": "accessories"})
            items.append({"item": "Sunscreen", "quantity": 1, "category": "toiletries"})
        elif any(city in destination.lower() for city in ["mountain", "alpine", "ski"]):
            items.append({"item": "Warm layers", "quantity": 2, "category": "clothing"})
            items.append({"item": "Winter accessories", "quantity": 1, "category": "accessories"})
        
        return items
    
    def _create_packing_checklist(self, items: List[Dict[str, Any]], luggage_size: str) -> List[Dict[str, Any]]:
        """Create a packing checklist"""
        checklist = []
        
        for item in items:
            checklist.append({
                "item": item["item"],
                "quantity": item["quantity"],
                "packed": False,
                "category": item["category"]
            })
        
        # Add general packing items
        checklist.extend([
            {"item": "Toiletries", "quantity": 1, "packed": False, "category": "toiletries"},
            {"item": "Phone charger", "quantity": 1, "packed": False, "category": "electronics"},
            {"item": "Travel documents", "quantity": 1, "packed": False, "category": "documents"},
            {"item": "Medications", "quantity": 1, "packed": False, "category": "health"},
        ])
        
        return checklist
    
    def _get_packing_tips(self, destination: str, duration: int, weather_forecast: Optional[Dict[str, Any]]) -> List[str]:
        """Get packing tips for the trip"""
        tips = [
            "Roll your clothes to save space and prevent wrinkles",
            "Pack a small first aid kit with basic medications",
            "Bring a portable charger for your devices",
            "Pack a small laundry bag for dirty clothes"
        ]
        
        if duration > 7:
            tips.append("Consider doing laundry during your trip to pack lighter")
        
        if weather_forecast and weather_forecast.get("temperature", 20) < 10:
            tips.append("Layer your clothing for warmth and flexibility")
        
        return tips
