# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create and activate a virtual environment, then install dependencies
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Set environment variables
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
ENV PORT=8080
ENV GEMINI_API_KEY="AIzaSyDgJ_0xf87nMi-OYpIqo9BA9EZrsYCrlGo"

# Run the application
CMD ["sh", "-c", ". venv/bin/activate && flask run"]