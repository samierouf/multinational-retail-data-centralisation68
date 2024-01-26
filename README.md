# Multination Retail Data Centralisation

The aim of this project is to gather extract and clean data from multiple sources and centralise them in one local database to allow for easier access and querrying. This project is to develop skils in datat extarction, datat cleaning and querrying databases.

## Prerequisite
AWS account
Python 3.11 
pytnon packages: 'psycoopg2', 'sqlalchemy', 'pandas', 'numpy', 'tabula', 'pandasgui', 'requests', 'boto3', 're'
Java 8
Download versions from the 'requierments.txt' file
SQL
postgresql
pgAdmin 4 or other suitable alterntive. (create a empty database called 'sales_data' this is thename of the datatbase on your local computer that you are going to upload the database to.
YAML files containg the information about the datatbase you are going to upload to as well as download from called 'pgadmin_creds.yaml' and 'db_cred.yaml' respectively.

## Instalation
```bash
pip install -r requirments.txt
```

## Clonening the repo
using the folwing clone the repo
```bash
git clone https://github.com/samierouf/multinational-retail-data-centralisation68.git
```

## Usage
To run this code or to recreate something similare you will need the all of the prerequisites. Once you have evrything dowlonaded/installed you can createn an environment and local reposity and clone the repo. Once the repo has been installed you can run the main.py file which will automatically extract clean and upload the data from the variuos sorces and upload to the sales_data databse you created on your localhost.

##


