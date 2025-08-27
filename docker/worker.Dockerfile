FROM python:3.11-slim
WORKDIR /code
COPY . /code
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install --with-deps chromium
CMD ["celery", "-A", "app.workers.tasks.celery_app", "worker", "--loglevel=info"]
