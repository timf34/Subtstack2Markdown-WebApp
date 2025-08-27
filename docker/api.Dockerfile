FROM python:3.11-slim
WORKDIR /code
COPY . /code
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install --with-deps chromium
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
