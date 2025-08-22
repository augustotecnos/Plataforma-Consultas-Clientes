#!/bin/bash

# Customer Management System - Startup Script

echo "🚀 Starting Customer Management System..."

# Check if .env exists, if not create from example
if [ ! -f .env ]; then
    echo "⚠️  .env file not found, creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your configuration"
    exit 1
fi

# Check if PostgreSQL is running
if ! pg_isready -h localhost -p 5432 -U postgres > /dev/null 2>&1; then
    echo "❌ PostgreSQL is not running. Starting with Docker..."
    docker-compose up -d postgres redis
    echo "⏳ Waiting for PostgreSQL to be ready..."
    sleep 10
fi

# Check if Redis is running
if ! redis-cli ping > /dev/null 2>&1; then
    echo "❌ Redis is not running. Starting with Docker..."
    docker-compose up -d redis
    echo "⏳ Waiting for Redis to be ready..."
    sleep 5
fi

# Install dependencies if not already installed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Activate virtual environment
source venv/bin/activate

# Run the application
echo "✅ Starting FastAPI application..."
python -m src.main
