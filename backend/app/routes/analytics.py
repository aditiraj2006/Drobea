from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from datetime import datetime, timedelta
from bson import ObjectId

from app.models.user import User
from app.models.analytics import AnalyticsDashboard, AnalyticsRequest
from app.services.database.mongodb import get_database
from app.utils.auth import get_current_user

router = APIRouter()

@router.get("/dashboard")
async def get_analytics_dashboard(
    period: str = Query("monthly", regex="^(daily|weekly|monthly|yearly)$"),
    current_user: User = Depends(get_current_user)
):
    """
    Get analytics dashboard data
    """
    try:
        db = get_database()
        
        # Get or create analytics dashboard
        dashboard = await db.analytics_dashboard.find_one({
            "user_id": current_user.id,
            "period": period
        })
        
        if not dashboard:
            # Generate new dashboard
            dashboard = await generate_analytics_dashboard(current_user.id, period, db)
        
        return {"dashboard": dashboard}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analytics dashboard: {str(e)}"
        )

@router.get("/sustainability")
async def get_sustainability_metrics(
    current_user: User = Depends(get_current_user)
):
    """
    Get sustainability metrics
    """
    try:
        db = get_database()
        
        # Get wardrobe items
        wardrobe_items = await db.wardrobe_items.find({
            "user_id": current_user.id,
            "is_active": True
        }).to_list(length=None)
        
        # Calculate sustainability metrics
        total_items = len(wardrobe_items)
        total_wears = sum(item.get("usage_stats", {}).get("wear_count", 0) for item in wardrobe_items)
        avg_wears_per_item = total_wears / total_items if total_items > 0 else 0
        
        # Calculate carbon footprint (simplified calculation)
        carbon_footprint = total_items * 20.5  # kg CO2 per item (average)
        
        # Calculate water usage
        water_usage = total_items * 2000  # liters per item (average)
        
        # Calculate waste generated
        waste_generated = total_items * 0.5  # kg per item
        
        # Calculate circularity score
        circularity_score = min(avg_wears_per_item / 10, 1.0)  # Normalized score
        
        # Get donation recommendations
        donation_candidates = [item for item in wardrobe_items 
                             if item.get("organization", {}).get("donation_candidate", False)]
        
        sustainability_metrics = {
            "carbon_footprint": carbon_footprint,
            "water_usage": water_usage,
            "waste_generated": waste_generated,
            "circularity_score": circularity_score,
            "donation_recommendations": len(donation_candidates),
            "total_items": total_items,
            "total_wears": total_wears,
            "avg_wears_per_item": avg_wears_per_item
        }
        
        return {"sustainability": sustainability_metrics}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get sustainability metrics: {str(e)}"
        )

@router.get("/usage-trends")
async def get_usage_trends(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user)
):
    """
    Get usage trends over time
    """
    try:
        db = get_database()
        
        # Set default date range if not provided
        if not start_date:
            start_date = (datetime.utcnow() - timedelta(days=30)).isoformat()
        if not end_date:
            end_date = datetime.utcnow().isoformat()
        
        # Parse dates
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        # Get usage data
        usage_data = await db.wardrobe_items.aggregate([
            {"$match": {"user_id": current_user.id, "is_active": True}},
            {"$project": {
                "last_worn": "$usage_stats.last_worn",
                "wear_count": "$usage_stats.wear_count",
                "created_at": 1
            }},
            {"$match": {
                "last_worn": {"$gte": start_dt, "$lte": end_dt}
            }},
            {"$group": {
                "_id": {
                    "year": {"$year": "$last_worn"},
                    "month": {"$month": "$last_worn"},
                    "day": {"$dayOfMonth": "$last_worn"}
                },
                "total_wears": {"$sum": "$wear_count"}
            }},
            {"$sort": {"_id": 1}}
        ]).to_list(length=None)
        
        return {"usage_trends": usage_data}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get usage trends: {str(e)}"
        )

@router.get("/cost-per-wear")
async def get_cost_per_wear_analysis(
    current_user: User = Depends(get_current_user)
):
    """
    Get cost per wear analysis
    """
    try:
        db = get_database()
        
        # Get wardrobe items with cost and wear data
        items = await db.wardrobe_items.find({
            "user_id": current_user.id,
            "is_active": True,
            "metadata.price": {"$exists": True, "$gt": 0}
        }).to_list(length=None)
        
        cost_analysis = []
        total_investment = 0
        total_wears = 0
        
        for item in items:
            price = item.get("metadata", {}).get("price", 0)
            wear_count = item.get("usage_stats", {}).get("wear_count", 0)
            cost_per_wear = price / wear_count if wear_count > 0 else price
            
            cost_analysis.append({
                "item_id": str(item["_id"]),
                "name": item.get("ai_tags", {}).get("subcategory", "Unknown"),
                "price": price,
                "wear_count": wear_count,
                "cost_per_wear": cost_per_wear
            })
            
            total_investment += price
            total_wears += wear_count
        
        # Sort by cost per wear
        cost_analysis.sort(key=lambda x: x["cost_per_wear"])
        
        avg_cost_per_wear = total_investment / total_wears if total_wears > 0 else 0
        
        return {
            "cost_analysis": cost_analysis,
            "total_investment": total_investment,
            "total_wears": total_wears,
            "avg_cost_per_wear": avg_cost_per_wear
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get cost per wear analysis: {str(e)}"
        )

@router.get("/insights")
async def get_analytics_insights(
    current_user: User = Depends(get_current_user)
):
    """
    Get personalized analytics insights
    """
    try:
        db = get_database()
        
        insights = []
        
        # Get wardrobe data
        wardrobe_items = await db.wardrobe_items.find({
            "user_id": current_user.id,
            "is_active": True
        }).to_list(length=None)
        
        # Insight 1: Most worn item
        most_worn_item = max(wardrobe_items, key=lambda x: x.get("usage_stats", {}).get("wear_count", 0))
        if most_worn_item.get("usage_stats", {}).get("wear_count", 0) > 0:
            insights.append({
                "type": "achievement",
                "title": "Most Worn Item",
                "message": f"Your {most_worn_item.get('ai_tags', {}).get('subcategory', 'item')} has been worn {most_worn_item.get('usage_stats', {}).get('wear_count', 0)} times!",
                "category": "usage"
            })
        
        # Insight 2: Unused items
        unused_items = [item for item in wardrobe_items 
                       if item.get("usage_stats", {}).get("wear_count", 0) == 0]
        if unused_items:
            insights.append({
                "type": "recommendation",
                "title": "Unused Items",
                "message": f"You have {len(unused_items)} items that haven't been worn yet. Consider styling them or donating them.",
                "category": "sustainability",
                "action_required": True,
                "action_text": "View unused items"
            })
        
        # Insight 3: Color analysis
        color_counts = {}
        for item in wardrobe_items:
            colors = item.get("ai_tags", {}).get("colors", [])
            for color in colors:
                color_counts[color] = color_counts.get(color, 0) + 1
        
        if color_counts:
            most_used_color = max(color_counts, key=color_counts.get)
            insights.append({
                "type": "insight",
                "title": "Color Preference",
                "message": f"Your most used color is {most_used_color}. Consider adding more variety to your wardrobe.",
                "category": "style"
            })
        
        return {"insights": insights}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analytics insights: {str(e)}"
        )

async def generate_analytics_dashboard(user_id: ObjectId, period: str, db):
    """
    Generate analytics dashboard for user
    """
    try:
        # Get wardrobe items
        wardrobe_items = await db.wardrobe_items.find({
            "user_id": user_id,
            "is_active": True
        }).to_list(length=None)
        
        # Calculate basic metrics
        total_items = len(wardrobe_items)
        total_wears = sum(item.get("usage_stats", {}).get("wear_count", 0) for item in wardrobe_items)
        avg_wears_per_item = total_wears / total_items if total_items > 0 else 0
        
        # Get most/least worn items
        most_worn_item = max(wardrobe_items, key=lambda x: x.get("usage_stats", {}).get("wear_count", 0)) if wardrobe_items else None
        least_worn_item = min(wardrobe_items, key=lambda x: x.get("usage_stats", {}).get("wear_count", 0)) if wardrobe_items else None
        
        # Create dashboard
        dashboard = AnalyticsDashboard(
            user_id=user_id,
            period=period,
            wear_analytics={
                "total_items": total_items,
                "items_worn": len([item for item in wardrobe_items if item.get("usage_stats", {}).get("wear_count", 0) > 0]),
                "total_wears": total_wears,
                "average_wears_per_item": avg_wears_per_item,
                "most_worn_item": str(most_worn_item["_id"]) if most_worn_item else None,
                "least_worn_item": str(least_worn_item["_id"]) if least_worn_item else None,
                "unused_items": len([item for item in wardrobe_items if item.get("usage_stats", {}).get("wear_count", 0) == 0])
            }
        )
        
        # Save dashboard
        result = await db.analytics_dashboard.insert_one(dashboard.dict(by_alias=True))
        dashboard.id = result.inserted_id
        
        return dashboard.dict(by_alias=True)
        
    except Exception as e:
        raise Exception(f"Failed to generate analytics dashboard: {str(e)}")
