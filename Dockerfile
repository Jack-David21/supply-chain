FROM python:3.11-slim

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
# We do this before copying the rest of the app to take advantage of Docker cache
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

# Copy the necessary project directories
COPY api/ ./api/
COPY frontend/ ./frontend/
COPY models/ ./models/

# Create the data directory (this will be used as a mount point for the volume)
RUN mkdir -p ./data

# Expose the API port
EXPOSE 8000

# Command to run the FastAPI server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]