# Firebase Setup Instructions

## Backend Setup

### 1. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" or select existing project
3. Follow the setup wizard

### 2. Enable Authentication
1. In Firebase Console, go to Authentication > Sign-in method
2. Enable "Email/Password" provider
3. Enable "Google" provider

### 3. Get Service Account Credentials
1. Go to Project Settings > Service Accounts
2. Click "Generate new private key"
3. Save the downloaded JSON file as `firebase-credentials.json` in the backend root
4. Update `.env` file:
   ```
   FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
   FIREBASE_PROJECT_ID=your-project-id
   ```

### 4. Install Firebase Admin SDK
```bash
cd backend
pip install firebase-admin==6.3.0
```

## Frontend Setup

### 1. Get Firebase Config
1. In Firebase Console, go to Project Settings > General
2. Scroll to "Your apps" section
3. Click "Add app" > Web (</>) 
4. Register your app
5. Copy the Firebase config object

### 2. Create Frontend Environment File
Create `frontend/.env.local`:
```env
VITE_FIREBASE_API_KEY=your-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
```

### 3. Install Firebase SDK
```bash
cd frontend
npm install firebase
```

## Testing Authentication

### Email/Password Login
```bash
POST http://localhost:8000/auth/register
{
  "email": "user@example.com",
  "username": "testuser",
  "password": "Test@123"
}

POST http://localhost:8000/auth/login
{
  "email": "user@example.com",
  "password": "Test@123"
}
```

### Google OAuth Login
```bash
POST http://localhost:8000/auth/google
{
  "id_token": "firebase-id-token-from-frontend"
}
```

## Security Notes

⚠️ **Important:**
- Never commit `firebase-credentials.json` to version control
- Add to `.gitignore`: `firebase-credentials.json`
- Use environment variables for sensitive data
- Rotate credentials regularly
- Restrict API keys in Firebase Console

## Troubleshooting

### Firebase Not Initialized
- Check if `firebase-credentials.json` exists
- Verify file path in `.env`
- Check file permissions

### Authentication Errors
- Verify Firebase project ID
- Check if authentication methods are enabled
- Ensure service account has proper permissions

### CORS Issues
- Add your frontend URL to CORS_ORIGINS in backend `.env`
- Configure authorized domains in Firebase Console
