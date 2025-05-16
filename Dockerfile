# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY main.py .
COPY bodyfat.pkl .
COPY Templates ./Templates

# Expose Flask port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "main.py"]
