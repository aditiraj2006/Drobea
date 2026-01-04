import os
import firebase_admin
from firebase_admin import credentials, auth
from typing import Optional, Dict, Any
from fastapi import HTTPException, status

class FirebaseAuth:
    """Firebase Authentication Service"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseAuth, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialize_firebase()
            self._initialized = True
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
            
            if credentials_path and os.path.exists(credentials_path):
                # Initialize with service account credentials
                cred = credentials.Certificate(credentials_path)
                firebase_admin.initialize_app(cred)
                print("✓ Firebase initialized with service account")
            else:
                # Initialize with default credentials (for development)
                project_id = os.getenv("FIREBASE_PROJECT_ID")
                if project_id:
                    firebase_admin.initialize_app(options={
                        'projectId': project_id,
                    })
                    print(f"✓ Firebase initialized with project ID: {project_id}")
                else:
                    print("⚠ Warning: Firebase not initialized. Google OAuth will not work.")
                    print("  Please set FIREBASE_CREDENTIALS_PATH or FIREBASE_PROJECT_ID in .env")
        except ValueError as e:
            # Firebase already initialized
            print("✓ Firebase already initialized")
        except Exception as e:
            print(f"✗ Firebase initialization failed: {str(e)}")
            raise
    
    async def verify_google_token(self, id_token: str) -> Dict[str, Any]:
        """
        Verify Google OAuth ID token from Firebase
        
        Args:
            id_token: Firebase ID token from client
            
        Returns:
            Dict containing user information
        """
        try:
            # Verify the ID token
            decoded_token = auth.verify_id_token(id_token)
            
            # Extract user information
            user_info = {
                "uid": decoded_token.get("uid"),
                "email": decoded_token.get("email"),
                "email_verified": decoded_token.get("email_verified", False),
                "name": decoded_token.get("name"),
                "picture": decoded_token.get("picture"),
                "firebase_uid": decoded_token.get("uid")
            }
            
            return user_info
            
        except auth.InvalidIdTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )
        except auth.ExpiredIdTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication token has expired"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token verification failed: {str(e)}"
            )
    
    async def get_user_by_uid(self, uid: str) -> Optional[Dict[str, Any]]:
        """
        Get Firebase user by UID
        
        Args:
            uid: Firebase user UID
            
        Returns:
            User information or None
        """
        try:
            user = auth.get_user(uid)
            return {
                "uid": user.uid,
                "email": user.email,
                "email_verified": user.email_verified,
                "display_name": user.display_name,
                "photo_url": user.photo_url,
                "disabled": user.disabled,
            }
        except auth.UserNotFoundError:
            return None
        except Exception as e:
            print(f"Error getting Firebase user: {str(e)}")
            return None
    
    async def create_custom_token(self, uid: str) -> str:
        """
        Create a custom Firebase token for a user
        
        Args:
            uid: User UID
            
        Returns:
            Custom token string
        """
        try:
            return auth.create_custom_token(uid)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create custom token: {str(e)}"
            )

# Singleton instance
firebase_auth = FirebaseAuth()
