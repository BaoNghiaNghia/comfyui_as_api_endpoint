# Step 1: Use an official Python runtime as a base image
FROM python:3.12-slim

# Step 2: Set environment variables for better container behavior
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Step 3: Set the working directory in the container
WORKDIR /app

# Step 4: Copy the requirements file first to leverage Docker cache
COPY requirements.txt /app/

# Step 5: Install any required packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the remaining application code into the container
COPY . /app

# Step 7: Ensure the app directory has the correct permissions
RUN chmod -R 755 /app

# Step 8: Expose the port FastAPI will run on
EXPOSE 8000

# Step 9: Run FastAPI using Uvicorn with the correct path for the entry point
# If backend/main.py exists, adjust the path to match. Otherwise, use the appropriate entry point.
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
