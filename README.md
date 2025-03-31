# Development
DJANGO_ENV=development python manage.py runserver

# Staging
DJANGO_ENV=staging gunicorn config.wsgi:application

# Production
DJANGO_ENV=production gunicorn config.wsgi:application --bind 0.0.0.0:8000
