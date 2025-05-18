@echo off
echo Creating .env file with your configuration...

(
echo # Django settings
echo DJANGO_SECRET_KEY=5gvXdHYM0RHtBdL-YonM3woKwhyoUPcNOUgnyFGAbiuikjG9G7eBrnUKWTYBNBo1epg
echo DEBUG=True
echo.
echo # Database (for development)
echo DB_NAME=postgres
echo DB_USER=postgres
echo DB_PASSWORD=your_password_here
echo DB_HOST=localhost
echo DB_PORT=5432
echo.
echo # Database (Supabase PostgreSQL)
echo SUPABASE_DB_NAME=postgres
echo SUPABASE_DB_USER=postgres
echo SUPABASE_DB_PASSWORD=QsXQew5sKHA68Dla
echo SUPABASE_DB_HOST=db.zpfcxjkrihvsuumwmylv.supabase.co
echo SUPABASE_DB_PORT=5432
echo.
echo # Supabase API
echo SUPABASE_URL=https://zpfcxjkrihvsuumwmylv.supabase.co
echo SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwZmN4amtyaWh2c3V1bXdteWx2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDcxNDQ1ODgsImV4cCI6MjA2MjcyMDU4OH0.ff55krJMf1mkOBBVHzhbEfCZDPm2d0pjAF7H8hiuPvE
echo.
echo # OpenRouter AI API (get from openrouter.ai)
echo OPENROUTER_API_KEY=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
echo.              
echo # Ola Maps API (get from maps.olacabs.com)
echo OLA_MAPS_API_KEY=SxJhsrEpqjBqIdicTM7OsQcaFSRC0KRoq43BiRQf
echo.
echo # Deployment settings (for production)
echo ALLOWED_HOSTS=wanderai-backend.fly.dev,localhost,127.0.0.1
echo CORS_ALLOWED_ORIGINS=https://wanderai.app,http://localhost:3000,http://127.0.0.1:3000
) > .env

echo .env file created successfully!
echo You can now run start.bat to start the application. 