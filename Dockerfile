# Use an official Python runtime as a parent image
FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        curl && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code
COPY src /app/src

ENV APP_PORT 8086

# Define a health check
HEALTHCHECK --interval=2m --timeout=5s \
    CMD healthchecker --host=localhost --port=$APP_PORT --path="/utils/health.py" --function=healthcheck

# Set up the proxy environment variables
ENV USE_PROXY false

EXPOSE $APP_PORT

# Run main.py when the container launches
CMD ["python", "src/main.py"]
