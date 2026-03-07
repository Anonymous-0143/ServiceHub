FROM python:3.11-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies from the nested servicehub directory
COPY servicehub/requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY servicehub/ /code/

# Create a directory for sqlite database volume
RUN mkdir -p /data

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start daphne/uvicorn for handling WebSockets and HTTP
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "servicehub.asgi:application"]
