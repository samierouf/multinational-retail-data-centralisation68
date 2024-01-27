import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
import pandas as pd
import numpy as np 
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from pandasgui import show
import tabula
from datetime import date
import re
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning
from pandasgui import show
connector = DatabaseConnector()
extractor = DataExtractor()
cleaning = DataCleaning()

pgadmin_creds = connector.read_db_creds('pgadmin_creds.yaml')
pgadmin_engine = connector.init_db_engine(pgadmin_creds)

if __name__ == "__main__":
    #### Users Data ####
    db_creds = connector.read_db_creds('db_creds.yaml')
    engine = connector.init_db_engine(db_creds)
    tables = connector.list_db_tables(engine)
    users_data = extractor.read_rds_table(engine, 'legacy_users')
    users_data = cleaning.clean_user_data(users_data)
    connector.upload_to_db(users_data, 'dim_users', pgadmin_engine)

    #### card data ####
    card_data = extractor.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
    card_data = cleaning.clean_card_data(card_data)
    connector.upload_to_db(card_data, 'dim_card_details', pgadmin_engine)

    #### store data ####
    number_of_stores = extractor.list_number_of_stores('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores')
    store_data = extractor.retrive_store_data(number_of_stores)
    store_data = cleaning.called_clean_store_data(store_data)
    connector.upload_to_db(store_data, 'dim_store_details', pgadmin_engine)

    #### product data ####
    address = 's3://data-handling-public/products.csv'
    product_data = extractor.extract_from_s3(address, 's3_products.csv')
    product_data = cleaning.clean_products_data(product_data)
    connector.upload_to_db(product_data, 'dim_products', pgadmin_engine)

    #### orders data ####
    db_creds = connector.read_db_creds('db_creds.yaml')
    engine = connector.init_db_engine(db_creds)
    tables = connector.list_db_tables(engine)
    data_7 = extractor.read_rds_table(engine, 'orders_table')
    data_7 = cleaning.clean_orders_data(data_7)
    connector.upload_to_db(data_7, 'orders_table', pgadmin_engine)

    #### date data ####
    address = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'
    data_8 = extractor.extract_from_s3_json(address)
    data_8 = cleaning.clean_date_details(data_8)
    connector.upload_to_db(data_8, 'dim_date_times', pgadmin_engine)
