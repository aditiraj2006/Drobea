# Drobea Frontend

Modern React TypeScript frontend for the AI-Powered Clothing Navigator.

## Features

- **Modern UI**: Beautiful, responsive design with Tailwind CSS
- **Real-time Updates**: React Query for efficient data fetching
- **State Management**: Context API for global state
- **Authentication**: Secure JWT-based authentication
- **Virtual Try-On**: Interactive virtual try-on interface
- **Wardrobe Management**: Drag-and-drop wardrobe organization
- **Social Features**: Community sharing and interaction
- **Analytics Dashboard**: Comprehensive style insights

## Tech Stack

- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Query + Context API
- **Routing**: React Router DOM
- **UI Components**: Custom components with Framer Motion
- **Forms**: React Hook Form
- **Charts**: Chart.js
- **Build Tool**: Vite

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   Navigate to http://localhost:3000

## Environment Variables

```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Drobea
VITE_APP_VERSION=1.0.0
```

## Project Structure

```
frontend/
├── public/                     # Static assets
├── src/
│   ├── components/            # Reusable components
│   │   ├── layout/           # Layout components
│   │   ├── wardrobe/         # Wardrobe-specific components
│   │   ├── outfits/          # Outfit components
│   │   ├── ai/               # AI-related components
│   │   ├── social/           # Social features
│   │   └── common/           # Common components
│   ├── pages/                # Page components
│   ├── services/             # API services and context
│   ├── types/                # TypeScript type definitions
│   ├── styles/               # Global styles
│   ├── App.tsx               # Main app component
│   └── main.tsx              # Entry point
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── vite.config.ts
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Key Features

### Authentication
- Secure login/register with JWT
- Password strength validation
- Social login integration
- Password reset functionality

### Wardrobe Management
- Drag-and-drop item organization
- AI-powered auto-tagging
- Bulk upload with progress tracking
- Advanced filtering and search

### Virtual Try-On
- Reference photo upload
- Pose detection and analysis
- AI-generated try-on images
- Quality rating and feedback

### Outfit Planning
- Visual outfit builder
- Calendar integration
- Weather-based recommendations
- Packing list generator

### Social Features
- Community feed
- Outfit sharing
- Follow/unfollow users
- Style challenges

### Analytics
- Wardrobe usage statistics
- Cost-per-wear analysis
- Sustainability metrics
- Style trend insights

## Component Architecture

### Layout Components
- `Header`: Navigation and user menu
- `Sidebar`: Main navigation
- `Layout`: Main layout wrapper

### Wardrobe Components
- `WardrobeGrid`: Item grid display
- `ItemCard`: Individual item card
- `UploadWizard`: Multi-step upload process
- `WardrobeFilters`: Advanced filtering

### AI Components
- `VirtualTryOn`: Try-on interface
- `ColorAnalysis`: Color recommendation
- `StyleRecommendations`: AI suggestions
- `TryOnGenerator`: Image generation

### Common Components
- `Loading`: Loading states
- `Modal`: Reusable modal
- `Toast`: Notifications
- `ImageUpload`: File upload

## State Management

### Context Providers
- `AuthContext`: User authentication state
- `AppContext`: App-wide settings
- `NotificationContext`: Notification management

### React Query
- Automatic caching and synchronization
- Background updates
- Optimistic updates
- Error handling

## Styling

### Tailwind CSS
- Utility-first CSS framework
- Custom design system
- Responsive design
- Dark mode support

### Custom Components
- Consistent design tokens
- Reusable component library
- Accessibility features
- Animation support

## API Integration

### Service Layer
- Centralized API calls
- Type-safe requests/responses
- Error handling
- Request/response interceptors

### Authentication
- JWT token management
- Automatic token refresh
- Protected routes
- Role-based access

## Development Guidelines

### Code Style
- TypeScript strict mode
- ESLint configuration
- Prettier formatting
- Consistent naming conventions

### Component Guidelines
- Functional components with hooks
- Props interface definitions
- Error boundaries
- Loading states

### Testing
- Unit tests with Jest
- Component tests with React Testing Library
- E2E tests with Cypress

## Deployment

### Build Process
```bash
npm run build
```

### Production Build
- Optimized bundle
- Code splitting
- Asset optimization
- Environment configuration

### Deployment Options
- Vercel
- Netlify
- AWS S3 + CloudFront
- Docker container

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance

- Code splitting
- Lazy loading
- Image optimization
- Bundle analysis
- Performance monitoring

## License

This project is licensed under the MIT License.
