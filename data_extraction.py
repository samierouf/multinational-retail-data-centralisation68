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
    """
    class for extracting data from various sources
    
    Attributes:
        none

    Methods:
    __init__(self) -> None: Initializes the DataExtractor class
    read_rd_table(engine, data): reads data drom a RDS datatbase
    retrieve_pdf_data(link): extracts datat from a PDF
    API_key(): holds the api key information
    list_number_of_store(number_of_stores_endpoint): list number of stores to extract
    retrieve_store_data(number_of_stores): extracts alll the stores from the API
    extract_from_s3(address, file_name): extracts data from an S£ bucket using boto3 package
    extract_from_s3_json(url): extracts data from a JSON file stored in S3
    """

    def __init__(self) -> None:
        pass

    def read_rds_table(self, engine, table_name): # table_name for only individual tables not multiple
        """
        this function reads data from an RDS database table.

        Args:
            engine: Database engine.
            table_name (str): Name of the table to read.

        Returns:
            pd.DataFrame: DataFrame containing the read data.
        """
        with engine.connect() as conn:
            read_data = pd.read_sql_table(table_name, engine)

            return read_data
        
    def retrieve_pdf_data(self, link): # link must be in parentheseas ''
        """
        function extracts data from a PDF file.

        Args:
            link (str): Link to the PDF file.

        Returns:
            pd.DataFrame: DataFrame containing the extracted data.
        """

        pdf_data_frame = tabula.read_pdf(link, pages='all')
        pdf_data_frame = pd.concat(pdf_data_frame)
        show(pdf_data_frame)

        return pdf_data_frame
    
    @ staticmethod
    def API_key(self):
        """
        contains the API key information.

        Args:
            none

        Returns:
            dict: dictionary containing the API key.
        """
        API = {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}

        return API
    
    def list_number_of_stores(self, number_of_stores_endpoint):
        """
        Retrieves the number of stores from a specified endpoint.

        Args:
            number_of_stores_endpoint (str): Endpoint for retrieving the number of stores.

        Returns:
            int: Number of stores.
        """
        header = self.API_key()
        response = requests.get(number_of_stores_endpoint, headers= header)
        repos = response.json()
        number_of_stores = repos['number_stores']

        return number_of_stores

    def retrive_store_data(self, number_of_stores):
        """
        the function rretrieves store data for the specified number of stores.

        Args:
            number_of_stores (int): Number of stores to retrieve data for.

        Returns:
            pd.DataFrame: DataFrame containing store data.
        """
        headers = self.API_key()
        store_data = [] # list of data frames
        for store_number in range(number_of_stores): #tore_number will be the number of the store dta is being extracted for
            response = requests.get(f'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}', headers= headers)
            repos = response.json() #data of store
            normalized_repos = pd.json_normalize(repos) # dataframe of the store
            store_data.append(normalized_repos) # addes the datat frame of the dtore datat to the list of datat frames
        df_store_data = pd.concat(store_data, ignore_index=True).reset_index(drop=True)

        return df_store_data


    def extract_from_s3(self, address, file_name):
        """
        function extracts data from an S3 bucket.

        Args:
            address (str): S3 bucket address.
            file_name (str): local file name on computer to save the downloaded data.

        Returns:
            pd.DataFrame: DataFrame containing the extracted data.
        """
        bucket, key = address.replace("s3://", "").split("/", 1)
        s3 = boto3.client('s3')
        s3.download_file(bucket, key, file_name)
        file = pd.read_csv(file_name)

        return file

    def extract_from_s3_json(self, url):
        """
        Extracts data from a JSON file stored in S3 that is on a public URL

        Args:
            url (str): public URL of the JSON file.

        Returns:
            pd.DataFrame: DataFrame containing the extracted data.
        """
        response = requests.get(url)
        repos = response.json() 
        data= pd.DataFrame([])
        for column_name in repos.keys():
            value_list = []
            for i in repos[column_name].keys():
                value_list.append(repos[column_name][i])
            data[column_name] = value_list

        return data
    
        

        



    
        
    
