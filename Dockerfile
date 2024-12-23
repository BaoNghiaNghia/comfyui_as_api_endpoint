# Step 1: Use an official Python runtime as a base image
FROM python:3.9-slim

# Step 2: Set environment variables for optimal container behavior
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH"

# Step 3: Set the working directory in the container
WORKDIR /app

# Step 4: Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Copy the requirements file first to leverage Docker's caching mechanism
COPY requirements.txt .

# Step 6: Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Step 7: Copy the application code into the container
COPY . .

# Step 8: Ensure the application directory has proper permissions
RUN chmod -R 755 /app

# Step 9: Expose the port FastAPI will run on
EXPOSE 8000

# Step 10: Set the default command to run FastAPI
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
