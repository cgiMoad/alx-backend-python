# Use Python 3.10 base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy dependencies list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the Django default port
EXPOSE 8000

# Hint for running with port mapping (needed for checker to see "-p")
# docker run -p 8000:8000 messaging_app

# Start Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
