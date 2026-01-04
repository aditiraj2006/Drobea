from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from bson import ObjectId

from app.models.user import User
from app.services.ai.color_analysis import ColorAnalysisService
from app.services.ai.style_recommendations import StyleRecommendationService
from app.services.ai.auto_tagging import AutoTaggingService
from app.services.external.gemini_api import GeminiClient
from app.utils.auth import get_current_user

router = APIRouter()

# Initialize services
color_analysis = ColorAnalysisService()
style_recommendations = StyleRecommendationService()
auto_tagging = AutoTaggingService()
gemini_client = GeminiClient()

@router.post("/color-analysis")
async def analyze_personal_colors(
    user_photos: List[str],
    current_user: User = Depends(get_current_user)
):
    """
    Analyze user's personal color palette
    """
    try:
        # Analyze personal colors
        color_analysis_result = await color_analysis.analyze_personal_colors(user_photos)
        
        # Get style preferences from Gemini
        style_preferences = await gemini_client.analyze_style_preferences(user_photos)
        
        return {
            "personal_colors": color_analysis_result,
            "style_preferences": style_preferences
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Color analysis failed: {str(e)}"
        )

@router.post("/style-recommendations")
async def get_style_recommendations(
    user_preferences: dict,
    current_user: User = Depends(get_current_user)
):
    """
    Get personalized style recommendations
    """
    try:
        # Get style recommendations
        recommendations = await style_recommendations.get_personalized_recommendations(
            user_id=str(current_user.id),
            preferences=user_preferences
        )
        
        return {"recommendations": recommendations}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Style recommendations failed: {str(e)}"
        )

@router.post("/auto-tag")
async def auto_tag_item(
    image_path: str,
    current_user: User = Depends(get_current_user)
):
    """
    Auto-tag a clothing item using AI
    """
    try:
        # Auto-tag the item
        tags = await auto_tagging.analyze_item(image_path)
        
        return {"tags": tags}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Auto-tagging failed: {str(e)}"
        )

@router.get("/trends")
async def get_fashion_trends(
    season: str = "current",
    current_user: User = Depends(get_current_user)
):
    """
    Get current fashion trends
    """
    try:
        # Get trends from Gemini
        trends = await gemini_client.generate_fashion_trends(season)
        
        return {"trends": trends}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get trends: {str(e)}"
        )

@router.post("/outfit-suggestions")
async def get_outfit_suggestions(
    occasion: str,
    weather: Optional[dict] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get AI-powered outfit suggestions
    """
    try:
        # Get user's wardrobe items
        from app.services.database.mongodb import get_database
        db = get_database()
        
        wardrobe_items = await db.wardrobe_items.find({
            "user_id": current_user.id,
            "is_active": True
        }).to_list(length=None)
        
        # Convert to format expected by Gemini
        items_for_gemini = []
        for item in wardrobe_items:
            items_for_gemini.append({
                "category": item.get("ai_tags", {}).get("category", ""),
                "subcategory": item.get("ai_tags", {}).get("subcategory", ""),
                "color": item.get("ai_tags", {}).get("colors", [""])[0],
                "style": item.get("ai_tags", {}).get("style", ""),
                "pattern": item.get("ai_tags", {}).get("pattern", "")
            })
        
        # Get outfit suggestions from Gemini
        suggestions = await gemini_client.generate_outfit_suggestions(
            wardrobe_items=items_for_gemini,
            occasion=occasion,
            weather=weather
        )
        
        return {"suggestions": suggestions}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Outfit suggestions failed: {str(e)}"
        )

@router.post("/color-harmony")
async def analyze_color_harmony(
    colors: List[str],
    current_user: User = Depends(get_current_user)
):
    """
    Analyze color harmony and suggest complementary colors
    """
    try:
        # Analyze color harmony with Gemini
        harmony_analysis = await gemini_client.analyze_color_harmony(colors)
        
        return {"harmony_analysis": harmony_analysis}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Color harmony analysis failed: {str(e)}"
        )
