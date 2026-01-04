from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from app.models.user import User
from app.models.shopping import (
    Product, WishlistItem, WishlistCreate, ShoppingList, ShoppingListCreate,
    Purchase, ShoppingRecommendation
)
from app.services.database.mongodb import get_database
from app.utils.auth import get_current_user

router = APIRouter()

@router.get("/products")
async def get_products(
    category: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get products with optional filtering
    """
    try:
        db = get_database()
        
        # Build filter query
        filter_query = {"user_id": current_user.id, "is_active": True}
        
        if category:
            filter_query["category"] = category
        if brand:
            filter_query["brand"] = brand
        if min_price is not None:
            filter_query["price"] = {"$gte": min_price}
        if max_price is not None:
            if "price" in filter_query:
                filter_query["price"]["$lte"] = max_price
            else:
                filter_query["price"] = {"$lte": max_price}
        
        # Get products with pagination
        skip = (page - 1) * limit
        products = await db.products.find(filter_query).skip(skip).limit(limit).to_list(length=limit)
        
        return {"products": products}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get products: {str(e)}"
        )

@router.post("/products")
async def create_product(
    product_data: Product,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new product
    """
    try:
        db = get_database()
        
        # Set user ID
        product_data.user_id = current_user.id
        
        # Save to database
        result = await db.products.insert_one(product_data.dict(by_alias=True))
        product_data.id = result.inserted_id
        
        return {"message": "Product created successfully", "product_id": str(result.inserted_id)}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create product: {str(e)}"
        )

@router.get("/wishlist")
async def get_wishlist(
    current_user: User = Depends(get_current_user)
):
    """
    Get user's wishlist
    """
    try:
        db = get_database()
        
        # Get wishlist items with product details
        pipeline = [
            {"$match": {"user_id": current_user.id}},
            {"$lookup": {
                "from": "products",
                "localField": "product_id",
                "foreignField": "_id",
                "as": "product"
            }},
            {"$unwind": "$product"},
            {"$sort": {"created_at": -1}}
        ]
        
        wishlist_items = await db.wishlist_items.aggregate(pipeline).to_list(length=None)
        
        return {"wishlist": wishlist_items}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get wishlist: {str(e)}"
        )

@router.post("/wishlist")
async def add_to_wishlist(
    wishlist_data: WishlistCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Add item to wishlist
    """
    try:
        db = get_database()
        
        # Check if product exists
        product = await db.products.find_one({"_id": wishlist_data.product_id})
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        # Check if already in wishlist
        existing_item = await db.wishlist_items.find_one({
            "user_id": current_user.id,
            "product_id": wishlist_data.product_id
        })
        
        if existing_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product already in wishlist"
            )
        
        # Create wishlist item
        wishlist_item = WishlistItem(
            user_id=current_user.id,
            product_id=wishlist_data.product_id,
            notes=wishlist_data.notes,
            priority=wishlist_data.priority,
            target_price=wishlist_data.target_price,
            size_preference=wishlist_data.size_preference,
            color_preference=wishlist_data.color_preference
        )
        
        # Save to database
        result = await db.wishlist_items.insert_one(wishlist_item.dict(by_alias=True))
        
        return {"message": "Item added to wishlist successfully", "item_id": str(result.inserted_id)}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add to wishlist: {str(e)}"
        )

@router.delete("/wishlist/{item_id}")
async def remove_from_wishlist(
    item_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Remove item from wishlist
    """
    try:
        db = get_database()
        
        result = await db.wishlist_items.delete_one({
            "_id": ObjectId(item_id),
            "user_id": current_user.id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wishlist item not found"
            )
        
        return {"message": "Item removed from wishlist successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove from wishlist: {str(e)}"
        )

@router.get("/shopping-lists")
async def get_shopping_lists(
    current_user: User = Depends(get_current_user)
):
    """
    Get user's shopping lists
    """
    try:
        db = get_database()
        
        shopping_lists = await db.shopping_lists.find({
            "user_id": current_user.id
        }).sort("created_at", -1).to_list(length=None)
        
        return {"shopping_lists": shopping_lists}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get shopping lists: {str(e)}"
        )

@router.post("/shopping-lists")
async def create_shopping_list(
    list_data: ShoppingListCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new shopping list
    """
    try:
        db = get_database()
        
        # Create shopping list
        shopping_list = ShoppingList(
            user_id=current_user.id,
            name=list_data.name,
            description=list_data.description,
            items=list_data.items or [],
            is_shared=list_data.is_shared,
            shared_with=list_data.shared_with or []
        )
        
        # Save to database
        result = await db.shopping_lists.insert_one(shopping_list.dict(by_alias=True))
        
        return {"message": "Shopping list created successfully", "list_id": str(result.inserted_id)}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create shopping list: {str(e)}"
        )

@router.get("/purchases")
async def get_purchases(
    current_user: User = Depends(get_current_user)
):
    """
    Get user's purchase history
    """
    try:
        db = get_database()
        
        purchases = await db.purchases.find({
            "user_id": current_user.id
        }).sort("purchase_date", -1).to_list(length=None)
        
        return {"purchases": purchases}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get purchases: {str(e)}"
        )

@router.post("/purchases")
async def record_purchase(
    purchase_data: Purchase,
    current_user: User = Depends(get_current_user)
):
    """
    Record a new purchase
    """
    try:
        db = get_database()
        
        # Set user ID
        purchase_data.user_id = current_user.id
        
        # Save to database
        result = await db.purchases.insert_one(purchase_data.dict(by_alias=True))
        
        return {"message": "Purchase recorded successfully", "purchase_id": str(result.inserted_id)}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record purchase: {str(e)}"
        )

@router.get("/recommendations")
async def get_shopping_recommendations(
    current_user: User = Depends(get_current_user)
):
    """
    Get personalized shopping recommendations
    """
    try:
        db = get_database()
        
        # Get user's style preferences
        user = await db.users.find_one({"_id": current_user.id})
        style_preferences = user.get("profile", {}).get("style_preferences", [])
        
        # Get recommendations based on style preferences
        recommendations = await db.shopping_recommendations.find({
            "user_id": current_user.id,
            "is_dismissed": False
        }).sort("created_at", -1).to_list(length=None)
        
        return {"recommendations": recommendations}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recommendations: {str(e)}"
        )

@router.post("/import-product")
async def import_product(
    url: str,
    platform: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Import product from external URL
    """
    try:
        # This would integrate with external APIs to scrape product data
        # For now, return a placeholder response
        
        return {
            "message": "Product import feature coming soon",
            "url": url,
            "platform": platform
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to import product: {str(e)}"
        )
