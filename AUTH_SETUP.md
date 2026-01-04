# Drobea Authentication Setup Guide

## Overview
Drobea supports two authentication methods:
1. **Email/Password** - Traditional email-based authentication
2. **Google OAuth** - Sign in with Google using Firebase

## Backend Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Update `backend/.env`:
```env
# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=drobea

# JWT
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Firebase (for Google OAuth)
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
FIREBASE_PROJECT_ID=your-firebase-project-id

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 3. Setup Firebase (for Google OAuth)

#### A. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" or select existing
3. Follow setup wizard

#### B. Enable Authentication
1. Navigate to: **Authentication** > **Sign-in method**
2. Enable **Email/Password** provider
3. Enable **Google** provider
4. Save changes

#### C. Get Service Account Credentials
1. Go to: **Project Settings** (⚙️) > **Service Accounts**
2. Click **"Generate new private key"**
3. Save JSON file as `backend/firebase-credentials.json`
4. ⚠️ **Never commit this file to version control!**

### 4. Start Backend Server
```bash
cd backend
python -m uvicorn app.main:app --reload
```

Server runs on: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## Frontend Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

This installs Firebase SDK and all dependencies.

### 2. Get Firebase Web Config
1. In Firebase Console: **Project Settings** > **General**
2. Scroll to **"Your apps"**
3. Click **Add app** > **Web** (</>)
4. Register app (name: "Drobea Web")
5. Copy the config object

### 3. Configure Environment
Create/update `frontend/.env.local`:
```env
# API Configuration
VITE_API_URL=http://localhost:8000

# Firebase Configuration
VITE_FIREBASE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789012
VITE_FIREBASE_APP_ID=1:123456789012:web:xxxxxxxxxxxxx
```

### 4. Start Frontend Server
```bash
cd frontend
npm run dev
```

Frontend runs on: `http://localhost:3001` or `http://localhost:3000`

## Testing Authentication

### Email/Password Registration
```bash
# POST http://localhost:8000/auth/register
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "Test@12345"
  }'
```

### Email/Password Login
```bash
# POST http://localhost:8000/auth/login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Test@12345"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Google OAuth Login
1. Click "Continue with Google" on login page
2. Select Google account
3. Frontend sends Firebase ID token to backend
4. Backend verifies and returns JWT token

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/register` | POST | Register with email/password |
| `/auth/login` | POST | Login with email/password |
| `/auth/google` | POST | Login/register with Google |
| `/auth/logout` | POST | Logout (client discards token) |
| `/auth/refresh` | POST | Refresh access token |
| `/auth/me` | GET | Get current user info |
| `/auth/forgot-password` | POST | Request password reset |
| `/auth/reset-password` | POST | Reset password with token |

## Security Best Practices

### Backend
- ✅ Use strong SECRET_KEY (generate with `openssl rand -hex 32`)
- ✅ Store sensitive credentials in `.env`
- ✅ Never commit `firebase-credentials.json`
- ✅ Enable CORS only for trusted origins
- ✅ Use HTTPS in production
- ✅ Rotate secrets regularly

### Frontend
- ✅ Never store sensitive data in localStorage
- ✅ Use environment variables for config
- ✅ Implement token refresh before expiry
- ✅ Clear tokens on logout
- ✅ Validate user input

## Troubleshooting

### Firebase Not Initialized
**Symptoms:** "Firebase not initialized" in backend logs

**Solutions:**
- Check if `firebase-credentials.json` exists
- Verify `FIREBASE_CREDENTIALS_PATH` in `.env`
- Ensure file permissions are correct
- Check Firebase project ID matches

### Google Sign-In Popup Blocked
**Symptoms:** Pop-up doesn't open

**Solutions:**
- Allow pop-ups in browser settings
- Add exception for localhost
- Try different browser
- Check console for errors

### CORS Errors
**Symptoms:** "CORS policy: No 'Access-Control-Allow-Origin' header"

**Solutions:**
- Add frontend URL to `CORS_ORIGINS` in backend `.env`
- Restart backend server
- Clear browser cache
- Check network tab for actual error

### Invalid Token Errors
**Symptoms:** 401 Unauthorized

**Solutions:**
- Check token expiry
- Verify SECRET_KEY matches
- Refresh token or re-login
- Check Authorization header format: `Bearer <token>`

## Development Workflow

1. **Start MongoDB:**
   ```bash
   mongod --dbpath=/path/to/data
   ```

2. **Start Backend:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

3. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

4. **Test:**
   - Open browser: `http://localhost:3000`
   - Try email registration
   - Try Google sign-in
   - Check API docs: `http://localhost:8000/docs`

## Production Deployment

### Backend
- Set `DEBUG=False`
- Use production SECRET_KEY
- Configure production MONGODB_URL
- Enable HTTPS
- Set proper CORS_ORIGINS
- Use environment variables (no .env file)

### Frontend
- Build: `npm run build`
- Deploy `dist/` folder
- Set production API URL
- Configure Firebase for production domain
- Add domain to Firebase authorized domains

## Additional Resources

- [Firebase Auth Documentation](https://firebase.google.com/docs/auth)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
