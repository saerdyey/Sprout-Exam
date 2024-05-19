# Use a slim Python 3 image
FROM python:3.10.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Copy your app code
COPY . .

# Expose port for FastAPI (default 8000)
EXPOSE 8000

# Set environment variable for database connection (replace with your details)
ENV PGDB_HOST="localhost"
ENV PGDB_USERNAME="postgres"
ENV PGDB_PASSWORD="password123"
ENV PGDB_NAME="sprout_exam"
ENV PGDB_PORT="5432"


# Run uvicorn server (entrypoint for FastAPI)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]