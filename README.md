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

## Project format
'database_utils.py'
'data_extraction.py'
'data_cleaning.py'
'SQL_code' file 

## Project information
### data_utils.py
contains the code that is used to connet to the databases.
### data_extraction.py
contains the code that is used to extract the data from its different locations

### data_cleaning.py 
contains the code that is used to clean and process the data after extraction.

### SQL_code
contains the code for devloping the star based schemea and the code for queerying the datat to find specific information.

## Project steps
this projects can be broken down into 4 key milestone.

### Milestone 1
This milestone is all about setting up the python environment, the sales_data  database , creating the YAMAL  files that are going to hold the credentials for uploading and dowloading databases and having an accese to AWS CLI vi access keys for an IamUser account.

### Milestone 2
#### Data extraction
In this milestone we are goint to extract the data from their various sources, clean the data as well as upload them to the loca sales_data daabase that was created in milestone 1. the datat will be extracted from multiple diffrent sorces. the order table datat is stored in a daabase on AWS RDS and will be uploaded to the localhost wiht the names `orders_table`.  The user data is also stored in the same location as the order table datat so we can reuse the same method to extract it and will be uploaded to the `sales_data` database under the name `dim_users`. hte card datat is located in a pdf doccument inside an AWS S3 bucket after extracting we will upload it with the name `dim_card_details`. The store data is stored on an APi after extraction it will be uploaded to the under the name `dim_store_details`. the product details data is located in CSV on an AWS S3 bucket and be called `dim_product` when it is uploaded. The dates data is stored as a JSON file on S£ after extracting it we will call it `dim_date_times` when we upload it to the loacal database `sales_data`.

#### Data cleaning
After extracting the data from the various sources they were then uploaded to the sales_data database. The orders_table is the most important table as it acts as the single source of truth it will also be the table that all other tables serve as such it is imports to ensure the datat in the other table match the data in the `orders_table`. As such we can see what the length of the other tables can be from the orders table as well as the information that they must conaint as we will later make forign keys for the order_table later in milestone 3. this can be done using 
```sql
SELECT DISTINCT COUNT(date_uuid)
FROM orders_table
```
