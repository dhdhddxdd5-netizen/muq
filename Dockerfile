FROM python:3.12-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    DJANGO_SETTINGS_MODULE=dalal_project.settings

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy ALL application code
COPY . .

# Verify the dalal_project module exists and is importable
RUN echo "=== Verifying dalal_project module ===" && \
    ls -la /app/dalal_project/ && \
    echo "✓ dalal_project directory exists" && \
    python -c "import dalal_project; print('✓ dalal_project imported successfully')" && \
    python -c "from dalal_project import wsgi; print('✓ dalal_project.wsgi imported successfully')" && \
    python -c "import django; django.setup(); from dalal_project import urls; print('✓ dalal_project.urls imported successfully')" && \
    echo "=== All modules verified ===" || exit 1

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "run_server.py"]

