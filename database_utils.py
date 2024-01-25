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

class DatabaseConnector:
    """
    A class for connecting to a PostgreSQL database.

    Attributes:
        None

    Methods:
        read_db_creds(yaml_file_name): reads database credentials from a YAML file.

        init_db_engine(db_creds): iinitializes a database engine using the provided credentials.

        list_db_tables(engine):lists the tables present in the connected database.

        upload_to_db(data_frame, table_name, sql_engine): uploads a DataFrame to a specified table in the connected database.
    """
    def read_db_creds(self, yamal_file_name):
        """
        reads database credentials from YAML file.

        Args:
            yaml_file_name (str): name of YAML file containing database credentials.

        Returns:
            dict: dictionary containing database credentials.
        """
        with open(yamal_file_name, 'r') as file:
            db_creds = yaml.safe_load(file)
            
        return db_creds
    
    def init_db_engine(self, db_creds):
        """
        fucntion initializes a database engine using the database credentials.

        Args:
            db_creds (dict): Dictionary containing database credentials.

        Returns:
            sqlalchemy.engine.base.Engine: Initialized database engine.
        """
        engine = create_engine(f"postgresql+psycopg2://{db_creds['RDS_USER']}:{db_creds['RDS_PASSWORD']}@{db_creds['RDS_HOST']}:{db_creds['RDS_PORT']}/{db_creds['RDS_DATABASE']}")
        
        return engine
    
    def list_db_tables(self, engine):
        """
        fucntion lists the tables present in the database.

        Args:
            engine (sqlalchemy.engine.base.Engine): Database engine.

        Returns:
            list: List of table names.
        """       
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        return tables
    
    def upload_to_db(self, data_frame, table_name, sql_engine):
        """
        function uploads a DataFrame to a specified table in the connected database.

        Args:
            data_frame (pd.DataFrame): DataFrame to be uploaded.
            table_name (str): Name of the table to upload data to.
            sql_engine (sqlalchemy.engine.base.Engine): Database engine.

        Returns:
            uploads to datatbase
        """
        pg_admin_upload = data_frame.to_sql(table_name, sql_engine, if_exists='replace')
        
        return pg_admin_upload
