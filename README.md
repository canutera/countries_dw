

<!-- 
<details>
  <summary><strong>English</strong></summary><br /> -->

# Welcome to **countries_dw**

- [Welcome to **countries\_dw**](#welcome-to-countries_dw)
    - [Description](#description)
    - [How to use](#how-to-use)
    - [Setting a PostgreSQL database in a WSL environment](#setting-a-postgresql-database-in-a-wsl-environment)
    - [Deploy dbt project in Postgres Database](#deploy-dbt-project-in-postgres-database)
    - [Next steps](#next-steps)

### Description
This project consumes [REST Countries](https://restcountries.com/) API and parses its data into dataframes. 
There are several informations available and it was chosen for being open source to practice data engineering techniques. 

Data from all countries are recieved as a list of dictionaries in a json response. 

[Country class](src\parser\country.py) is responsible for parsing and assembling tables for
each country contained in the response.

[CountriesHook](src\hook\countries_hook.py) makes a GET request at [All countries endpoint](https://restcountries.com/v3.1/all)
and save a json file with information. Then parses and concatenates information from every country to save all tables at the [data folder](data). This project uses Pandas for manipulating data, so all pandas files formats are supported.


### How to use

To start using this repository, create a project folder, open a terminal and Git Clone using the [countries_dw url](https://github.com/canutera/countries_dw.git).
```bash
git clone https://github.com/canutera/countries_dw.git
```
This project uses [Poetry](https://python-poetry.org/) to manage its dependencies. 
To use Poetry, make sure you have this python package installed. If you don't, run the following command:
```bash
pip install poetry
```
Then run:
```bash
# add commented line to create venv inside the project folder
# poetry config virtualenvs.in-project true
poetry install
```
To install the project dependencies inside the current folder. After installing run:
```bash
poetry shell
activate
```
Your brand new virtual envinroment should be setup and ready to use after these steps.

The example below, shows a simple usage for countries_dw project which can be found in [main.py](src\main.py) file:
```python
from src.countries_hook import CountriesHook
file_format = 'csv'
hook = (CountriesHook()
            .parse_countries()
            .parse_tables()
            .save_tables(file_format, index=False)
        )
```
If you run the following code in a Jupyter Notebook, make sure you are connected to the created virtual environment for this project.
After running the code above, all tables should appear in the data folder. Just make sure, a valid format was passed.
You can check [pandas.DataFrame Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) to look for valid formats.

### Setting a PostgreSQL database in a WSL environment

I chose to set up PostgreSQL database on WSL, because I intend to orchestrate this whole project using Apache Airflow but still do not fully understand how to make it using docker. And
because Airflow only works in a Linux environment, I ended up learning to set up in a WSL due to not having access to a Docker License in my work. (This might a good option if you are in the same situation).

> A docker implementation will be later added to this repository.

To install WSL Distro in your machine, open a PowerShell terminal and type:
```shell
WSL --install Ubuntu
```
You can choose any distro, in this case I chose Ubuntu.
This may take some minutes, an after installing, you will be asked to create a user with a password.

After setting user, run these commands below:

```bash
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
```
If all commands were run correctly, after this you should be in the Postgres terminal in Ubuntu. Run the following commands:
```SQL
--create user
CREATE USER gabriel_canuto PASSWORD 'countries_dw';

--Create the countries metadata database and setup all permissions
CREATE DATABASE countries;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gabriel_canuto;
ALTER USER gabriel_canuto SET search_path = public;
GRANT ALL PRIVILEGES ON DATABASE countries TO gabriel_canuto;
ALTER USER gabriel_canuto CREATEDB;

--connect to countries database
\c countries;
GRANT ALL ON SCHEMA public TO gabriel_canuto;
```
> You might want to customize user and password.

Your Postgres database is now set up in WSL.

### Deploy dbt project in Postgres Database

If you used Poetry to manage dependecies, dbt-core and dbt-postgres (which is our adapter) should be already installed. Also the model is already created and ready run in [dbt folder](src\dbt). But first, we need to set up the dbt profile for this project in your machine.

> The profiles.yml file can be found at:
>  
> C:\Users\\<your_username>\\\.dbt\profiles.yml

Copy and paste the code below to set this profile to work in dbt


```yml
countries_dw:
  outputs:

    postgres:
      type: postgres
      threads: 2
      host: 127.0.0.1
      port: 5432
      user: gabriel_canuto
      pass: countries_dw
      dbname: countries
      schema: public

  target: postgres
```
> **If you customized your user and password in Postgres**, please change the info before saving the files in order to work properly.

To use the created model make sure your terminal is inside the src/dbt folder. If not, type: 

```shell
cd src/dbt
```
Inside the dbt folder, run:

```shell
dbt debug
```
To check if the profile is set up correctly. If something goes wrong, you might want to: 
 -  make sure you are inside src/dbt folder
 -  make sure database is running and accepting connections
 -  check your profiles.yml file again 

If all checks passed, just run:

```shell
dbt seed
dbt run
```
To deploy this project to your database.

To check out the project documentation, please run:

```shell
dbt docs generate
dbt docs serve
```

A webserver on localhost:8080 will open in your browser.


<details>
  <summary><strong> Information on how this project was built</strong></summary><br />

  Data from countries api was parsed to csv files and saved in [dbt seed folder](src\dbt\seeds).

  > Note:
  > According to [dbt seed docs](https://docs.getdbt.com/docs/build/seeds) this is a poor use of this feature. Seed is meant to keep track
  > of relevant data using version control. But for the sake of simplicity and also because our data is small (less than 1MB), this feature was used to load data to the warehouse. 
  > 
  > Seed information is hidden from docs and is declared as a source in the raw schema. 

The following code was run in the project environment to save csvs in the [dbt seed folder](src\dbt\seeds).

```python
from src.hook.countries_hook import CountriesHook
file_format = 'csv'
hook = (CountriesHook()
            .parse_countries()
            .parse_tables()
            .save_tables(file_format, destination='C:\Git\countries_dw\src\dbt\seeds', index=False)
      )
```
Then in seed folder, a [properties.yml file](src\dbt\seeds\properties.yml) was configured to load data and omitit seeds from documetation using the format below:

```yml
version: 2

seeds:
  - name: table
    config:
      enabled: true
      docs:
        show: false
      database: countries
      schema: raw
      column_types: 
        col1: int
        col2: varchar(255)
      
```
Seeded files were declared as source in the [model schema](src\dbt\models\staging\schema.yml) along with models for the staging schema including constraints.

</details>







### Next steps

- [x] Set up a WSL 
- [x] Set up a PostgreSQL database to store table
- [x] Create data model and documentation
- [ ] Finish model creation and docs
- [ ] Start data visualization for countries_dw














<h1 align="center">Hi 👋, I'm Gabriel Canuto</h1>
<h3 align="center">Another curious person on a data journey</h3>

<h3 align="left">Connect with me:</h3>
<p align="left">
<a href="https://linkedin.com/in/gabriel-canuto0" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="gabriel-canuto0" height="30" width="40" /></a>
<a href="https://instagram.com/gabriel_canuto" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="gabriel_canuto" height="30" width="40" /></a>
</p>

<h3 align="left">Languages and Tools:</h3>
<p align="left"> <a href="https://pandas.pydata.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg" alt="pandas" width="40" height="40"/> </a> <a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> </p>

