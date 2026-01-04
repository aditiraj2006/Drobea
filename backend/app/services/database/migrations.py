import asyncio
from datetime import datetime
from app.services.database.mongodb import get_database

async def run_migrations():
    """Run database migrations"""
    db = get_database()
    
    # Migration 1: Add default collections if they don't exist
    collections = await db.list_collection_names()
    
    required_collections = [
        "users", "wardrobe_items", "outfits", "virtual_tryon_profiles",
        "generation_results", "posts", "comments", "products", "wishlist_items",
        "shopping_lists", "purchases", "analytics_dashboard", "notifications",
        "challenges", "challenge_submissions"
    ]
    
    for collection_name in required_collections:
        if collection_name not in collections:
            await db.create_collection(collection_name)
            print(f"Created collection: {collection_name}")
    
    # Migration 2: Add sample data for development
    if await db.users.count_documents({}) == 0:
        await create_sample_data(db)
    
    print("Database migrations completed successfully")

async def create_sample_data(db):
    """Create sample data for development"""
    from app.models.user import User, UserProfile
    from app.models.wardrobe import WardrobeItem, AITags, ImageData, ItemMetadata
    from app.models.outfit import Outfit, OutfitItem
    from app.models.social import Post
    from app.models.shopping import Product, WishlistItem
    from app.models.analytics import AnalyticsDashboard
    
    # Sample user
    sample_user = User(
        email="demo@Drobea.com",
        username="demo_user",
        password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/4.8.2",  # password: demo123
        profile=UserProfile(
            bio="Fashion enthusiast and AI clothing explorer",
            style_preferences=["casual", "modern", "minimalist"],
            color_season="autumn"
        )
    )
    
    user_result = await db.users.insert_one(sample_user.dict(by_alias=True))
    user_id = user_result.inserted_id
    
    # Sample wardrobe items
    sample_items = [
        WardrobeItem(
            user_id=user_id,
            images=[ImageData(
                original="https://example.com/tshirt1.jpg",
                processed="https://example.com/tshirt1_processed.jpg",
                thumbnail="https://example.com/tshirt1_thumb.jpg",
                width=800, height=600, file_size=1024000
            )],
            ai_tags=AITags(
                category="top",
                subcategory="t-shirt",
                colors=["white", "navy"],
                style="casual",
                pattern="striped",
                season=["spring", "summer"],
                occasion=["casual", "work"],
                confidence_score=0.95
            ),
            metadata=ItemMetadata(
                brand="Uniqlo",
                size="M",
                price=29.99,
                material="cotton"
            )
        ),
        WardrobeItem(
            user_id=user_id,
            images=[ImageData(
                original="https://example.com/jeans1.jpg",
                processed="https://example.com/jeans1_processed.jpg",
                thumbnail="https://example.com/jeans1_thumb.jpg",
                width=800, height=600, file_size=1200000
            )],
            ai_tags=AITags(
                category="bottom",
                subcategory="jeans",
                colors=["blue"],
                style="casual",
                pattern="solid",
                season=["spring", "fall", "winter"],
                occasion=["casual", "work"],
                confidence_score=0.92
            ),
            metadata=ItemMetadata(
                brand="Levi's",
                size="32",
                price=89.99,
                material="denim"
            )
        )
    ]
    
    item_results = await db.wardrobe_items.insert_many([item.dict(by_alias=True) for item in sample_items])
    item_ids = item_results.inserted_ids
    
    # Sample outfit
    sample_outfit = Outfit(
        user_id=user_id,
        name="Casual Friday",
        description="Perfect for a casual Friday at work",
        items=[
            OutfitItem(item_id=item_ids[0], category="top", layer=0),
            OutfitItem(item_id=item_ids[1], category="bottom", layer=1)
        ],
        occasion="work",
        season="spring",
        weather_conditions=["mild", "sunny"]
    )
    
    outfit_result = await db.outfits.insert_one(sample_outfit.dict(by_alias=True))
    
    # Sample post
    sample_post = Post(
        user_id=user_id,
        outfit_id=outfit_result.inserted_id,
        content="Loving this casual Friday look! #casualfriday #workwear",
        hashtags=["casualfriday", "workwear"],
        is_public=True
    )
    
    await db.posts.insert_one(sample_post.dict(by_alias=True))
    
    # Sample product
    sample_product = Product(
        user_id=user_id,
        name="Classic White Sneakers",
        brand="Adidas",
        price=79.99,
        category="shoes",
        subcategory="sneakers",
        colors=["white"],
        url="https://example.com/sneakers",
        platform="adidas"
    )
    
    product_result = await db.products.insert_one(sample_product.dict(by_alias=True))
    
    # Sample wishlist item
    sample_wishlist = WishlistItem(
        user_id=user_id,
        product_id=product_result.inserted_id,
        notes="Need these for summer outfits",
        priority=3
    )
    
    await db.wishlist_items.insert_one(sample_wishlist.dict(by_alias=True))
    
    # Sample analytics dashboard
    sample_analytics = AnalyticsDashboard(
        user_id=user_id,
        period="monthly"
    )
    
    await db.analytics_dashboard.insert_one(sample_analytics.dict(by_alias=True))
    
    print("Sample data created successfully")

if __name__ == "__main__":
    asyncio.run(run_migrations())
