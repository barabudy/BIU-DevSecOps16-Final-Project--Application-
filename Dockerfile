FROM python:3.11-slim

WORKDIR /smart-home-app

COPY . .

# Install system dependencies (e.g., for psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir -r requierments.txt

# Expose the port the Flask app runs on
EXPOSE 5050

# Set environment variables for Flask
ENV FLASK_APP=smart_home_app.py
ENV FLASK_ENV=development

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5050"]
