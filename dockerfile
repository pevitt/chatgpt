# Base image
FROM python:3.9-slim-buster

# Set work directory
WORKDIR /app

# Intall required dependencias
# Install required dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    libcurl4-openssl-dev \
    netcat \
&& rm -rf /var/lib/apt/lists/*


# Copy requirements file
COPY requirements.txt .

# Install requirements
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app will be served on
EXPOSE 8000

# Start the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "adviserapi.wsgi:application"]