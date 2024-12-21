# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the application code and requirements.txt into the container
COPY . /app

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run your application
CMD ["gunicorn", "-w", "4", "-b", "127.0.0.1:5000", "app:pairing_service"]