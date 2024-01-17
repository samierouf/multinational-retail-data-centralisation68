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


# class DataCleaning:
#     regex_expression = '^(?:(?:\(?(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?(?:\(?0\)?[\s-]?)?)|(?:\(?0))(?:(?:\d{5}\)?[\s-]?\d{4,5})|(?:\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3}))|(?:\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4})|(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}))(?:[\s-]?(?:x|ext\.?|\#)\d{3,4})?$' #Our regular expression to match

#     def clean_user_data(self, data):
#         data.drop(columns='index', inplace=True)
#         #making all text lowercase
#         data['first_name'] = data['first_name'].str.lower()
#         data['last_name'] = data['last_name'].str.lower()
#         data['company'] = data['company'].str.lower()
#         data['email_address'] = data['email_address'].str.lower()
#         data['address'] = data['address'].str.lower()
#         data['country'] = data['country'].str.lower()
#         data['user_uuid'] = data['user_uuid'].str.lower()
#         #dropping duplicates
#         data = data.drop_duplicates()
#         #uk numbers only
#         data.loc[~data['phone_number'].str.match(self.regex_expression), 'phone_number'] = np.nan
#         data = data.drop_duplicates(subset=['user_uuid'])
#         # valid date format only
#         pd.to_datetime(data['join_date'], format='%Y-%m-%d', errors='coerce')
#         pd.to_datetime(data['date_of_birth'], format='%Y-%m-%d', errors='coerce')
#         #dropping null values
#         data = data.dropna(axis= 0, how= 'any')


class DataCleaning:
    
    regex_expression = r'^(?:(?:\(?(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?(?:\(?0\)?[\s-]?)?)|(?:\(?0))(?:(?:\d{5}\)?[\s-]?\d{4,5})|(?:\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3}))|(?:\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4})|(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}))(?:[\s-]?(?:x|ext\.?|\#)\d{3,4})?$'

    def clean_user_data(self, data):
        # drop index colunm
        data.drop(columns='index', inplace=True)
        # making all text lowercase
        columns_to_lower = ['first_name', 'last_name', 'company', 'email_address', 'address', 'country', 'user_uuid']
        data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
        # dropping duplicates
        data.drop_duplicates(inplace=True)
        # uk numbers only
        data.loc[~data['phone_number'].str.match(self.regex_expression), 'phone_number'] = np.nan
        # dropping duplicates based on 'user_uuid'
        data.drop_duplicates(subset=['user_uuid'], inplace=True)
        # valid date format only
        data['join_date'] = pd.to_datetime(data['join_date'], format='%Y-%m-%d', errors='coerce')
        data['date_of_birth'] = pd.to_datetime(data['date_of_birth'], format='%Y-%m-%d', errors='coerce')
        # dropping null values
        data.dropna(axis=0, how='any', inplace=True)
        data.reset_index(drop = True, inplace = True)
        show(data)
        return data
    
    def clean_card_data(self, pdf_data):
        columns_to_lower = ['card_provider']
        pdf_data[columns_to_lower] = pdf_data[columns_to_lower].apply(lambda x: x.str.lower())
        pdf_data.drop_duplicates(inplace=True)
        pdf_data.reset_index(drop = True, inplace = True)
        for card_index in range(len(pdf_data)):
            if str(pdf_data['card_number'].values[card_index]).isnumeric() == False:
                pdf_data['card_number'].values[card_index] = np.nan
            else:
                pass
        pdf_data['card_number'] = pd.to_numeric(pdf_data['card_number'], errors='coerce')
        pdf_data['date_payment_confirmed'] = pd.to_datetime(pdf_data['date_payment_confirmed'], format='%Y-%m-%d', errors='coerce')
        pdf_data.dropna(axis=0, how='any', inplace=True)
        pdf_data.reset_index(drop = True, inplace = True)
        show(pdf_data)
        return pdf_data
    
    def called_clean_store_data(self, data):
        data.drop(columns='lat', inplace=True)#
        data.drop(columns='index', inplace=True)
        data.drop_duplicates(inplace=True)
        columns_to_lower = [ 'address', 'locality', 'store_type','country_code', 'continent']
        data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
        data.drop_duplicates(inplace=True)
        data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')
        data['staff_numbers'] = pd.to_numeric(data['staff_numbers'], errors='coerce')
        data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce')
        data['opening_date'] = pd.to_datetime(data['opening_date'], format='%Y-%m-%d', errors='coerce')
        data.dropna(axis=0, how='any', inplace=True)
        data.reset_index(drop = True, inplace = True)
        data['continent'].replace('eeeurope', 'europe', inplace=True)
        data['continent'].replace('eeamerica', 'america', inplace=True)
        data.drop_duplicates(inplace=True)
        data.dropna(axis=0, how='any', inplace=True)
        data.reset_index(drop = True, inplace = True)
        show(data)
        return data



    
        
    


        
    
        
    


        
