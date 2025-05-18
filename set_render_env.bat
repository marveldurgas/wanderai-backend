@echo off
REM Script to set environment variables for Render.com deployment (Windows version)

REM Generate a random secret key (simpler version for Windows)
for /f "tokens=*" %%a in ('powershell -Command "[System.Guid]::NewGuid().ToString()"') do set RANDOM_KEY=%%a

REM Set environment variables
render env set DJANGO_SETTINGS_MODULE=wanderlustai_backend.settings
render env set DJANGO_SECRET_KEY=%RANDOM_KEY%
render env set DJANGO_ALLOWED_HOSTS="wanderai-backend.onrender.com,render.com,localhost,127.0.0.1"
render env set DJANGO_DEBUG="False"
render env set CORS_ALLOWED_ORIGINS="https://wanderai.app,http://localhost:3000,http://127.0.0.1:3000"
render env set OPENAI_API_KEY="your-openai-api-key"
render env set OLA_APP_TOKEN="your-ola-app-token"

echo Environment variables set for Render.com
echo Don't forget to update OPENAI_API_KEY and OLA_APP_TOKEN with your actual keys! 