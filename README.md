# Drobea (वस्त्रसारथी) - AI-Powered Clothing Navigator

A comprehensive digital wardrobe platform that combines AI-powered outfit recommendations with realistic virtual try-on capabilities using generative AI.

## 🌟 Features

### Core Features
- **Digital Wardrobe Management**: AI-powered clothing item organization and tagging
- **Virtual Try-On**: Realistic AI-generated virtual try-on using Gemini and Stable Diffusion
- **Smart Outfit Planning**: AI-powered outfit recommendations and calendar integration
- **Social Community**: Share outfits, follow users, and participate in style challenges
- **Analytics Dashboard**: Comprehensive wardrobe and style insights
- **Shopping Integration**: Wishlist management and product recommendations

### AI-Powered Features
- **Auto-Tagging**: Automatic clothing categorization and tagging
- **Color Analysis**: Personal color palette analysis and recommendations
- **Style Recommendations**: Personalized style suggestions based on preferences
- **Virtual Try-On**: High-quality AI-generated try-on images
- **Trend Analysis**: Fashion trend detection and recommendations

## 🚀 Tech Stack

### Backend
- **Framework**: Python with FastAPI
- **Database**: MongoDB with Motor driver
- **AI/ML**: TensorFlow, PyTorch, OpenCV, scikit-learn
- **Image Processing**: rembg, Pillow, OpenCV
- **AI Services**: Google Gemini API, Stable Diffusion
- **File Storage**: Cloudinary
- **Authentication**: JWT tokens

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Query + Context API
- **Routing**: React Router DOM
- **UI Components**: Framer Motion, React DnD
- **Charts**: Chart.js
- **Build Tool**: Vite

## 📁 Project Structure

```
Drobea/
├── backend/     # FastAPI backend
│   ├── app/
│   │   ├── models/           # Pydantic models
│   │   ├── routes/           # API routes
│   │   ├── services/         # Business logic
│   │   └── utils/            # Utilities
│   ├── requirements.txt
│   └── README.md
├── frontend/    # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   └── types/           # TypeScript types
│   ├── package.json
│   └── README.md
└── README.md
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB
- Git

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
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

5. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to http://localhost:3000

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=drobea
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

#### Frontend (.env.local)
```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Drobea
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 Key Features Implementation

### Virtual Try-On System
- **Pose Detection**: MediaPipe for body pose analysis
- **AI Generation**: Gemini API for high-quality image generation
- **Fallback System**: Stable Diffusion as backup
- **Quality Assessment**: User rating and feedback system

### Wardrobe Management
- **Auto-Tagging**: AI-powered clothing categorization
- **Color Analysis**: Dominant color extraction and analysis
- **Smart Search**: Natural language search capabilities
- **Bulk Operations**: Efficient batch processing

### Outfit Planning
- **Visual Builder**: Drag-and-drop outfit creation
- **Calendar Integration**: Event-based outfit planning
- **Weather Integration**: Weather-aware recommendations
- **Packing Lists**: Trip-specific packing suggestions

### Social Features
- **Community Feed**: User-generated content sharing
- **Style Challenges**: Community competitions
- **Follow System**: User connections and interactions
- **Outfit Sharing**: Social outfit sharing

## 🚀 Deployment

### Docker Deployment
```bash
# Backend
cd backend
docker build -t backend .
docker run -p 8000:8000 backend

# Frontend
cd frontend
docker build -t frontend .
docker run -p 3000:3000 frontend
```

### Production Deployment
1. Set up production MongoDB
2. Configure environment variables
3. Set up reverse proxy (nginx)
4. Enable HTTPS
5. Use process manager (PM2, systemd)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini API for AI image generation
- Stable Diffusion for fallback generation
- MediaPipe for pose detection
- The open-source community for amazing libraries

## 📞 Support

For support, email support@Drobea.com or join our Discord community.

## 🔮 Roadmap

- [ ] Mobile app (React Native)
- [ ] AR try-on capabilities
- [ ] Advanced AI styling recommendations
- [ ] Integration with major e-commerce platforms
- [ ] Sustainability tracking and recommendations
- [ ] Multi-language support

---

**Drobea** - Your AI-Powered Clothing Navigator 🎨✨
