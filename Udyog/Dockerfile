# Use official lightweight Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Install system dependencies (required for psycopg2)
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# 🔥 Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8080

# Run server
CMD ["gunicorn", "Udyog.wsgi:application", "--bind", "0.0.0.0:8080"]
