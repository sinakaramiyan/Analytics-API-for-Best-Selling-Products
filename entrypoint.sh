#!/bin/sh

# Wait for database to be ready using Python
echo "Waiting for database..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if python -c "
import socket
import sys
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('db', 5432))
    sock.close()
    sys.exit(0 if result == 0 else 1)
except Exception as e:
    sys.exit(1)
"; then
        echo "Database is ready!"
        break
    else
        echo "Database not ready yet (attempt $attempt/$max_attempts)..."
        sleep 2
    fi
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    echo "Failed to connect to database after $max_attempts attempts. Continuing anyway..."
fi

# Wait for Redis
echo "Waiting for Redis..."
attempt=1

while [ $attempt -le $max_attempts ]; do
    if python -c "
import socket
import sys
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('redis', 6379))
    sock.close()
    sys.exit(0 if result == 0 else 1)
except Exception as e:
    sys.exit(1)
"; then
        echo "Redis is ready!"
        break
    else
        echo "Redis not ready yet (attempt $attempt/$max_attempts)..."
        sleep 2
    fi
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    echo "Failed to connect to Redis after $max_attempts attempts. Continuing anyway..."
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create superuser if doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
" || echo "Superuser creation failed"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "All setup complete! Starting server..."
exec "$@"