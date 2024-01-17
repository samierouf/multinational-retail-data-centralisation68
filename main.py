import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
import pandas as pd
import numpy as np 
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning
from pandasgui import show


connector = DatabaseConnector()
extractor = DataExtractor()
cleaning = DataCleaning()

# db_creds = connector.read_db_creds('db_creds.yaml')
# engine = connector.init_db_engine(db_creds)
# tables = connector.list_db_tables(engine)
# print(tables)
# data = extractor.read_rds_table(engine, 'legacy_users')
# print(data)
# data = cleaning.clean_user_data(data)
# print(data)
# pgadmin_creds = connector.read_db_creds('pgadmin_creds.yaml')
# pgadmin_engine = connector.init_db_engine(pgadmin_creds)
# # connector.upload_to_db(data, 'dim_users', pgadmin_engine)
##### task 4
# pdf_data = extractor.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
# pdf_data = cleaning.clean_card_data(pdf_data)
# connector.upload_to_db(pdf_data, 'dim_card_details', pgadmin_engine)

##### task 5

number_of_stores = extractor.list_number_of_stores('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores')
print(number_of_stores)
data = extractor.retrive_store_data(number_of_stores)
print(type(data))
print(data)
print(data.columns)
#show(data)



data.info()
data.drop(columns='lat', inplace=True)#
data.drop(columns='index', inplace=True)
data.info()
data.drop_duplicates(inplace=True)
columns_to_lower = [ 'address', 'locality', 'store_code','store_type','country_code', 'continent']
data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
data.drop_duplicates(inplace=True)
print(data['longitude'])
print(data['staff_numbers'])
data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')
data['staff_numbers'] = pd.to_numeric(data['staff_numbers'], errors='coerce')
data.info()
print(data['longitude'])
print(data['locality'])
print(data['store_code'])
print(data['staff_numbers'])
print(data['opening_date'])
print(data['store_type'])
print(data['latitude'])
print(data['country_code'])
print(data['continent'])

#show(data)
# # Index([ 'address', 'longitude', 'locality', 'store_code',
#        'staff_numbers', 'opening_date', 'store_type', 'latitude',
#        'country_code', 'continent'],
#       dtype='object')