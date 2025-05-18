# WanderAI Project Setup Guide

This guide will help you set up the WanderAI project for development.

## Backend Setup

1. **Create and activate a virtual environment**:
   ```bash
   cd wanderai-backend
   python -m venv abc
   .\abc\Scripts\activate  # Windows
   source abc/bin/activate  # macOS/Linux
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install django-environ psycopg2-binary
   ```

3. **Create a `.env` file in the wanderai-backend directory**:
   ```
   # Django settings
   DJANGO_SECRET_KEY=your_secret_key_here
   DEBUG=True

   # Database (for development)
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=your_password_here
   DB_HOST=localhost
   DB_PORT=5432

   # Database (Supabase PostgreSQL)
   SUPABASE_DB_NAME=postgres
   SUPABASE_DB_USER=postgres
   SUPABASE_DB_PASSWORD=your_supabase_password
   SUPABASE_DB_HOST=db.your-project-ref.supabase.co
   SUPABASE_DB_PORT=5432

   # Supabase API
   SUPABASE_URL=https://your-project-ref.supabase.co
   SUPABASE_KEY=your_anon_key_here

   # OpenRouter AI API (get from openrouter.ai)
   OPENROUTER_API_KEY=your_openrouter_key_here

   # Ola Maps API (get from maps.olacabs.com)
   OLA_MAPS_API_KEY=your_ola_maps_key_here

   # Deployment settings (for production)
   ALLOWED_HOSTS=wanderai-backend.fly.dev,localhost,127.0.0.1
   CORS_ALLOWED_ORIGINS=https://wanderai.app,http://localhost:3000,http://127.0.0.1:3000
   CSRF_TRUSTED_ORIGINS=https://wanderai.app,http://localhost:3000,http://127.0.0.1:3000
   ```

4. **Run migrations and start the development server**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

## Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd wanderai-frontend
   ```

2. **Create a `.env` file in the wanderai-frontend directory**:
   ```
   # API URL
   API_BASE_URL=http://localhost:8000

   # Map tile provider (use OpenStreetMap)
   MAP_TILE_URL=https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png

   # Supabase for auth
   SUPABASE_URL=https://your-project-ref.supabase.co
   SUPABASE_ANON_KEY=your_anon_key_here
   ```

3. **Install Flutter dependencies**:
   ```bash
   flutter pub get
   ```

4. **Generate required files**:
   ```bash
   dart run build_runner build --delete-conflicting-outputs
   ```

5. **Run the Flutter app**:
   ```bash
   flutter run
   ```

## Project Structure

### Backend
- **AI Module**: AI-powered travel recommendations
- **Travels Module**: Journey and calendar management
- **Maps Module**: Geographic data integration
- **Users Module**: User authentication and profiles
- **Integrations**: External API clients (Supabase, OpenRouter, Maps)

### Frontend
- **Core**: Foundation components, theme management
- **Product**: Business logic, models, repositories
- **View**: UI screens and components
- **Features**: New feature modules using clean architecture

## API Features

### Health Check Endpoint
The backend includes a health check endpoint at `/api/health/` that returns a 200 OK response if the application is running properly. This is useful for monitoring and deployment platforms to verify the application's health.

To test the health check:
```bash
curl http://localhost:8000/api/health/
```

### API Documentation
API documentation is available at:
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- Schema: `/api/schema/`

## API Keys Required
- Supabase project (for authentication and database)
- OpenRouter API key (for AI features)
- Maps API key (for geographical features)

## Development Tips
- The backend is set up to use SQLite in development mode
- For production, configure PostgreSQL database connection
- The frontend uses Flutter for cross-platform deployment 