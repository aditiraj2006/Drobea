import { initializeApp, FirebaseApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider, Auth } from 'firebase/auth'

// Firebase configuration from environment variables
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
}

// Initialize Firebase
let app: FirebaseApp | undefined
let auth: Auth | undefined
let googleProvider: GoogleAuthProvider | undefined

try {
  // Check if all required config values are present
  if (firebaseConfig.apiKey && firebaseConfig.projectId) {
    app = initializeApp(firebaseConfig)
    auth = getAuth(app)
    googleProvider = new GoogleAuthProvider()
    
    // Optional: Configure Google provider
    googleProvider.addScope('profile')
    googleProvider.addScope('email')
    
    console.log('✓ Firebase initialized successfully')
  } else {
    console.warn('⚠ Firebase configuration missing. Google OAuth will not be available.')
    console.warn('  Please set Firebase environment variables in .env.local')
  }
} catch (error) {
  console.error('✗ Firebase initialization error:', error)
}

export { auth, googleProvider }
export default app
