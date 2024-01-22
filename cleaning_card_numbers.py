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



#############################################################################################################################################################################################################################################################
##### COde below works /


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
import re
connector = DatabaseConnector()
extractor = DataExtractor()
cleaning = DataCleaning()

pgadmin_creds = connector.read_db_creds('pgadmin_creds.yaml')
pgadmin_engine = connector.init_db_engine(pgadmin_creds)



#### function


# def clean_card_data2(pdf_data):
#      # making everything lowercase
#     columns_to_lower = ['card_provider']
#     pdf_data[columns_to_lower] = pdf_data[columns_to_lower].apply(lambda x: x.str.lower())
#     ### get rid of ?
#     pdf_data['card_number'] = pdf_data['card_number'].apply(lambda x: re.sub(r'\?', '', str(x))) 
#     pdf_data['card_number'] = pdf_data['card_number'].astype(str).str.replace(r'\?','', regex = True)


#     # checks to see if he values in card_number are numeric if not assignes nan
#     for card_index in range(len(pdf_data)):
#         if str(pdf_data['card_number'].values[card_index]).isnumeric() == False:
#             pdf_data['card_number'].values[card_index] = np.nan
#         else:
#             pass
#     # formating the date 
#     pdf_data['date_payment_confirmed'] = pd.to_datetime(pdf_data['date_payment_confirmed'], errors='ignore')
#     # pdf_data.dropna(subset = ['date_payment_confirmed'], axis = 0, how='any', inplace = True) #15250 left
#     pdf_data.dropna(subset = ['card_number'], axis = 0, how='any', inplace = True) #1528 left just this one being used

#     return pdf_data
    
def correct_dates(pdf_data):
    data = pd.DataFrame({
    'date_payment_confirmed': ["December 2021 17", "2005 July 01", "December 2000 01", "2008 May 11", "October 2000 04",
                               "September 2016 04", "2017/05/15", "May 1998 09"]
                            })
    date_mapping = {
    "December 2021 17": '2021-12-17',
    "2005 July 01": '2005-07-01',
    "December 2000 01": '2000-12-01',
    "2008 May 11": '2008-05-11',
    "October 2000 04": '2000-10-04',
    "September 2016 04": '2016-09-04',
    "2017/05/15": '2017-05-15',
    "May 1998 09": '1998-05-09'
                    }
    
    pdf_data['date_payment_confirmed'] = data['date_payment_confirmed'].replace(date_mapping)
    data.dropna(subset=['date_payment_confirmed'], axis=0, how='any', inplace=True)

    return data

def correct_dates(pdf_data):
    date_mapping = {
        "December 2021 17": '2021-12-17',
        "2005 July 01": '2005-07-01',
        "December 2000 01": '2000-12-01',
        "2008 May 11": '2008-05-11',
        "October 2000 04": '2000-10-04',
        "September 2016 04": '2016-09-04',
        "2017/05/15": '2017-05-15',
        "May 1998 09": '1998-05-09'
    }

    pdf_data['date_payment_confirmed'] = pdf_data['date_payment_confirmed'].replace(date_mapping)

    return pdf_data

def clean_card_data2(pdf_data):
    pdf_data = correct_dates(pdf_data)
        # making everything lowercase
    columns_to_lower = ['card_provider']
    pdf_data[columns_to_lower] = pdf_data[columns_to_lower].apply(lambda x: x.str.lower())

            # Replace '?' in card_number
    pdf_data['card_number'] = pdf_data['card_number'].apply(lambda x: re.sub(r'\?', '', str(x)))

            # Check if the values in card_number are numeric, if not assign NaN
    # pdf_data['card_number'] = pd.to_numeric(pdf_data['card_number'], errors='coerce')

    for card_index in range(len(pdf_data)):
        if str(pdf_data['card_number'].values[card_index]).isnumeric() == False:
            pdf_data['card_number'].values[card_index] = np.nan
        else:
            pass

            # Convert date_payment_confirmed to the correct format
    pdf_data['date_payment_confirmed'] = pd.to_datetime(pdf_data['date_payment_confirmed'], errors='coerce')

            # Drop rows with NaN values in card_number
    pdf_data.dropna(subset=['card_number'], axis=0, how='any', inplace=True)

            # Drop rows with NaN values in date_payment_confirmed
    pdf_data.dropna(subset=['date_payment_confirmed'], axis=0, how='any', inplace=True)

    return pdf_data






#### task 4
pdf_data = extractor.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
show(pdf_data)
print(pdf_data)
print(pdf_data.columns)
pdf_data.info()
# pdf_data['card_number'] = pdf_data['card_number'].str.replace(r'\?','')
# pdf_data['card_number'] = pdf_data['card_number'].astype(str).str.replace(r'\?','', regex = True)
# pdf_data.drop(columns='date_payment_confirmed', inplace=True)
# pdf_data.drop_duplicates(subset=['card_number'], inplace=True)
# pdf_data['card_number'] = pdf_data['card_number'].apply(lambda x: re.sub(r'\?', '', str(x))) ## mybe
# pdf_data['card_number'] = pdf_data['card_number'].str.lstrip('?')
pdf_data = clean_card_data2(pdf_data)
show(pdf_data)
print(pdf_data)
print(pdf_data.columns)
pdf_data.info()
connector.upload_to_db(pdf_data, 'dim_card_details', pgadmin_engine)
print('end4')



# code works use it 



