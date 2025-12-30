web: cd backend && python manage.py migrate --noinput && python manage.py seed_data || true && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
