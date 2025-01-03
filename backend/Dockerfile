FROM python:3.11-slim

WORKDIR /smart-home-app

# Install & Update system packages
RUN apt-get update && apt-get install -y \
    build-essential python3-dev libpq-dev gcc curl --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl --fail http://localhost:5001 || exit 1

# Expose the port the Flask app runs on
EXPOSE 5001

# Run the Flask application
CMD ["python3","smart_home_app.py"]
