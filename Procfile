web: gunicorn --timeout 200 core.wsgi
worker: celery -A core worker --loglevel=info