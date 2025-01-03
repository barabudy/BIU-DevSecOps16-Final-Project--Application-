# BIU-DevSecOps16-Final-Project-Application
## Description
This repo hosts the application for the Bar-Ilan University DevSecOps course project. It was made by Stav Sabag, Adir Segev and Bar Abudi.

## Pre-requisites
Ensure a secrets folder exists with the required authentication files

## Startup
To Start the database and backend services run the following command:
docker compose up -d

### Database Connection
The smart home sensors database is hosted and accessible at IP 192.18.145.233
Connections requires a username and password (./secrets/)

## Endpoint Operations
### READ sensors
Send a GET request to host:5001/get-sensors

### CREATE new sensor
Send a POST request to host:5001/create-sensor, include JSON payload with the following properties (non-empty):
location - any string accepted
type - "thermostat" or "light" values accepted
date_added - values in format YYYY-MM-DD accepted

JSON payload Example:
{"location": "Kids Bedroom",
    "type": "thermostat",
    "date_added": "2025-01-02"}

### DELETE an existing sensor
Send a DELETE request to host:5001/delete-sensor, include JSON payload with the following properties (non-empty):
id - must be an existing sensor id

JSON payload Example:
{"id": "1008"}

### UPDATE an existing sensor
Send a PUT request to host:5001/update-sensor, include JSON payload with the properties you wish to change:
id - must be an existing sensor id
location - optional, non empty string
state - optional, "on" or "off" accepted
type - optional, "light" or "thermostat" accepted

JSON payload Example:
{
    "id":"1001"
    "location": "Basemeent",
    "state":"off",
    "type": "thermostat",}