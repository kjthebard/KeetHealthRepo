from jinja2 import Template

keet_users = Template (
"""

-- Creating Schema and Setting the Schema
CREATE SCHEMA IF NOT EXISTS {{ENV}}_{{SCHEMA}};
USE SCHEMA {{ENV}}_{{SCHEMA}};

-- Creating Database and setting the Database
CREATE DATABASE IF NOT EXISTS {{ENV}}_{{DATABASE}};
USE DATABASE {{ENV}}_{{DATABASE}};

-- Creating the table for data landing from pandas.
CREATE TABLE IF NOT EXISTS {{ENV}}_{{TABLE}} (
id varchar(20),
first_name varchar(200),
last_name varchar(200),
age integer,
gender char(8),
visit-date date
);

-- Create User to interact with the database
CREATE USER IF NOT EXISTS {{ENV}}_{{ROLE}};

-- Grant Privs on the schema, database and table. 
GRANT ALL ON SCHEMA {{ENV}}_{{SCHEMA}} TO ROLE {{ENV}}_{{ROLE}};
GRANT ALL ON DATABASE {{ENV}}_{{DATABASE}} TO ROLE {{ENV}}_{{ROLE}};
GRANT ALL ON TABLE {{ENV}}_{{TABLE}} TO ROLE {{ENV}}_{{ROLE}};

""")