from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime # Used for date and time validation for sensors
import logging

logging.basicConfig(level=logging.ERROR)

from dotenv import load_dotenv
load_dotenv()

from os import getenv
# Oracle VM2 IP
# DB_HOST_ADDRESS = "192.18.145.233"
DB_HOST_ADDRESS = getenv("POSTGRES_USER")



DB_USER_FILE = "secrets/postgres_user"
DB_PASSWORD_FILE = "secrets/postgres_password"
DB_NAME = "smart-home-db"
DB_TABLE = "smart_sensors"

# Read secrets files securely
def read_secret(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# initialize Database credentials
DB_USER = read_secret(DB_USER_FILE)
DB_PASS = read_secret(DB_PASSWORD_FILE)
CONNECTION_STRING = "postgresql://{0}:{1}@{2}:5432/{3}".format(DB_USER, DB_PASS, DB_HOST_ADDRESS, DB_NAME)

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

# Routes
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Smart Home Control Panel API!"})

@app.route('/sensors', methods=['GET'])
def get_devices():
    app.logger.debug("GET / sensors called")
    Sensors = Sensor.query.all()
    return jsonify([sensor.to_dict() for sensor in Sensors])


@app.route('/new-device', methods=['POST'])
def create_sensor():
    data = request.json  # Expect JSON payload
    location = data.get('location')
    type = data.get('type')
    state = "off"  # Default state
    date_added = data.get('date_added')

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
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Attempt adding new sensor to the database
    try:
        db.session.add(new_sensor)
        db.session.commit()
        return jsonify({"message": "Sensor added successfully", "sensor": new_sensor.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding sensor: {e}")
        return jsonify({"error": "Internal server error"}), 500
    

# @app.route('/devices/<int:device_id>', methods=['PUT'])
# def update_device(device_id):
#     device = Device.query.get_or_404(device_id)
#     data = request.json
#     if 'name' in data:
#         device.name = data['name']
#     if 'status' in data:
#         device.status = data['status']
#     db.session.commit()
#     return jsonify(device.to_dict())

# @app.route('/devices/<int:device_id>', methods=['DELETE'])
# def delete_device(device_id):
#     device = Device.query.get_or_404(device_id)
#     db.session.delete(device)
#     db.session.commit()
#     return jsonify({"message": "Device deleted successfully"})

# Main Entry
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
