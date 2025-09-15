#!/bin/bash

# XobehStudio Deployment Script
echo "🚀 Setting up XobehStudio for deployment..."

# Create necessary directories
mkdir -p generated_images generated_videos

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📋 Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please update .env file with your API keys before running!"
fi

# Build and run with Docker Compose
echo "🔨 Building Docker containers..."
docker-compose build

echo "🏃 Starting services..."
docker-compose up -d

echo "✅ XobehStudio is running!"
echo "📱 API Documentation: http://localhost:8000/docs"
echo "🖼️  Images will be accessible at: http://localhost:8000/images/"

# Show running containers
docker-compose ps