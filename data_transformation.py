import yaml
import sqlalchemy
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import inspect
import psycopg2
import numpy
import re
from datetime import datetime
import datetime as dt

class DataTransform:
    
    '''
    Class for transforming the data
    
    Methods:
        format_date(data, column_name): changes column type to datetime.
        remove_non_numbers(data, column_name): removes non numeric items from the string.
        column_to_int(data, column_name): converts data to Int64 type
    '''

    def format_date(self, data, column_name):
        '''
        Function to convert columns to datetime type.

        Args:
            data (pd.Dataframe): dataframe that contains the column you want to change.
            column_name (str): name of column you want to chage to datetime.

        Return
            pd.Datrame: dataframe returned with selected column now as type datetime 

        '''
        data[column_name] = pd.to_datetime(data[column_name], format='%b-%Y')
        return data
           
    def remove_non_numbers(self, data, column_name):
        '''
        Function to remove non numbers from a string

        Args:
            data (pd.Dataframe): dataframe that contains the column you want to change.
            column_name (str): name of column that contains the data.
        
        Return:
            pd.Dataframe:  dataframe returned with selected column with non numeric charcaters removed 

            '''
        data[column_name] = data[column_name].astype(str).str.extract('(\d+)', expand=False) # regx removes 
        return data
    
    def column_to_int(self, data, column_name):
        '''
        Function to convert columns to Int64 type.

        Args:
            data (pd.Dataframe): dataframe that contains the column you want to change.
            column_name (str): name of column you want to change to int.

        Return
            pd.Datrame: dataframe returned with selected column now as type Int64 

        '''
        data[column_name] = data[column_name].astype('Int64')
        return data
    

