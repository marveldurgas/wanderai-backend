#!/bin/bash
echo "Creating .env file with your configuration..."

cat > .env << EOL
# Django settings
DJANGO_SECRET_KEY=5gvXdHYM0RHtBdL-YonM3woKwhyoUPcNOUgnyFGAbiuikjG9G7eBrnUKWTYBNBo1epg
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
SUPABASE_DB_PASSWORD=QsXQew5sKHA68Dla
SUPABASE_DB_HOST=db.zpfcxjkrihvsuumwmylv.supabase.co
SUPABASE_DB_PORT=5432

# Supabase API
SUPABASE_URL=https://zpfcxjkrihvsuumwmylv.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwZmN4amtyaWh2c3V1bXdteWx2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDcxNDQ1ODgsImV4cCI6MjA2MjcyMDU4OH0.ff55krJMf1mkOBBVHzhbEfCZDPm2d0pjAF7H8hiuPvE

# OpenRouter AI API (get from openrouter.ai)
OPENROUTER_API_KEY=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
              
# Ola Maps API (get from maps.olacabs.com)
OLA_MAPS_API_KEY=SxJhsrEpqjBqIdicTM7OsQcaFSRC0KRoq43BiRQf

# Deployment settings (for production)
ALLOWED_HOSTS=wanderai-backend.fly.dev,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://wanderai.app,http://localhost:3000,http://127.0.0.1:3000
EOL

echo ".env file created successfully!"
echo "You can now run start.sh to start the application."

# Make this script executable
chmod +x setup_env.sh 