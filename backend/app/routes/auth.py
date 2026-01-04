from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional
import os
from jose import JWTError, jwt
from passlib.context import CryptContext
from bson import ObjectId

from app.models.user import User, UserCreate, UserResponse, Token, LoginRequest, GoogleAuthRequest
from app.services.database.mongodb import get_database
from app.services.external.firebase_auth import firebase_auth
from app.utils.auth import get_current_user, create_access_token, verify_password, get_password_hash
from app.utils.validators import validate_email, validate_password

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """
    Register a new user
    """
    try:
        db = get_database()
        
        # Validate email format
        if not validate_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        
        # Validate password strength
        if not validate_password(user_data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters with uppercase, lowercase, number and special character"
            )
        
        # Check if user already exists
        existing_user = await db.users.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username already exists
        existing_username = await db.users.find_one({"username": user_data.username})
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user
        user_dict = user_data.dict()
        user_dict["password_hash"] = hashed_password
        del user_dict["password"]
        
        user = User(**user_dict)
        user_dict = user.dict(by_alias=True)
        
        # Insert user
        result = await db.users.insert_one(user_dict)
        user_dict["_id"] = result.inserted_id
        
        # Return user without password
        user_response = UserResponse(**user_dict)
        return user_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """
    Login user and return access token
    """
    try:
        db = get_database()
        
        # Find user by email
        user = await db.users.find_one({"email": login_data.email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(login_data.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is active
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )
        
        # Update last login
        await db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        # Create access token
        access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
        access_token = create_access_token(
            data={"sub": str(user["_id"])},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": int(access_token_expires.total_seconds())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.post("/google", response_model=Token)
async def google_auth(auth_data: GoogleAuthRequest):
    """
    Authenticate with Google OAuth (Firebase)
    """
    try:
        # Verify Firebase ID token
        user_info = await firebase_auth.verify_google_token(auth_data.id_token)
        
        db = get_database()
        
        # Check if user exists by email or firebase_uid
        user = await db.users.find_one({
            "$or": [
                {"email": user_info["email"]},
                {"firebase_uid": user_info["uid"]}
            ]
        })
        
        if user:
            # Update existing user
            await db.users.update_one(
                {"_id": user["_id"]},
                {
                    "$set": {
                        "firebase_uid": user_info["uid"],
                        "auth_provider": "google",
                        "is_verified": user_info.get("email_verified", False),
                        "last_login": datetime.utcnow(),
                        "updated_at": datetime.utcnow(),
                        "profile.avatar": user_info.get("picture", user.get("profile", {}).get("avatar"))
                    }
                }
            )
            user_id = str(user["_id"])
        else:
            # Create new user from Google account
            username = user_info["email"].split("@")[0]
            
            # Check if username exists, append number if needed
            base_username = username
            counter = 1
            while await db.users.find_one({"username": username}):
                username = f"{base_username}{counter}"
                counter += 1
            
            new_user = User(
                email=user_info["email"],
                username=username,
                password_hash=None,  # No password for OAuth users
                auth_provider="google",
                firebase_uid=user_info["uid"],
                is_verified=user_info.get("email_verified", False),
                profile={
                    "avatar": user_info.get("picture"),
                    "bio": "",
                    "style_preferences": [],
                    "body_measurements": {},
                    "color_season": None,
                    "location": None,
                    "timezone": None
                }
            )
            
            user_dict = new_user.dict(by_alias=True)
            result = await db.users.insert_one(user_dict)
            user_id = str(result.inserted_id)
        
        # Create access token
        access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
        access_token = create_access_token(
            data={"sub": user_id},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": int(access_token_expires.total_seconds())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Google authentication failed: {str(e)}"
        )

@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user)):
    """
    Refresh access token
    """
    try:
        # Create new access token
        access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
        access_token = create_access_token(
            data={"sub": str(current_user.id)},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": int(access_token_expires.total_seconds())
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout user (client should discard token)
    """
    return {"message": "Successfully logged out"}

@router.post("/forgot-password")
async def forgot_password(email: str):
    """
    Send password reset email
    """
    try:
        db = get_database()
        
        # Check if user exists
        user = await db.users.find_one({"email": email})
        if not user:
            # Don't reveal if email exists or not
            return {"message": "If the email exists, a password reset link has been sent"}
        
        # Generate reset token
        reset_token = create_access_token(
            data={"sub": str(user["_id"]), "type": "password_reset"},
            expires_delta=timedelta(hours=1)
        )
        
        # TODO: Send email with reset token
        # For now, just return success
        return {"message": "If the email exists, a password reset link has been sent"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password reset request failed: {str(e)}"
        )

@router.post("/reset-password")
async def reset_password(token: str, new_password: str):
    """
    Reset password with token
    """
    try:
        # Verify token
        try:
            payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM", "HS256")])
            user_id = payload.get("sub")
            token_type = payload.get("type")
            
            if not user_id or token_type != "password_reset":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid reset token"
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset token"
            )
        
        # Validate new password
        if not validate_password(new_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters with uppercase, lowercase, number and special character"
            )
        
        # Update password
        db = get_database()
        hashed_password = get_password_hash(new_password)
        
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password_hash": hashed_password, "updated_at": datetime.utcnow()}}
        )
        
        return {"message": "Password reset successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password reset failed: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    return UserResponse(**current_user.dict(by_alias=True))

@router.post("/verify-email")
async def verify_email(token: str):
    """
    Verify email address
    """
    try:
        # Verify token
        try:
            payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM", "HS256")])
            user_id = payload.get("sub")
            token_type = payload.get("type")
            
            if not user_id or token_type != "email_verification":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid verification token"
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification token"
            )
        
        # Update user verification status
        db = get_database()
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_verified": True, "updated_at": datetime.utcnow()}}
        )
        
        return {"message": "Email verified successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Email verification failed: {str(e)}"
        )
