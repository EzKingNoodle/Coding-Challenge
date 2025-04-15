# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 5000 for Flask
EXPOSE 5000

# Run Gunicorn with Flask application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"] 