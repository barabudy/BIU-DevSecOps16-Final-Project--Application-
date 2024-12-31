-- init.sql

-- Create the initial sensors table
CREATE TABLE smart_sensors (
    sensor_id SERIAL PRIMARY KEY,
    sensor_location VARCHAR(100) NOT NULL,
    sensor_type VARCHAR(20) NOT NULL CHECK (sensor_type IN ('light', 'thermostat')),
    sensor_state VARCHAR(10) NOT NULL CHECK (sensor_state IN ('on', 'off')),
    date_added DATE NOT NULL DEFAULT CURRENT_DATE);

-- Set a starting value for sensor_id of 1000
ALTER SEQUENCE smart_sensors_sensor_id_seq RESTART WITH 1000;

-- Insert sample entries
INSERT INTO smart_sensors (sensor_location, sensor_type, sensor_state, date_added) VALUES
('living room', 'light', 'on', '2024-12-25'),
('kids bedroom', 'thermostat', 'off', '2024-12-26'),
('bedroom-upstairs', 'light', 'on', '2024-12-27'),
('kitchen', 'thermostat', 'off', CURRENT_DATE);
