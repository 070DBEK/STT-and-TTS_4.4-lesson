# Speech-to-Text and Text-to-Speech API

A Django REST Framework API that provides speech-to-text and text-to-speech conversion services using OpenAI's Whisper and TTS models.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **Speech-to-Text**: Convert audio files to text using OpenAI Whisper
- **Text-to-Speech**: Convert text to speech using OpenAI TTS
- **History Tracking**: Track all conversions with filtering and search
- **Async Processing**: Background processing using Celery
- **File Management**: Secure file upload and download
- **API Documentation**: Complete OpenAPI specification

## Quick Start

### 1. Clone the repository
\`\`\`bash
git clone <repository-url>
cd speech-api
\`\`\`

### 2. Install dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Set up environment variables
\`\`\`bash
cp .env.example .env
# Edit .env file with your OpenAI API key and other settings
\`\`\`

### 4. Run migrations
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

### 5. Create superuser (optional)
\`\`\`bash
python manage.py createsuperuser
\`\`\`

### 6. Start Redis (for Celery)
\`\`\`bash
# Using Docker
docker run -d -p 6379:6379 redis:alpine

# Or install Redis locally
\`\`\`

### 7. Start Celery worker
\`\`\`bash
celery -A config worker --loglevel=info
\`\`\`

### 8. Run the development server
\`\`\`bash
python manage.py runserver
\`\`\`

## Using Docker

### 1. Build and run with Docker Compose
\`\`\`bash
docker-compose up --build
\`\`\`

This will start:
- Django web server on port 8000
- Celery worker for background tasks
- Redis for task queue

## API Endpoints

### Authentication
- `POST /api/v1/auth/register/` - Register new user
- `POST /api/v1/auth/login/` - Login user
- `POST /api/v1/auth/token/refresh/` - Refresh access token

### User Profile
- `GET /api/v1/user/profile/` - Get user profile

### Speech-to-Text
- `POST /api/v1/stt/convert/` - Convert audio to text
- `GET /api/v1/stt/{id}/` - Get STT conversion details
- `GET /api/v1/stt/history/` - Get STT conversion history

### Text-to-Speech
- `POST /api/v1/tts/convert/` - Convert text to speech
- `GET /api/v1/tts/{id}/` - Get TTS conversion details
- `GET /api/v1/tts/{id}/audio/` - Download audio file
- `GET /api/v1/tts/history/` - Get TTS conversion history

## Example Usage

### 1. Register a user
\`\`\`bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
\`\`\`

### 2. Login
\`\`\`bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
\`\`\`

### 3. Convert speech to text
\`\`\`bash
curl -X POST http://localhost:8000/api/v1/stt/convert/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "audio=@path/to/audio.mp3" \
  -F "language=en" \
  -F "model=base"
\`\`\`

### 4. Convert text to speech
\`\`\`bash
curl -X POST http://localhost:8000/api/v1/tts/convert/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test message.",
    "voice": "nova",
    "language": "en",
    "speed": 1.0
  }'
\`\`\`

## Configuration

### Environment Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `OPENAI_API_KEY`: Your OpenAI API key
- `REDIS_URL`: Redis connection URL for Celery

### File Upload Limits
- Maximum file size: 25MB
- Supported audio formats: mp3, wav, m4a, mp4, mpeg, mpga, webm

### Supported Models
- **STT Models**: tiny, base, small, medium, large
- **TTS Voices**: alloy, echo, fable, onyx, nova, shimmer

## Project Structure

The project is organized into three Django apps following separation of concerns:

- **users**: User authentication, registration, and profile management
- **stt**: Speech-to-Text conversion functionality using OpenAI Whisper
- **tts**: Text-to-Speech conversion functionality using OpenAI TTS

### App Structure:
- `users/` - User management and authentication
- `stt/` - Speech-to-Text models, views, and tasks
- `tts/` - Text-to-Speech models, views, and tasks
- `config/` - Main Django project configuration

Each app contains:
- `models.py` - Database models
- `serializers.py` - API serializers for request/response handling
- `views.py` - API views and endpoints
- `tasks.py` - Celery background tasks
- `filters.py` - Django-filter configurations
- `urls.py` - URL routing
- `admin.py` - Django admin configuration

## Development

### Running Tests
\`\`\`bash
python manage.py test
\`\`\`

### Code Style
This project follows PEP 8 style guidelines. Use tools like `black` and `flake8` for code formatting and linting.

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Production Deployment

### 1. Set environment variables
\`\`\`bash
export SECRET_KEY="your-production-secret-key"
export DEBUG=False
export ALLOWED_HOSTS="yourdomain.com"
export OPENAI_API_KEY="your-openai-api-key"
\`\`\`

### 2. Use a production database
Update `DATABASES` setting in `settings.py` to use PostgreSQL or another production database.

### 3. Use a production web server
\`\`\`bash
pip install gunicorn
gunicorn config.wsgi:application
\`\`\`

### 4. Set up a reverse proxy
Configure Nginx or Apache to serve static files and proxy requests to Django.

### 5. Use a production task queue
Set up Redis or RabbitMQ for Celery in production.

## License

This project is licensed under the MIT License.
\`\`\`
\`\`\`python file="scripts/create_migrations.py"
#!/usr/bin/env python
"""
Script to create and apply database migrations
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import execute_from_command_line

def main():
    """Create and apply migrations"""
    print("Creating migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    print("Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("Migrations completed successfully!")

if __name__ == '__main__':
    main()
