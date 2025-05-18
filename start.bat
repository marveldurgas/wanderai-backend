@echo off
echo Running WanderAI Backend startup script...

REM Apply database migrations
echo Applying database migrations...
python manage.py migrate --noinput

REM Create superuser if not exists
echo Creating superuser if not exists...
python manage.py shell -c "exec(open('create_superuser.py').read())"

REM Start gunicorn server
echo Starting Gunicorn server...
IF "%PORT%"=="" SET PORT=8000
gunicorn --bind 0.0.0.0:%PORT% wanderlustai_backend.wsgi:application 