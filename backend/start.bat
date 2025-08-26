@echo off
echo 🚀 Starting Customer Management System...

REM Check if .env exists, if not create from example
if not exist ".env" (
    echo ⚠️  .env file not found, creating from .env.example...
    copy .env.example .env
    echo 📝 Please edit .env file with your configuration
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Check if PostgreSQL is running (simplified check)
echo 🔍 Checking PostgreSQL...
python -c "import psycopg2; psycopg2.connect(host='localhost', user='postgres', password='postgres', dbname='customer_db')" 2>nul
if errorlevel 1 (
    echo ❌ PostgreSQL not running. Starting with Docker...
    docker-compose up -d postgres redis
    echo ⏳ Waiting for services...
    timeout /t 10 /nobreak >nul
)

REM Check if Redis is running (simplified check)
echo 🔍 Checking Redis...
python -c "import redis; redis.Redis(host='localhost', port=6379, db=0).ping()" 2>nul
if errorlevel 1 (
    echo ❌ Redis not running. Starting with Docker...
    docker-compose up -d redis
    echo ⏳ Waiting for Redis...
    timeout /t 5 /nobreak >nul
)

REM Run the application
echo ✅ Starting FastAPI application...
python -m src.main
