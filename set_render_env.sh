#!/bin/bash
# Script to set environment variables for Render.com deployment

# Set environment variables
render env set \
  DJANGO_SETTINGS_MODULE=wanderlustai_backend.settings \
  DJANGO_SECRET_KEY=$(openssl rand -hex 32) \
  DJANGO_ALLOWED_HOSTS="wanderai-backend.onrender.com,render.com,localhost,127.0.0.1" \
  DJANGO_DEBUG="False" \
  CORS_ALLOWED_ORIGINS="https://wanderai.app,http://localhost:3000,http://127.0.0.1:3000" \
  OPENAI_API_KEY="your-openai-api-key" \
  OLA_APP_TOKEN="your-ola-app-token"

echo "Environment variables set for Render.com"
echo "Don't forget to update OPENAI_API_KEY and OLA_APP_TOKEN with your actual keys!" 