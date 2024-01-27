# Multinational Retail Data Centralization

The goal of this project is to extract, clean, and centralize data from multiple sources in one local database for easier access and querying. This project aims to develop skills in data extraction, data cleaning, and database querying.

## Prerequisites
- AWS account
- Python 3.11
  - Packages: 'psycopg2', 'sqlalchemy', 'pandas', 'numpy', 'tabula', 'pandasgui', 'requests', 'boto3', 're'
- Java 8
- Download versions from the 'requirements.txt' file
- SQL, PostgreSQL
- pgAdmin 4 or other suitable alternatives (create an empty database called 'sales_data')
- YAML files containing information about the databases: 'pgadmin_creds.yaml' and 'db_cred.yaml'

## Installation
```bash
pip install -r requirements.txt
```

## Clonening the repo
using the folwing clone the repo
```bash
git clone https://github.com/samierouf/multinational-retail-data-centralisation68.git
```

## Usage
To run this code or recreate something similar, install the prerequisites. Once everything is downloaded/installed, create an environment, a local repository, and clone the repo. Run the main.py file to automatically extract, clean, and upload data from various sources to the sales_data database on your localhost.

## Project format
- 'database_utils.py'
- 'data_extraction.py'
- 'data_cleaning.py'
- 'SQL_code' file 

## Project information
### data_utils.py
Contains code used to connect to databases.
### data_extraction.py
Contains code for extracting data from different locations.
### data_cleaning.py 
Contains code for cleaning and processing data after extraction.
### SQL_code
Contains code for developing the star-based schema and querying data to find specific information.
## Project steps
This project can be broken down into 4 key milestones.
### Milestone 1
This milestone is all about setting up the python environment, the sales_data  database , creating the YAMAL  files that are going to hold the credentials for uploading and dowloading databases and having an accese to AWS CLI vi access keys for an IamUser account.

### Milestone 2
#### Data extraction
In this milestone we are going to extract the data from their various sources, clean the data as well as upload them to the local sales_data database that was created in milestone 1. the data will be extracted from multiple different sources. the order table data is stored in a database on AWS RDS and will be uploaded to the localhost with the names `orders_table`.  The user data is also stored in the same location as the order table datat so we can reuse the same method to extract it and will be uploaded to the `sales_data` database under the name `dim_users`. the card data is located in a pdf doccument inside an AWS S3 bucket after extracting we will upload it with the name `dim_card_details`. The store data is stored on an API after extraction it will be uploaded to the under the name `dim_store_details`. the product details data is in a CSV on an AWS S3 bucket and be called `dim_product` when it is uploaded. The dates data is stored as a JSON file on S£ after extracting it we will call it `dim_date_times` when we upload it to the local database `sales_data`.

#### Data cleaning
After extracting the data from the various sources they were then uploaded to the sales_data database. The orders_table is the most important table as it acts as the single source of truth it will also be the table that all other tables serve as such it is imports to ensure the data in the other table match the data in the `orders_table`. As such we can see what the length of the other tables can be from the orders table as well as the information that they must contain as we will later make foreign keys for the order_table later in milestone 3. this can be done using :  

```sql
SELECT COUNT(DISTINCT(card_number))
FROM orders_table
```
replacing card_number with the corresponding foreign key of the table that you want to examine.
`dim_card_details` - card_number
`dim_date_times` - date_uuid
`dim_products` - product_code
`dim_store_detail` - store_code
`dim_users` - user_uuid
So from this we can see that there is 15284 pieces of unique data in the card_number column of the orders_table so the dim_card_details table must also be 120123 in size but the dim_card_details table size is 15309 which tells us that there is 25 pieces of invalid data that we must remove from the dim_card_details column. The invalid data that need to be cleaned can be viewed using:
```sql
SELECT DISTINCT card_number
FROM dim_card_details
WHERE card_number NOT IN (select card_number FROM orders_table
```
![Screenshot 2024-01-22 170211](https://github.com/samierouf/multinational-retail-data-centralisation68/assets/142994082/a9dd70d3-e408-4057-9ccb-aacdb73fd01f)


From this it can be seen that some of the card numbers have '?' in them so I remove using 
```python
pdf_data['card_number'] = pdf_data['card_number'].astype(str).str.replace(r'\?','', regex = True)
```
located in the `clean_card_data()` function which can be found in the `DataCleaning` class inside the `data_cleaning.py` file. we the rerun the previous sql queery to see if there is any that has been missed.

this cleaning is repeated for every table to make the data more uniform and be able to matches the orders_table it is during the cleaning where we drop columns and make sure that the data are in the correct format. One thing to look out for is any column that is related to dates as they can cause issues if they are not in the right format. I found that it SQL was much better at finding these irregular dates than python the SQL code I used to find them was:
```sql
SELECT *
FROM dim_card_details
WHERE NOT (dat_payment_confirmed is NULL OR date_payment_confirmed ~ '^\d{4}-\d{2}-\d{2}$';
```
![Screenshot 2024-01-22 181754](https://github.com/samierouf/multinational-retail-data-centralisation68/assets/142994082/5d9fc713-8709-48cb-bccc-72afb2aec7c9)

Here we can see that a number of the dates are not in the correct form and if python ```python pd.to_datetime()``` function was used they would come up as errors. so before we use the ```python pd.to_datetime()``` function to make the column into the right format they must be corrected which I have done by making a function called `correct_payment_dates()` in the `data_cleaning.py` file. in this function i created a dictionary to with the incorrectly formatted dates to their corrected form then mapped them over the date_payment_confirmed column of the card dataset to correct them. then used ```pd.to_datetime()``` to make the column to the right type and then the cleaned and processsed data is uploaded to sales_data database. This process is repeated for all tables. 

### Milestone 3
In this milestone we will be making a star-based schema for the database as well as make sure the columns are the correct data types. building a star-based schema where the orders_table as the central table will allow for easier understandability as well as making it easier to perform queries. this milestone can 9 parts:

- #### Part 1 `ms3_task1.sql`
  caste the columns of the orders_table toithe correct datatype.
- #### Part 2 `ms3_task2.sql`
  cast he columns of dim_users_table to the correct data type.
- #### Part 3 `ms3_task3.sql`
  merged the two 'latitude' columns into one and caste the columns to the correct datatype for dim_store_details.
- #### Part 4 `ms3_task4.sql`
  added a column called ' weight_range' which will tell delivery team if the product is light, mid_size, heavy or truck_required so they can make quick informed decision. removed the £ from the data in the product_price column.
- #### Part 5 `ms3_task5.sql`
  cast the columns to the correct datatype in the dim_product table
- #### Part 6 `ms3_task6.sql`
  updated the dim_date_time table with the correct data type
- #### Part 7 `ms3_task7.sql`
  updated the dim_card_details table to the correct datatypes
- #### Part 8 `ms3_task8.sql`
  creating primary keys for the other tables
- #### Part 9 `ms3_task9.sql`
  creating foreign keys in the order_table
when changing the column type to VARCHAR(?). To work out the max length the column needed to be i used the following code:
```sql
SELECT MAX(LENGTH(card_number::TEXT)) FROM dim_card_details;
```
![Screenshot 2024-01-27 134900](https://github.com/samierouf/multinational-retail-data-centralisation68/assets/142994082/9b77155d-f2cf-4ace-9509-4b7de347528f)


### Milestone 4
in this milestone we will be querying the data.

- #### How many stores does the business have and in which countries are they located in? `ms4_task1.sql`
  - ![Screenshot 2024-01-27 135956](https://github.com/samierouf/multinational-retail-data-centralisation68/assets/142994082/d5a64891-662c-478f-85cc-a17ba0c4b011)

- #### Which location currently have the most stores? `ms4_task2.sql`
  - ![Screenshot 2024-01-27 140552](https://github.com/samierouf/multinational-retail-data-centralisation68/assets/142994082/723332b7-6da0-4905-a0cc-fecaebe452ed)
- #### Which months produced the largest amount of sales? `ms4_task3.sql`
  - ![Screenshot 2024-01-27 141052](https://github.com/samierouf/multinational-retail-data-centralisation68/assets/142994082/7d24bee6-aa81-485a-bdab-db24a93a2ccb)
- #### How many sales are coming from online vs offline? `ms4_task4.sql`
  - ![Screenshot 2024-01-27 141220](https://github.com/samierouf/multinational-retail-data-centralisation68/assets/142994082/2ca0d532-ce3f-4def-a624-20cdc51ab7fd)
- #### What percentage of sales come through each store type? `ms4_task5.sql`
  - ![Screenshot 2024-01-27 141334](https://github.com/samierouf/multinational-retail-data-centralisation68/assets/142994082/3a2056db-859a-4201-9606-a6b7ac545ea7)
- #### Which month in each year produced the highest cost of sales? `ms4_task6.sql`
  - ![Screenshot 2024-01-27 143754](https://github.com/samierouf/multinational-retail-data-centralisation68/assets/142994082/575f7f88-0570-4c38-b4fb-b7a6d0ac0cc8)
- #### What is our staff head count? `ms4_task7.sql`
  - ![Screenshot 2024-01-27 143850](https://github.com/samierouf/multinational-retail-data-centralisation68/assets/142994082/715daf56-f4de-48ba-b719-0788b772df34)
- #### Which German store type is selling the most? `ms4_task8.sql`
  - ![Screenshot 2024-01-27 143949](https://github.com/samierouf/multinational-retail-data-centralisation68/assets/142994082/d315774f-848a-49f1-8713-75eadcb22724)
- #### How quickly is the company making sales? `ms4_task9.sql`
  - ![Screenshot 2024-01-27 144314](https://github.com/samierouf/multinational-retail-data-centralisation68/assets/142994082/1e15f892-3aab-432c-b229-f35867e32551)



## Learning
### Data Inspection and Cleaning
- Importance of inspecting data before cleaning.
- Relying on the source of truth for accurate data.

### Handling Null Values
- Treating all data that doesn't conform to the desired format as null.
- Balancing the removal of null data with the risk of losing useful information.

### Focus on Important Data
- Recognizing the significance of focusing on important data.
- Producing better results by prioritizing relevant information.

### Understanding Star-Based Schemas
- Benefits of star-based schemas for scalability and simplicity.
- Facilitating easier data querying with star-based schema structures.

### SQL Skills Development
- Creating Common Table Expressions (CTEs).
- Joining tables, converting data types, and comfortable usage of SQL.

### Python Techniques
- Introduction to boolean indexing.
- Problem-solving related to data reading and cleaning.
- 
### Handling Null Values
### Handling Null Values
- Learned from an instance where treating all data not in the desired format as null had consequences.
- Encountered a scenario where spending time to correct data format proved to be worthwhile.
  - **Example:** During the cleaning process, I initially removed all dates that were not in the correct format. However, this approach led to issues in creating primary and foreign keys. It was only when I started focusing on the important data that I realized correcting the formatting issues, instead of treating them as null, was worth the time invested.

### Python Techniques
- Encountered a challenge with `str.replace(r'\D', '')` and discovered the correct solution: `astype(str).str.replace(r'\D', '')`.

## Reflecting on Real-World Application
- Recognizing how these skills can be applied to future projects or in a professional database management setting.
- Understanding the practical implications of data inspection, cleaning, and SQL usage in real-world scenarios.






 




