FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy only requirements first (for better layer caching)
ARG REQUIREMENTS=requirements.txt
COPY ${REQUIREMENTS} .

# Install dependencies
RUN pip install --no-cache-dir -r ${REQUIREMENTS}

# Copy the rest of the application
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Default command (overridden in docker-compose if needed)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
