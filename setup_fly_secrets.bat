@echo off
echo Setting up Fly.io secrets for deployment...

REM Run these commands to set up Fly.io secrets
fly secrets set ^
  DJANGO_SECRET_KEY="5gvXdHYM0RHtBdL-YonM3woKwhyoUPcNOUgnyFGAbiuikjG9G7eBrnUKWTYBNBo1epg" ^
  DJANGO_DEBUG="False" ^
  DJANGO_ALLOWED_HOSTS="wanderai-backend.fly.dev,localhost,127.0.0.1" ^
  CORS_ALLOWED_ORIGINS="https://wanderai.app,http://localhost:3000,http://127.0.0.1:3000" ^
  SUPABASE_DB_HOST="db.zpfcxjkrihvsuumwmylv.supabase.co" ^
  SUPABASE_DB_PASSWORD="QsXQew5sKHA68Dla" ^
  SUPABASE_URL="https://zpfcxjkrihvsuumwmylv.supabase.co" ^
  SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwZmN4amtyaWh2c3V1bXdteWx2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDcxNDQ1ODgsImV4cCI6MjA2MjcyMDU4OH0.ff55krJMf1mkOBBVHzhbEfCZDPm2d0pjAF7H8hiuPvE" ^
  OPENROUTER_API_KEY="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" ^
  OLA_MAPS_API_KEY="SxJhsrEpqjBqIdicTM7OsQcaFSRC0KRoq43BiRQf"

echo Fly.io secrets set successfully!
echo You can now deploy your application with 'fly deploy' 