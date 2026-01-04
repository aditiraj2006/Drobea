import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database = None

db = Database()

async def connect_to_mongo():
    """Create database connection"""
    try:
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("DATABASE_NAME", "drobea")
        
        db.client = AsyncIOMotorClient(mongodb_url)
        db.database = db.client[database_name]
        
        # Test the connection
        await db.client.admin.command('ping')
        logger.info(f"Connected to MongoDB database: {database_name}")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        logger.info("Disconnected from MongoDB")

async def create_indexes():
    """Create database indexes for better performance"""
    try:
        # User collection indexes
        await db.database.users.create_index("email", unique=True)
        await db.database.users.create_index("username", unique=True)
        await db.database.users.create_index("created_at")
        
        # Wardrobe items indexes
        await db.database.wardrobe_items.create_index("user_id")
        await db.database.wardrobe_items.create_index("ai_tags.category")
        await db.database.wardrobe_items.create_index("ai_tags.colors")
        await db.database.wardrobe_items.create_index("ai_tags.style")
        await db.database.wardrobe_items.create_index("created_at")
        await db.database.wardrobe_items.create_index([("user_id", 1), ("ai_tags.category", 1)])
        
        # Outfits indexes
        await db.database.outfits.create_index("user_id")
        await db.database.outfits.create_index("occasion")
        await db.database.outfits.create_index("season")
        await db.database.outfits.create_index("is_public")
        await db.database.outfits.create_index("created_at")
        
        # Virtual try-on indexes
        await db.database.virtual_tryon_profiles.create_index("user_id", unique=True)
        await db.database.generation_results.create_index("user_id")
        await db.database.generation_results.create_index("created_at")
        
        # Social indexes
        await db.database.posts.create_index("user_id")
        await db.database.posts.create_index("is_public")
        await db.database.posts.create_index("created_at")
        await db.database.posts.create_index("hashtags")
        await db.database.posts.create_index([("is_public", 1), ("created_at", -1)])
        
        # Shopping indexes
        await db.database.products.create_index("user_id")
        await db.database.products.create_index("platform")
        await db.database.products.create_index("category")
        await db.database.wishlist_items.create_index("user_id")
        await db.database.wishlist_items.create_index("product_id")
        
        # Analytics indexes
        await db.database.analytics_dashboard.create_index("user_id")
        await db.database.analytics_dashboard.create_index("period")
        await db.database.analytics_dashboard.create_index("generated_at")
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.error(f"Error creating database indexes: {e}")

def get_database():
    """Get database instance"""
    return db.database

def get_collection(collection_name: str):
    """Get specific collection"""
    return db.database[collection_name]
