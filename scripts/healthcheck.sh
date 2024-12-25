#!/bin/sh

# Read the username from the secrets file
POSTGRES_USER=$(cat /run/secrets/postgres_user)

# Run the health check
exec pg_isready -U "$POSTGRES_USER"
