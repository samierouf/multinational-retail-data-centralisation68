import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
import pandas as pd
import numpy as np 
from database_utils import DatabaseConnector
import tabula
from pandasgui import show
import requests
import boto3 

class DataExtractor:

    def read_rds_table(self, engine, table_name): # table_name for only individual tables not multiple
        with engine.connect() as conn:
            read_data = pd.read_sql_table(table_name, engine)

            return read_data
        
    def retrieve_pdf_data(self, link): # link must be in parentheseas ''
        pdf_data_frame = tabula.read_pdf(link, pages='all')
        pdf_data_frame = pd.concat(pdf_data_frame)
        show(pdf_data_frame)

        return pdf_data_frame
    
    def API_key(self):
        API = {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}

        return API
    
    def list_number_of_stores(self, number_of_stores_endpoint):
        header = self.API_key()
        response = requests.get(number_of_stores_endpoint, headers= header)
        repos = response.json()
        number_of_stores = repos['number_stores']

        return number_of_stores

    def retrive_store_data(self, number_of_stores):
        headers = self.API_key()
        store_data = [] # list of data frames
        for store_number in range(number_of_stores): #tore_number will be the number of the store dta is being extracted for
            response = requests.get(f'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}', headers= headers)
            repos = response.json() #data of store
            normalized_repos = pd.json_normalize(repos) # dataframe of the store
            store_data.append(normalized_repos) # addes the datat frame of the dtore datat to the list of datat frames
        df_store_data = pd.concat(store_data, ignore_index=True).reset_index(drop=True)

        return df_store_data

    # def extract_from_s3(self, address):
    #     s3 = boto3.client('s3') 
    #     s3.download_file(address,'products.csv', '/Downloads/Multinational_retail_data/s3_products.csv')
    #     file = pd.read_csv('s3_products.csv')
    #     return file

    def extract_from_s3(self, address, file_name):
        bucket, key = address.replace("s3://", "").split("/", 1)
        s3 = boto3.client('s3')
        s3.download_file(bucket, key, file_name)
        file = pd.read_csv(file_name)

        return file

    def extract_from_s3_json(self, url):
        response = requests.get(url)
        repos = response.json() 
        data= pd.DataFrame([])
        for column_name in repos.keys():
            value_list = []
            for i in repos[column_name].keys():
                value_list.append(repos[column_name][i])
            data[column_name] = value_list

        return data
    
    
        

        



    
        
    
