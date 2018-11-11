# Migrate
python manage.py makemigrations
python manage.py migrate

# Start gunicorn
gunicorn api.wsgi -b=unix:/socket/app.sock

