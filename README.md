# PulseNotify

PulseNotify is a flight price monitoring service. It tracks fares in the background and notifies users asynchronously when prices drop below their targets.

## Running the Services

To run this application locally, you will need to spin up three separate processes. Each handles a different part of the architecture:

### 1. Django API Server
This serves the REST API endpoints for user authentication and configuring price alerts.
```bash
source venv/bin/activate
python manage.py runserver
```

### 2. Celery Worker
The worker processes background tasks asynchronously (like querying current prices and saving notifications). Running these in a worker ensures that API responses remain fast and non-blocking for the user.
```bash
source venv/bin/activate
celery -A pulsenotify worker --loglevel=info
```

### 3. Celery Beat Scheduler
The beat scheduler acts as the clock. It triggers the scheduled price check job every 60 seconds and pushes it to the Celery queue.
```bash
source venv/bin/activate
celery -A pulsenotify beat --loglevel=info
```

---

## Local Setup

### 1. Spin up Postgres & Redis
Start the database and message broker services via Docker:
```bash
docker compose up -d
```

### 2. Migrations and Admin Seeding
Apply database migrations and seed a default admin user (`admin` / `adminpass`) for testing permission-restricted endpoints:
```bash
source venv/bin/activate
python manage.py migrate
python seed_admin.py
```
