# Deploying WanderAI Backend to Render.com

This guide walks you through deploying the WanderAI backend on Render.com.

## Prerequisites

1. A Render.com account
2. Your codebase pushed to GitHub/GitLab

## Setup Steps

### 1. Create a new Web Service

1. Go to your Render Dashboard
2. Click **New** and select **Web Service**
3. Connect your GitHub/GitLab repository
4. Configure the service:
   - **Name**: `wanderai-backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `cd wanderlustai_backend && gunicorn wanderlustai_backend.wsgi:application --bind 0.0.0.0:$PORT`

### 2. Configure Environment Variables

Add the following environment variables:

- `DJANGO_SECRET_KEY`: Generate a secure key
- `DJANGO_DEBUG`: Set to `False`
- `DJANGO_ALLOWED_HOSTS`: `wanderai-backend.onrender.com,your-custom-domain.com`
- `CORS_ALLOWED_ORIGINS`: `https://your-frontend-url.com`
- `OPENAI_API_KEY`: Your OpenAI API key
- `OLA_APP_TOKEN`: Your Ola Maps API token

### 3. Set Up Database

#### Option 1: Use Render PostgreSQL

1. Go to your Render Dashboard
2. Click **New** and select **PostgreSQL**
3. Configure the database:
   - **Name**: `wanderai-db`
   - **User**: `wanderai_user`
   - **Database**: `wanderai`
4. After creation, copy the "Internal Connection String"
5. Add it as an environment variable in your Web Service:
   - `DATABASE_URL`: `<paste connection string>`

#### Option 2: Continue Using Supabase

Add these environment variables to your Web Service:
- `SUPABASE_HOST`: Your Supabase host
- `SUPABASE_PASSWORD`: Your Supabase database password

### 4. Deploy Your Service

Click **Create Web Service** to deploy.

Your backend will be available at: `https://wanderai-backend.onrender.com`

## Updating Your Frontend

Update your frontend API configuration:

```dart
// lib/core/constants/string/api_constants.dart
class ApiConstants {
  static const String baseUrl = 'https://wanderai-backend.onrender.com/api';
  // ...rest of your code
}
```

## Troubleshooting

- Check Render logs for deployment issues
- Ensure environment variables are correctly set
- Verify database connection is working 