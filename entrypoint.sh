python manage.py collectstatic --no-input && gunicorn core.project.wsgi:application --bind 0.0.0.0:8000