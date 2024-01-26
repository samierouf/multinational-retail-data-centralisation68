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
After extracting the data from the various sources they were then uploaded to the sales_data database. The orders_table is the most important table as it acts as the single source of truth it will also be the table that all other tables serve as such it is imports to ensure the datat in the other table match the data in the `orders_table`. As such we can see what the length of the other tables can be from the orders table as well as the information that they must conaint as we will later make forign keys for the order_table later in milestone 3. this can be done using :
```sql
SELECT COUNT(DISTINCT(card_number))
FROM orders_table
```
replacing card_number with the corresponding forieng key of the table that you want to examine.
`dim_card_details` - card_number
`dim_date_times` - date_uuid
`dim_products` - product_code
`dim_store_detail` - store_code
`dim_users` - user_uuid
So from this we can see that there is 15284 pieces of unique data in the card_number column of the orders_table so the dim_card_details table must also be 120123 in size but the dim_card_details table size is 15309 which tells us that there is 25 pieces of invalid data that we have to remove from the dim_card_details column. The invalid data that need to be cleaned can be viewed using:
```sql
SELECT DISTINCT card_number
FROM dim_card_details
WHERE card_number NOT IN (select card_number FROM orders_table
```
From this it can be seen that many of the card numbers have '?' in them so I remove using 
```python
pdf_data['card_number'] = pdf_data['card_number'].astype(str).str.replace(r'\?','', regex = True)
```
located in the `clean_card_data()` function which can be found in the `DataCleaning` class inside the `data_cleaning.py` file. we the rerun the previous sql queery to see if there is any that has been missed.

this cleaning is repeated for evrey table to make the data more uniform and be able to matches the orders_table it is during the cleaning where we drop columns and make sure that the datat are in the ocreect format.One thing to look out for is any column that is related to dates as they can cause issues if they are not in the right format. I found that it SQL was much better at finding these irregular dates than python the SQL code i used to find them was:
```sql
SELECT *
FROM dim_card_details
WHERE NOT (dat_payment_confirmed is NULL OR date_payment_confirmed ~ '^\d{4}-\d{2}-\d{2}$';
```
here we can see that a number of the dates are not in the correct form and if python ```python pd.to_datetime()``` function was used they would come up as errors. so before we use the ```python pd.to_datetime()``` function to make the column into the right format they must be corrected which i have done by making a function called `correct_payment_dates()` in the `data_cleaning.py` file. in this function i created a dictionary to with the incorrectly formatted dates to their corrected form then mapped them over the date_payment_confirmed column of the card dataset to correct them. then used ```pd.to_datetime()``` to make the column to the right type and then the cleaned and processsed data is uploaded to sales_data database. This process is repeated for all tables.

### Milestone 3
In this milestone we will be making a star-based schema for the database as well as make sure the columns are the correct datat types. building a star-based schema where the orders_table as the central table will allow for easier understandability as well as making it easier to preforme querries. this milestone can 9 parts:

- #### Part 1 `ms3_task1.sql`
  catsed the columns of the orders_table toithe correct datatype.
- #### Part 2 `ms3_task2.sql`
  cast he columns of dim_users_table to the correct data type.
- #### Part 3 `ms3_task3.sql`
  merged the two 'lattitude' columns into one and caste the columns to the correct datatype for dim_store_details.
- #### Part 4 `ms3_task4.sql`
  added a column called ' weight_range' which will tell delivery team if the product is light, mid_size, heavy or truck_required so they can make quick informeddecisions. removed the £ from the data in the product_price column.
- #### Part 5 `ms3_task5.sql`
  cast the columns to the corrrect datatype in the dim_product table
- #### Part 6 `ms3_task6.sql`
  updated the dim_date_time table with the correct data type
- #### Part 7 `ms3_task7.sql`
  pdated the dim_card_details table to the coreect datatypes
- #### Part 8 `ms3_task8.sql`
  creating primary keys for the other tables
- #### Part 9 `ms3_task9.sql`
  creating foreign keys in the order_table

### Milestone 4
in this milestone we will be querying the data.

- #### How many stores does the business have and in which countries are they located in?
  
- #### Which location currently have the most stores? 'ms4_task1.sql`
- #### Which months produced thelargest amount of sales? 'ms4_task2.sql`
- #### Which country produced the larges amount of sales? 'ms4_task3.sql`
- #### How many sales are coming from online? 'ms4_task4.sql`
- #### What percentage of slaes come through each store type? 'ms4_task5.sql`
- #### Whoch month in each year produced the highestcost of sales? 'ms4_task6.sql`
- #### What is our staff head count? 'ms4_task7.sql`
- #### Which german store type is selling the most? 'ms4_task8.sql`
- #### How quickly is the company making sales? 'ms4_task9.sql`







 




