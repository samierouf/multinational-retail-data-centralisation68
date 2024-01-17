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
pgadmin_creds = connector.read_db_creds('pgadmin_creds.yaml')
pgadmin_engine = connector.init_db_engine(pgadmin_creds)
# # connector.upload_to_db(data, 'dim_users', pgadmin_engine)
##### task 4
# pdf_data = extractor.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
# pdf_data = cleaning.clean_card_data(pdf_data)
# connector.upload_to_db(pdf_data, 'dim_card_details', pgadmin_engine)

##### task 5

number_of_stores = extractor.list_number_of_stores('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores')
print(number_of_stores)
api_data = extractor.retrive_store_data(number_of_stores)
api_data = cleaning.called_clean_store_data(api_data)
connector.upload_to_db(api_data, 'dim_store_details', pgadmin_engine)


###### task 6
