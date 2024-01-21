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

class DataCleaning:

    regex_expression = r'^(?:(?:\(?(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?(?:\(?0\)?[\s-]?)?)|(?:\(?0))(?:(?:\d{5}\)?[\s-]?\d{4,5})|(?:\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3}))|(?:\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4})|(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}))(?:[\s-]?(?:x|ext\.?|\#)\d{3,4})?$'

########### orgiginal###############################################
    # def clean_user_data(self, data):
    #     # makes data all lower case
    #     columns_to_lower = ['first_name', 'last_name', 'company', 'email_address', 'address', 'country', 'country_code', 'phone_number', 'join_date', 'user_uuid']
    #     data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
    #     # removing nulls
    #     data_columns = ['index', 'first_name', 'last_name', 'date_of_birth', 'company', 'email_address', 'address', 'country', 'country_code', 'phone_number', 'join_date', 'user_uuid']
    #     data[data_columns] = data[data_columns].replace(['', 'nan', 'null', 'none'], np.nan)

    #     data.dropna(axis = 0, how='any', inplace=True)
    #     # cleaning dates
    #     data['date_of_birth'] = pd.to_datetime(data['date_of_birth'], format='%Y-%m-%d', errors='coerce')
    #     data['join_date'] = pd.to_datetime(data['join_date'], format='%Y-%m-%d', errors='coerce')
    #     ## dates that are not possible join_date cant be before date_of_birth. join-date and birth_date cant be before the current date
    #     for column_index in range(len(data)):
    #         if data['join_date'].values[column_index] < data['date_of_birth'].values[column_index]:
    #             data['join_date'].values[column_index] = np.nan
    #         else:
    #             pass
        
    #     for column_index in range(len(data)):
    #         if data['join_date'].values[column_index] > date.today():
    #             data['join_date'].values[column_index] = np.nan
    #         elif data['date_of_birth'].values[column_index] > date.today():
    #             data['date_of_birth'].values[column_index] = np.nan
    #         else:
    #             pass

    #     data.dropna(subset= ['date_of_birth', 'join_date'], axis = 0, how='any', inplace=True)
    #     data.loc[~data['phone_number'].str.match(self.regex_expression), 'phone_number'] = np.nan
    #     data.dropna(axis = 0, how='any', inplace=True)

    #     return data





