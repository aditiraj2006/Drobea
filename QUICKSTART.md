# Drobea - Quick Start Guide

## ✅ Prerequisites
- Python 3.13+ installed
- Node.js 18+ installed
- MongoDB installed and running
- Firebase project created (optional, for Google OAuth)

## 🚀 Quick Start (5 minutes)

### 1. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies
```bash
cd frontend
npm install
```

### 3. Configure Backend Environment
Create `backend/.env` (or copy from `.env` if exists):
```env
# Required
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=drobea
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:5173

# Optional (for Google OAuth)
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
FIREBASE_PROJECT_ID=your-firebase-project-id
```

### 4. Configure Frontend Environment
Create `frontend/.env.local`:
```env
# Required
VITE_API_URL=http://localhost:8000

# Optional (for Google OAuth)
VITE_FIREBASE_API_KEY=your-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
```

### 5. Start MongoDB
```bash
# Windows
mongod

# macOS/Linux
sudo systemctl start mongod
```

### 6. Start Backend Server
```bash
cd backend
python -m uvicorn app.main:app --reload
```

Backend will run on: **http://localhost:8000**

API Docs: **http://localhost:8000/docs**

### 7. Start Frontend Server
```bash
cd frontend
npm run dev
```

Frontend will run on: **http://localhost:3000** or **http://localhost:3001**

## 🎯 Testing Authentication

### Email/Password Registration
1. Go to http://localhost:3000/register
2. Fill in:
   - Email: test@example.com
   - Username: testuser
   - Password: Test@12345
3. Click "Sign up"
4. You'll be redirected to dashboard

### Email/Password Login
1. Go to http://localhost:3000/login
2. Enter credentials
3. Click "Sign in"

### Google OAuth (Optional)
1. Complete Firebase setup (see `FIREBASE_SETUP.md`)
2. Add Firebase credentials
3. Restart both servers
4. Click "Continue with Google" button
5. Select Google account

## 📝 Available Features

### Currently Working:
- ✅ Email/Password Registration
- ✅ Email/Password Login
- ✅ Google OAuth Sign-in (with Firebase)
- ✅ JWT Token Authentication
- ✅ Protected Routes
- ✅ Dark Mode Toggle
- ✅ Responsive Navbar & Sidebar
- ✅ Dashboard Page
- ✅ User Profile Management

### Coming Soon:
- Wardrobe Management
- Outfit Planner
- Virtual Try-On
- AI Recommendations
- Social Features
- Analytics

## 🛠️ Development Commands

### Backend
```bash
# Run server with auto-reload
cd backend
python -m uvicorn app.main:app --reload

# Run on different port
python -m uvicorn app.main:app --reload --port 8001

# Install new package
pip install package-name
pip freeze > requirements.txt
```

### Frontend
```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Install new package
npm install package-name
```

## 🔧 Troubleshooting

### Backend won't start
- ✅ Check if MongoDB is running
- ✅ Verify Python packages installed: `pip list`
- ✅ Check `.env` file exists in backend folder
- ✅ Try: `pip install -r requirements.txt --force-reinstall`

### Frontend won't start
- ✅ Check if node_modules exists
- ✅ Try: `npm install --legacy-peer-deps`
- ✅ Clear cache: `npm cache clean --force`
- ✅ Delete node_modules and reinstall

### Google Sign-In not working
- ✅ Firebase not configured (it's optional)
- ✅ Button will be disabled if Firebase credentials missing
- ✅ Check browser console for errors
- ✅ See `FIREBASE_SETUP.md` for complete setup

### CORS Errors
- ✅ Add your frontend URL to `CORS_ORIGINS` in backend `.env`
- ✅ Restart backend server
- ✅ Clear browser cache

### Database Connection Error
- ✅ Ensure MongoDB is running: `mongod`
- ✅ Check MONGODB_URL in `.env`
- ✅ Test connection: `mongo` or `mongosh`

## 📚 Additional Documentation

- **Authentication Setup**: `AUTH_SETUP.md`
- **Firebase Setup**: `FIREBASE_SETUP.md`
- **Backend README**: `backend/README.md`
- **Frontend README**: `frontend/README.md`

## 🎨 Tech Stack

**Frontend:**
- React 18 + TypeScript
- Vite (Build Tool)
- TailwindCSS (Styling)
- React Router (Routing)
- TanStack Query (Data Fetching)
- Firebase (Google OAuth)
- Axios (HTTP Client)

**Backend:**
- FastAPI (Python)
- MongoDB + Motor (Database)
- Firebase Admin SDK (OAuth)
- JWT (Authentication)
- Bcrypt (Password Hashing)
- Pydantic (Validation)

## 💡 Tips

1. **Use VS Code** with these extensions:
   - Python
   - Pylance
   - ES7+ React/Redux/React-Native snippets
   - Tailwind CSS IntelliSense
   - MongoDB for VS Code

2. **API Documentation**: Visit `http://localhost:8000/docs` for interactive API docs

3. **Hot Reload**: Both backend and frontend have auto-reload enabled

4. **Dark Mode**: Toggle with the moon/sun icon in navbar

5. **Sidebar**: Click arrow button on sidebar edge to collapse/expand

## 🚨 Important Notes

- ⚠️ Never commit `.env` files or `firebase-credentials.json`
- ⚠️ Change `SECRET_KEY` in production
- ⚠️ Use HTTPS in production
- ⚠️ Firebase is optional (only for Google OAuth)
- ⚠️ Email/Password auth works without Firebase

## 🎉 You're Ready!

Your Drobea development environment is now set up!

Visit **http://localhost:3000** and start building your AI-powered clothing navigator! 🚀
