# BIU-DevSecOps16-Final-Project-Application
## Description
This repo is used for application related files as part of the final project performed at the Bar Ilan University DevSecOps course, by Stav Sabag, Adir Segev and Bar Abudi.

## Startup
To Start the database container (based on a postgres image), run the following command:
docker compose up -d

### Database Connection
The smart home sensors database is hosted and accessible at IP 192.18.145.233
Reading the database is possible by running the database-actions.py script
The script requires the username and password which should exist in a secrets folder

## BACKEND Endpoints Instructions
### READ sensors

### CREATE a new sensor
To create a new sensor send a POST request to host:5001/new-device, with a JSON payload including the following properties (empty values not permitted):
location - can be any string
type - can be either "thermostat" or "light" values
date_added - must be in YYYY-MM-DD format

Example:
{"location": "<Free form text>"",
    "type": "[thermostat | light]",
    "date_added": "2025-01-02"}

### DELETE an existing sensor
Fill sensor deletion documentation

### UPDATE an existing sensor
Fill sensor update documentation
