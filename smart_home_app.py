from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Flask App Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://devsecops16:devsecops16d@db:5432/smart-home-db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# Models
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="off")
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "last_updated": self.last_updated.isoformat()
        }

# Routes
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Smart Home Control Panel API!"})

@app.route('/devices', methods=['GET'])
def get_devices():
    devices = Device.query.all()
    return jsonify([device.to_dict() for device in devices])

@app.route('/devices', methods=['POST'])
def add_device():
    data = request.json
    new_device = Device(name=data['name'], status=data.get('status', 'off'))
    db.session.add(new_device)
    db.session.commit()
    return jsonify(new_device.to_dict()), 201

@app.route('/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = Device.query.get_or_404(device_id)
    data = request.json
    if 'name' in data:
        device.name = data['name']
    if 'status' in data:
        device.status = data['status']
    device.last_updated = datetime.utcnow()
    db.session.commit()
    return jsonify(device.to_dict())

@app.route('/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = Device.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    return jsonify({"message": "Device deleted successfully"})

# Main Entry
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
