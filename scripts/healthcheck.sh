#!/bin/sh

# Read username & database name from the secrets file
POSTGRES_USER=$(cat /run/secrets/postgres_user)
DATABASE_NAME=${POSTGRES_DB:-smart-home-db}  # Default to "smart-home-db" if not set

# Run the health check
exec pg_isready -U "$POSTGRES_USER" -d "$DATABASE_NAME"
