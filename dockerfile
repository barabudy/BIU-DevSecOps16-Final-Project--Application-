FROM postgres:17.2-alpine3.20

ARG POSTGRES_USER = "devsecops16"
ARG POSTGRES_PASSWORD = "devsecops16"
ARG POSTGRES_DB = "smart-home-db"

# Expose PostgreSQL default port
EXPOSE 5432:5432