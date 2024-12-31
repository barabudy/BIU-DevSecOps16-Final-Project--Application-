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