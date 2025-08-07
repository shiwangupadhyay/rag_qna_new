# Dockerfile

# 1. Use an official, slim Python base image
# Using a specific version is better for production stability
FROM python:3.11-slim

# 2. Set environment variables
# Prevents Python from buffering stdout and stderr, making logs appear in real-time
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy and install dependencies first
# This leverages Docker's layer caching. The pip install step will only re-run
# if you change your requirements.txt file, making subsequent builds much faster.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container
# This includes your app.py, utils/, src/, etc.
COPY . .

# 6. Expose the port the app will run on
# The container will listen on port 80
EXPOSE 80

# 7. Define the command to run your application
# Tells uvicorn to run the 'app' instance from the 'app.py' module.
# --host 0.0.0.0 makes the app accessible from outside the container.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]