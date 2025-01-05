from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import generate_latest, Counter
from flask_cors import CORS
from datetime import datetime # Used for date and time validation for sensors
from dotenv import load_dotenv
import logging
import os
# Test CI pipeline #2

logging.basicConfig(level=logging.ERROR)

# Oracle VM2 IP
DB_HOST_ADDRESS = "192.18.145.233"
DB_NAME = "smart-home-db"
DB_TABLE = "smart_sensors"

# initialize Database credentials via .env file
load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

if not DB_USER or not DB_PASS:
    raise EnvironmentError("DB_USER or DB_PASS environment variables are not set")

CONNECTION_STRING = "postgresql://{0}:{1}@{2}:5432/{3}".format(DB_USER, DB_PASS, DB_HOST_ADDRESS, DB_NAME)
HTTP_REQUESTS=Counter('HTTP_requests_Total', 'Total HTTP request amount', ['endpoint','method', 'code'])

# Flask App Configuration
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECTION_STRING
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# Models
class Sensor(db.Model):
    __tablename__ = DB_TABLE

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(10), nullable=False, default="off")
    date_added = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "location": self.location,
            "type": self.type,
            "state": self.state,
            "date_added": self.date_added.isoformat()
        }

@app.get('/metrics')
def metrics():
    return generate_latest()

# Routes
@app.route('/')
def home():
    HTTP_REQUESTS.labels(endpoint='/metrics', method='get', code='200').inc(1)
    return jsonify({"message": "Welcome to the Smart Home Control Panel API!"})

@app.route('/get-sensors', methods=['GET'])
def get_devices():
    HTTP_REQUESTS.labels(endpoint='/metrics', method='get', code='200').inc(1)
    app.logger.debug("GET / get-sensors called")
    Sensors = Sensor.query.all()
    return jsonify([sensor.to_dict() for sensor in Sensors])


@app.route('/create-sensor', methods=['POST'])
def create_sensor():
    HTTP_REQUESTS.labels(endpoint='/metrics', method='get', code='200').inc(1)
    data = request.json  # Sensor data in JSON payload
    location = data.get('location')
    type = data.get('type')
    state = "off"  # Default state
    date_added = data.get('date_added', datetime.now().strftime('%Y-%m-%d'))

    # Validate new sensor properties
    if not location or not type or not date_added:
        return jsonify({"error": "Missing required parameters"}), 400

    if type not in ['light', 'thermostat']:
        return jsonify({"error": "Invalid type values. Only 'light' and 'thermostat' sensors currently supported."}), 400

    # Create new sensor object
    new_sensor = Sensor(location=location, type=type, state=state, date_added=date_added)

    # Date validation
    try:
        datetime.strptime(date_added, '%Y-%m-%d')
    except ValueError:
        logging.error(f"Error occurred in {request.path}: {e}")
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Attempt adding new sensor to the database
    try:
        db.session.add(new_sensor)
        db.session.commit()
        return jsonify({"message": "Sensor added successfully", "sensor": new_sensor.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error occurred in {request.path}: {e}")
        return jsonify({"error": "Internal server error"}), 500
    

@app.route('/update-sensor', methods=['PUT'])
def update_sensor():
# Get sensor ID from request JSON
    HTTP_REQUESTS.labels(endpoint='/metrics', method='get', code='200').inc(1)
    data  = request.json
    sensor_id = data.get('id')
    location = data.get('location')
    type = data.get('type')
    state = data.get('state')
    # date_added = data.get('date_added')

    if not sensor_id:
        return jsonify({"error": "Sensor ID is required"}), 400
    
    try:
        # Query the database for the sensor by ID
        sensor = db.session.get(Sensor, sensor_id)

        if not sensor:
            return jsonify({"error": f"Sensor with ID {sensor_id} does not exist"}), 404
        
        # Update properties if they were provided with valid values
        if location:
            sensor.location = location
        if type:
            if type not in ['light', 'thermostat']:
                return jsonify({"error": "Invalid type values. Only 'light' and 'thermostat' sensors currently supported."}), 400
            sensor.type = type
        if state:
            if state not in ['on', 'off']:
                return jsonify({"error": "Invalid state values. Only 'on' and 'off' sensors states are currently supported."}), 400
            sensor.state = state

        db.session.commit()
        return jsonify({"message": f"Sensor with ID {sensor_id} updated successfully", "sensor": sensor.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error occurred in {request.path}: {e}")
        return jsonify({"error": str(e)}), 500

# Attempt sensor deletion by ID, if it exists
@app.route('/delete-sensor', methods=['DELETE'])
def delete_sensor():
    HTTP_REQUESTS.labels(endpoint='/metrics', method='get', code='200').inc(1)
    # Get sensor ID from request JSON
    data  = request.json
    sensor_id = data.get('id')

    # Validate sensor ID exist
    if not sensor_id:
        return jsonify({"error": "Missing sensor ID"}), 400
    
    try:
        # Query the database for the sensor
        sensor = db.session.get(Sensor, sensor_id)

        # Check if the sensor exists
        if not sensor:
            return jsonify({"error": f"Sensor with ID {sensor_id} does not exist"}), 404

        db.session.delete(sensor)
        db.session.commit()
        return jsonify({"message": f"Sensor with ID {sensor_id} deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error occurred in {request.path}: {e}")
        return jsonify({"error": str(e)}), 500

# Main Entry
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
