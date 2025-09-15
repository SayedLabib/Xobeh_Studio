# 🎨 XobehStudio AI Services

A powerful AI-powered API platform for image generation, video creation, and dream interpretation using cutting-edge AI models.

## 🚀 Features

- **🌙 Dream Interpreter**: Interpret dreams and generate visual representations using Gemini Imagen
- **🎨 Image Generation**: Multiple AI models for image creation
  - DALL-E 3 (OpenAI)
  - Gemini Imagen 4.0 (Google)
  - Flux Kontext Dev (FAL.ai)
  - Flux Kontext Edit (FAL.ai) - Image editing
- **🎥 Video Generation**: AI-powered video creation
  - Gemini Veo 2.0
  - Gemini Veo 3.0
- **✨ Prompt Enhancement**: Improve your prompts for better AI results

## 📋 Prerequisites

- Docker & Docker Compose
- API Keys for:
  - OpenAI (GPT & DALL-E)
  - Google Gemini
  - FAL.ai

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/SayedLabib/Xobeh_Studio.git
cd Xobeh_Studio
```


## 📁 Project Structure

```
XobehStudio/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── core/
│   │   └── config.py          # Configuration management
│   ├── features/
│   │   ├── feature_1/         # Dream Interpreter
│   │   ├── feature_2/         # DALL-E
│   │   ├── feature_4/         # Video Generation (Veo 2)
│   │   ├── feature_5/         # Prompt Enhancement
│   │   ├── feature_7/         # Gemini Imagen
│   │   ├── feature_9/         # Flux Kontext Dev
│   │   ├── feature_10/        # Video Generation (Veo 3)
│   │   └── feature_11/        # Flux Kontext Edit
│   └── nginx/
│       └── nginx.conf         # Nginx configuration
├── generated_images/          # Generated images storage
├── generated_videos/          # Generated videos storage
├── docker-compose.yml         # Docker services
├── Dockerfile                 # Application container
├── requirements.txt           # Python dependencies
└── deploy scripts            # Deployment automation
```

## 🔧 Configuration

### Environment Variables
```bash
# API Keys
GEMINI_API_KEY=your_gemini_key
OPEN_AI_API_KEY=your_openai_key
FAL_API_KEY=your_fal_key

# Server Settings
BASE_URL=http://localhost:8069
PORT=8069

# Image Settings
IMAGE_WIDTH=1024
IMAGE_HEIGHT=1024
IMAGES_DIR=generated_images
```

### Style Options
- **Photo**: Photorealistic images
- **Illustration**: Artistic illustrations
- **Comic**: Comic book style
- **Anime**: Anime/manga style
- **Abstract**: Abstract art
- **Fantasy**: Fantasy themed
- **PopArt**: Pop art style

### Shape Options
- **square**: 1:1 aspect ratio
- **portrait**: Vertical orientation
- **landscape**: Horizontal orientation

## 🖼️ Generated Content Access

### Images
- **Development**: `http://localhost:8069/images/filename.jpg`
- **Production**: `http://localhost/images/filename.jpg`

### Videos
- **Development**: `http://localhost:8069/videos/filename.mp4`
- **Production**: `http://localhost/videos/filename.mp4`


## 🔒 Security

- CORS enabled for web applications
- Rate limiting protection
- File upload validation
- Security headers (XSS, CSRF protection)



**Made with ❤️ by XobehStudio Team**