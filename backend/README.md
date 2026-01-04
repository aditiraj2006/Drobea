# Drobea Backend

AI-Powered Clothing Navigator with Virtual Try-On capabilities.

## Features

- **User Authentication & Management**: JWT-based auth with user profiles
- **Digital Wardrobe**: AI-powered clothing item management and organization
- **Virtual Try-On**: AI-generated virtual try-on using Gemini and Stable Diffusion
- **Outfit Planning**: Smart outfit recommendations and calendar integration
- **Social Features**: Community sharing and interaction
- **Analytics**: Comprehensive wardrobe and style analytics
- **Shopping Integration**: Wishlist and product management

## Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB with Motor (async driver)
- **AI/ML**: TensorFlow, PyTorch, OpenCV, scikit-learn
- **Image Processing**: rembg, Pillow, OpenCV
- **AI Services**: Google Gemini API, Stable Diffusion
- **File Storage**: Cloudinary
- **Authentication**: JWT tokens

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd drobea-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Set up MongoDB**
   - Install MongoDB locally or use MongoDB Atlas
   - Update `MONGODB_URL` in `.env`

6. **Run database migrations**
   ```bash
   python -m app.services.database.migrations
   ```

7. **Start the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Environment Variables

```env
# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=drobea

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Google Gemini
GEMINI_API_KEY=your-gemini-api-key

# Stable Diffusion
STABLE_DIFFUSION_API_URL=http://localhost:7860
STABLE_DIFFUSION_API_KEY=your-sd-api-key

# Weather API
WEATHER_API_KEY=your-weather-api-key

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# App Settings
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
drobea-backend/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── models/                 # Pydantic models
│   ├── routes/                 # API routes
│   ├── services/               # Business logic
│   │   ├── ai/                # AI services
│   │   ├── database/          # Database operations
│   │   ├── storage/           # File storage
│   │   └── external/          # External API integrations
│   ├── utils/                 # Utility functions
│   └── tests/                 # Test files
├── requirements.txt
├── Dockerfile
└── README.md
```

## Key Features Implementation

### Virtual Try-On
- Pose detection using MediaPipe
- AI image generation with Gemini API
- Fallback to Stable Diffusion
- Quality assessment and rating

### AI Services
- Auto-tagging of clothing items
- Color analysis and recommendations
- Style preference learning
- Outfit generation and suggestions

### Database Design
- User management with social features
- Wardrobe items with AI tags
- Outfit planning and calendar integration
- Analytics and usage tracking

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
isort .
```

### Type Checking
```bash
mypy .
```

## Deployment

### Docker
```bash
docker build -t drobea-backend .
docker run -p 8000:8000 drobea-backend
```

### Production
1. Set up production MongoDB
2. Configure environment variables
3. Set up reverse proxy (nginx)
4. Use process manager (PM2, systemd)
5. Enable HTTPS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
