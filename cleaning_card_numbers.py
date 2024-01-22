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
from cleaning_new_sun_12pm import DataCleaning
from pandasgui import show
connector = DatabaseConnector()
extractor = DataExtractor()
cleaning = DataCleaning()

pgadmin_creds = connector.read_db_creds('pgadmin_creds.yaml')
pgadmin_engine = connector.init_db_engine(pgadmin_creds)



#### function


def clean_card_data(self, pdf_data):
     # making everything lowercase
    columns_to_lower = ['card_provider']
    pdf_data[columns_to_lower] = pdf_data[columns_to_lower].apply(lambda x: x.str.lower())
    ### get rid of ?
    for card_index_1 in range(len(pdf_data)):
        if '?' in str(pdf_data['card_number'].values[card_index_1]) == True:
                pdf_data['card_number'].values[card_index_1] = str(pdf_data['card_number'].values[card_index_1]).replace('?', '')
        else:
            pass


    # checks to see if he values in card_number are numeric if not assignes nan
    for card_index in range(len(pdf_data)):
        if str(pdf_data['card_number'].values[card_index]).isnumeric() == False:
            pdf_data['card_number'].values[card_index] = np.nan
        else:
            pass
    # formating the date 
    pdf_data['date_payment_confirmed'] = pd.to_datetime(pdf_data['date_payment_confirmed'], format='%Y-%m-%d', errors='coerce')
    pdf_data.dropna(axis = 0, how='any', inplace = True) #15250 left
    pdf_data.dropna(subset = ['card_number'], axis = 0, how='any', inplace = True) #1528 left just this one being used

    return pdf_data
    






#### task 4
pdf_data = extractor.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
show(pdf_data)
print(pdf_data)
print(pdf_data.columns)
pdf_data.info()
pdf_data.drop(columns='date_payment_confirmed', inplace=True)
pdf_data.drop_duplicates(subset=['card_number'], inplace=True)
# for card_index_1 in range(len(pdf_data)):
#     str_pdf_cn = str(pdf_data['card_number'].values[card_index_1])
#     if '?' in str_pdf_cn == True:
#         pdf_data['card_number'].values[card_index_1] = int(str_pdf_cn.replace('?', ''))
#     else:
#         pass

# pdf_data['card_number'] = pdf_data['card_number'].str.replace('?','')
# pdf_data = pdf_data[str(pdf_data['card_number']).isnumeric() == True] 

pdf_data['card_number'] = pdf_data['card_number'].str.replace('?', '')
# pdf_data['card_number'] = pdf_data['card_number'].replace('[^0-9]', '', regex=True) # gets rid of everyhing
# pdf_data["card_number"] = pdf_data['card_number'].str.replace('[^\w\s]','')
# pdf_data = pdf_data[~pdf_data['card_number'].str.contains('[a-zA-Z?]', na=False)]
# pdf_data = cleaning.clean_card_data(pdf_data)
show(pdf_data)
print(pdf_data)
print(pdf_data.columns)
pdf_data.info()
connector.upload_to_db(pdf_data, 'dim_card_details', pgadmin_engine)
print('end4')



