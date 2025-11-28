# Use official lightweight Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Collect static files (optional for now)
# REMOVE THIS LINE - static handled differently on Cloud Run

# Expose port 8080 (Cloud Run expects this)
EXPOSE 8080

# Start server
CMD gunicorn Udyog.wsgi:application --bind 0.0.0.0:8080