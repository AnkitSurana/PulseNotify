# PulseNotify

A Django-based notification service that sends real-time alerts and notifications to users. Built with Django, Django REST Framework, Celery, and Redis for asynchronous task processing.

## Features

📬 **Multi-Channel Notifications** — Email, SMS, in-app notifications  
⚙️ **Async Task Queue** — Celery + Redis for background processing  
🔐 **User Authentication** — JWT-based auth with SimpleJWT  
🗄️ **Persistent Storage** — PostgreSQL for reliable data persistence  
🚀 **Scalable Architecture** — Task queue for handling high notification volume  
📊 **Analytics Ready** — Track notification delivery & engagement  

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL
- Redis (for Celery)
- pip

### Local Development

1. **Clone and setup:**
   ```bash
   git clone https://github.com/AnkitSurana/PulseNotify.git
   cd PulseNotify
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Initialize database:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Start Redis (in another terminal):**
   ```bash
   redis-server
   ```

6. **Start Celery worker (in another terminal):**
   ```bash
   celery -A pulsenotify worker -l info
   ```

7. **Run development server:**
   ```bash
   python manage.py runserver
   ```
   API available at `http://127.0.0.1:8000/api/`

## API Endpoints

### User Authentication

```bash
POST /api/auth/register
  body: { "email": "user@example.com", "password": "secure123" }

POST /api/auth/login
  body: { "email": "user@example.com", "password": "secure123" }
  response: { "access": "jwt_token", "refresh": "refresh_token" }

POST /api/auth/refresh
  body: { "refresh": "refresh_token" }
```

### Notifications

```bash
GET /api/notifications/
  → List all notifications for authenticated user

POST /api/notifications/send
  body: {
    "user_id": "uuid",
    "title": "Welcome",
    "message": "You're all set!",
    "type": "email",  # or "sms", "in_app"
    "data": { ... }
  }

GET /api/notifications/{id}/
  → Get notification details

PUT /api/notifications/{id}/mark-read
  → Mark notification as read
```

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|----------|
| Framework | Django 4.2 | Web framework |
| API | Django REST Framework 3.15 | REST API |
| Auth | djangorestframework-simplejwt | JWT authentication |
| Tasks | Celery 5.3 | Async task queue |
| Cache | Redis 5.0 | Task broker & cache |
| Database | PostgreSQL 13+ | Primary data store |
| Environment | python-dotenv | Config management |

## Architecture

```
PulseNotify/
├── core/
│   ├── models.py          # User, Notification, Template models
│   ├── views.py           # API viewsets
│   ├── serializers.py     # DRF serializers
│   ├── tasks.py           # Celery async tasks
│   └── permissions.py     # Custom permission classes
├── pulsenotify/
│   ├── settings.py        # Django settings
│   ├── celery.py          # Celery configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI app
├── requirements.txt       # Dependencies
├── manage.py              # Django CLI
├── .env.example           # Environment template
└── README.md
```

## Environment Variables (`.env`)

```env
# ── Database ────────────────────────────────────────────
DATABASE_URL=postgresql://user:password@localhost:5432/pulsenotify
DB_NAME=pulsenotify
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# ── Django ──────────────────────────────────────────────
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# ── Redis & Celery ──────────────────────────────────────
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# ── Email (SMTP) ────────────────────────────────────────
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# ── SMS (Twilio - Optional) ─────────────────────────────
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+1234567890
```

## Key Features Explained

### Async Notifications with Celery

Notifications are sent asynchronously to avoid blocking requests:

```python
from celery import shared_task

@shared_task
def send_notification(user_id, title, message, notification_type):
    # This runs in background worker, not in request handler
    user = User.objects.get(id=user_id)
    send_email(user.email, title, message)
    return f"Notification sent to {user_id}"
```

### Task Monitoring

Monitor Celery tasks using Flower:

```bash
pip install flower
celery -A pulsenotify events
flower -A pulsenotify --port=5555
```

Visit `http://localhost:5555` to view task status.

## Deployment

### Using Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "pulsenotify.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Heroku

```bash
heroku create pulsenotify-app
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:premium-0
git push heroku main
```

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test core

# With coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## Common Issues

### Redis connection failed
```bash
# Ensure Redis is running
redis-cli ping
# Should return: PONG

# Or start Redis
redis-server
```

### Celery tasks not executing
- Check Redis is running: `redis-cli ping`
- Check Celery worker is running: `celery -A pulsenotify worker -l info`
- Check worker logs for errors

### Database migration errors
```bash
python manage.py makemigrations
python manage.py migrate
```

## Contributing

We welcome contributions! Areas we need:

- SMS/Slack notification channels
- Notification scheduling
- Better retry logic
- Admin dashboard for notifications
- Push notification support

## License

MIT License — see [LICENSE](LICENSE)

## Support

- 📧 Email: ankitsurana002@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/AnkitSurana/PulseNotify/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/AnkitSurana/PulseNotify/discussions)

## Links

- **Django Docs**: [djangoproject.com](https://djangoproject.com)
- **Celery Docs**: [docs.celeryproject.org](https://docs.celeryproject.org)
- **DRF**: [django-rest-framework.org](https://www.django-rest-framework.org/)

---

Made with ❤️ by [Ankit Surana](https://github.com/AnkitSurana)
