# WanderlustAI Backend

WanderlustAI is an AI-powered travel suggestion system that leverages OpenAI and Ola Maps API to provide personalized travel recommendations.

## Features

- User authentication and profile management
- AI-generated travel itineraries based on user preferences
- Transportation options through Ola Maps API integration
- Journey management with status tracking
- RESTful API for frontend integration

## Technology Stack

- Django 4.2.7
- Django REST Framework
- PostgreSQL (via Supabase)
- JWT Authentication
- OpenAI API
- Ola Maps API

## Setup and Installation

### Prerequisites

- Python 3.8+
- PostgreSQL (optional for development, required for production)
- API keys for OpenAI and Ola Maps

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/wanderlustai.git
   cd wanderlustai/wanderai-backend
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   OPENAI_API_KEY=your_openai_api_key
   OLA_APP_TOKEN=your_ola_app_token
   
   # For Supabase (production)
   USE_SUPABASE=False
   SUPABASE_HOST=your_supabase_host
   SUPABASE_PASSWORD=your_supabase_password
   ```

5. Apply migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

## API Documentation

After running the server, API documentation is available at:
- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- ReDoc: http://localhost:8000/api/schema/redoc/

## Deployment

### Deploy to Fly.io

#### Prerequisites

1. Install Fly.io CLI:
   ```bash
   # On Windows with PowerShell
   iwr https://fly.io/install.ps1 -useb | iex
   
   # On macOS/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. Login to Fly.io:
   ```bash
   fly auth login
   ```

#### Configuration

1. Set up environment secrets (replace values with your own):
   ```bash
   fly secrets set DJANGO_SECRET_KEY="your-secret-key-here" \
     DJANGO_DEBUG="False" \
     DJANGO_ALLOWED_HOSTS="wanderai-backend.fly.dev" \
     CORS_ALLOWED_ORIGINS="https://your-frontend-domain.com,http://localhost:3000" \
     SUPABASE_HOST="db.your-project-id.supabase.co" \
     SUPABASE_PASSWORD="your-database-password" \
     OPENAI_API_KEY="your-openrouter-api-key" \
     OLA_APP_TOKEN="your-ola-maps-api-token"
   ```

2. Launch the app (first-time deployment):
   ```bash
   fly launch
   ```

3. Deploy updates:
   ```bash
   fly deploy
   ```

#### Monitoring and Maintenance

- View logs:
  ```bash
  fly logs
  ```

- SSH into the app:
  ```bash
  fly ssh console
  ```

- Run Django management commands:
  ```bash
  fly ssh console -C "python manage.py createsuperuser"
  ```

### Deploy to custom server

1. Set up environment variables
2. Run the startup script:
   ```
   ./start.sh
   ```

## License

[MIT License](LICENSE)

## Contributors

- Your Name - Initial work

## Acknowledgments

- OpenAI for the AI capabilities
- Ola Maps for transportation API 