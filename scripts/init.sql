-- init.sql

-- Create an inital "employees" table
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,    -- Auto-incrementing ID field
    name VARCHAR(100) NOT NULL,  -- Name of the employee
    job_title VARCHAR(100)     -- Job title of the employee
);

-- Insert some sample data into the "employees" table
INSERT INTO employees (name, job_title) VALUES
    ('Bar Abudi', 'DevOps Engineer'),
    ('Adir Segev', 'IT technician'),
    ('Stab Sabag', 'Bank Integrator');
