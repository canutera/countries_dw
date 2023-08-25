# special thanks to Gerald Gibson, most of these steps i got from his article about airflow + PostgresSQL + WSL
# link to article -> https://www.linkedin.com/pulse/airflow-postgresql-wsl-s3-gerald-gibson/

# Install ubuntu
wsl --install Ubuntu

# Ubuntu will ask to create user and password
# after setting up user, get last updates
sudo apt update && sudo apt upgrade

# Update pip
sudo apt install python3-pip

# Install Postgres 15 
sudo apt install libpq-dev

# steps below are needed to get pubkey for postgres 15
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo tee /etc/apt/trusted.gpg.d/pgdg.asc &>/dev/null
sudo apt update && sudo apt upgrade
sudo apt install postgresql postgresql-client -y
pip install psycopg2
sudo apt update && sudo apt upgrade

# Start the PostgreSQL service
sudo service postgresql start

# Go into the PostgreSQL interactive console to 
# issue setup commands
sudo -u postgres psql


# create user
CREATE USER gabriel_canuto PASSWORD 'countries_dw';

# Create the airflow metadata database and setup all permissions
CREATE DATABASE countries;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gabriel_canuto;
ALTER USER gabriel_canuto SET search_path = public;
GRANT ALL PRIVILEGES ON DATABASE countries TO gabriel_canuto;
ALTER USER gabriel_canuto CREATEDB;

# connect to countries database with user gabriel_canuto
\c countries gabriel_canuto
GRANT ALL ON SCHEMA public TO gabriel_canuto

# press Ctrl + D to exit 


