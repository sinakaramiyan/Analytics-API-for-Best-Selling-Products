# 10 bestselling products

A Dockerized Django REST Framework API to serve last month's top 10 bestselling products, implementing Redis caching and Celery workers for optimized performance.

## 🚀 Features

- **Django REST Framework** - Robust API development
- **Redis** - Caching and message brokering
- **Celery** - Asynchronous task queue
- **Celery Beat** - Scheduled tasks
- **PostgreSQL** - Database
- **Docker** - Containerized development environment
- **JWT Authentication** - Secure API authentication

## 📋 Prerequisites

- Docker
- Docker Compose

## 🛠️ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/sinakaramiyan/Analytics-API-for-Best-Selling-Products.git
cd Analytics_API
```

### 2. Environment Setup
Create a .env file in the project root (optional - environment variables are set in docker-compose):
```env
# Database
DB_NAME=analytics_db
DB_USER=analytics_user
DB_PASSWORD=analytics_pass
DB_HOST=db
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# Redis/Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```
### 3. Build and Start Services

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### 4. Apply Database Migrations

```bash
docker-compose exec web python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
docker-compose exec web python manage.py createsuperuser
```
### 6. Initialize with test data

```bash
docker-compose exec web python manage.py generate_test_data
```
## 🔧 Services

| Service         | Port  | Description                     |
|-----------------|-------|---------------------------------|
| Web             | 8000  | Django development server      |
| PostgreSQL      | 5432  | Database                        |
| Redis           | 6379  | Cache and message broker        |
| Celery Worker   | –     | Background task processor       |
| Celery Beat     | –     | Scheduled task scheduler        |

## 📊 API Endpoints

### Authentication

| Method | Endpoint              | Description            |
|--------|-----------------------|------------------------|
| POST   | `/api/token/`         | Obtain JWT token       |
| POST   | `/api/token/refresh/` | Refresh JWT token      |

## 🔄 Celery Tasks

### Monitoring Celery

```bash
# Check worker status
docker-compose exec celery-worker celery -A config inspect active

# Check scheduled tasks
docker-compose exec celery-beat celery -A config beat status
```

## 🧪 Testing

### Run Redis Diagnostics

```bash
# Test Redis connections and cache
docker-compose exec web python test.py
```

## 🗄️ Database Operations

### Access Database
```bash
# Connect to PostgreSQL
docker-compose exec db psql -U analytics_user -d analytics_db
```

## 🛠️ Development Commands

### Common Docker Commands
```bash
# View running services
docker-compose ps

# View logs
docker-compose logs -f
docker-compose logs -f web      # Web service logs
docker-compose logs -f redis    # Redis logs
docker-compose logs -f db       # Database logs

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild specific service
docker-compose build web
```

### Django Management

```bash
# Run inside web container
docker-compose exec web python manage.py <command>

# Common commands
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py createsuperuser
```

## 🔍 Monitoring & Debugging

### Check Service Health

```bash
# Test Redis connection
docker-compose exec redis redis-cli ping

# Test database connection
docker-compose exec db pg_isready -U analytics_user -d analytics_db

# Test Django setup
docker-compose exec web python manage.py check
```

## 🐛 Troubleshooting

### Reset Everything

```bash
# Complete cleanup and fresh start
docker-compose down -v
docker system prune -f
docker-compose up --build
```

## 📈 Performance Tips

- Use Redis for caching frequently accessed data  
- Offload long-running or heavy operations to Celery  
- Enable Django Debug Toolbar during development  
- Monitor Redis memory usage (`redis-cli info memory`)  
- Add database indexes on columns used in frequent queries

  ## 📝 License
  This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
