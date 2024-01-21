class DataCleaning:

    regex_expression = r'^(?:(?:\(?(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?(?:\(?0\)?[\s-]?)?)|(?:\(?0))(?:(?:\d{5}\)?[\s-]?\d{4,5})|(?:\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3}))|(?:\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4})|(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}))(?:[\s-]?(?:x|ext\.?|\#)\d{3,4})?$'

    def clean_user_data(self, data):
        # makes data all lower case
        columns_to_lower = ['first_name', 'last_name', 'company', 'email_address', 'address', 'country', 'country_code', 'phone_number', 'join_date', 'user_uuid']
        data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
        # removing nulls
        data_columns = ['index', 'first_name', 'last_name', 'date_of_birth', 'company', 'email_address', 'address', 'country', 'country_code', 'phone_number', 'join_date', 'user_uuid']
        data[data_columns] = data[data_columns].replace(['', 'nan', 'null', 'none'], np.nan)

        data.dropna(axis = 0, how='any', inplace=True)
        # cleaning dates
        data['date_of_birth'] = pd.to_datetime(data['date_of_birth'], format='%Y-%m-%d', errors='coerce')
        data['join_date'] = pd.to_datetime(data['join_date'], format='%Y-%m-%d', errors='coerce')
        ## dates that are not possible join_date cant be before date_of_birth. join-date and birth_date cant be before the current date
        # for column_index in range(len(data)):
        #     if data['join_date'].values[column_index] < data['date_of_birth'].values[column_index]:
        #         data['join_date'].values[column_index] = pd.NaT
        #     else:
        #         pass
        today_datetime = pd.to_datetime(date.today())



        for column_index in range(len(data)):
            join_date_value = data['join_date'].values[column_index]
            DOB_value = data['date_of_birth'].values[column_index]

            # Check if the value is not NaT before performing the comparison
            if not pd.isna(join_date_value) and join_date_value > today_datetime:
                data['join_date'].values[column_index] = pd.NaT
            elif not pd.isna(DOB_value) and DOB_value > today_datetime:
                data['date_of_birth'].values[column_index] = pd.NaT
            elif join_date_value < DOB_value:
                data['join_date'].values[column_index] = False
            else:
                pass

        # Use boolean indexing to remove rows where 'join_date' is False
        data = data[data['join_date'] != False]

        data.dropna(subset= ['date_of_birth', 'join_date'], axis=0, how='any', inplace=True)
        data.loc[~data['phone_number'].str.match(self.regex_expression), 'phone_number'] = np.nan
        data.dropna(axis=0, how='any', inplace=True)

        return data



    def clean_card_data(self, data): # 2476
        # makes data all lower case
        columns_to_lower = ['card_number', 'expiry_date', 'card_provider', 'date_payment_confirmed']
        data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
        # removing nulls
        data_columns = ['card_number', 'expiry_date', 'card_provider', 'date_payment_confirmed']
        data[data_columns] = data[data_columns].replace(['', 'nan', 'null', 'none'], np.nan)

        data.dropna(axis = 0, how='any', inplace=True)

        # cleaning dates
        data['expiry_date'] = pd.to_datetime(data['expiry_date'], format='%m/%y', errors='coerce')
        data['date_payment_confirmed'] = pd.to_datetime(data['date_payment_confirmed'], errors='coerce')

        today_datetime = pd.to_datetime(date.today())

        data = data[~((~data['date_payment_confirmed'].isna()) & (data['date_payment_confirmed'] > today_datetime))]

        # checking card_numbers
        for card_index in range(len(data)):
            if str(data['card_number'].values[card_index]).isnumeric() == False:
                data['card_number'].values[card_index] = np.nan
            else:
                pass
        
        data = data[~(data['card_number'] == False)]

        data.dropna(axis = 0, how='any', inplace = True)

        return data

####################################################################################################################################################################################################################################################################################################################################


class DataCleaning:

    regex_expression = r'^(?:(?:\(?(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?(?:\(?0\)?[\s-]?)?)|(?:\(?0))(?:(?:\d{5}\)?[\s-]?\d{4,5})|(?:\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3}))|(?:\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4})|(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}))(?:[\s-]?(?:x|ext\.?|\#)\d{3,4})?$'

    def clean_user_data(self, data): ###11508
        # makes data all lower case
        columns_to_lower = ['first_name', 'last_name', 'company', 'email_address', 'address', 'country', 'country_code', 'phone_number', 'join_date', 'user_uuid']
        data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
        # removing nulls
        data_columns = ['index', 'first_name', 'last_name', 'date_of_birth', 'company', 'email_address', 'address', 'country', 'country_code', 'phone_number', 'join_date', 'user_uuid']
        data[data_columns] = data[data_columns].replace(['', 'nan', 'null', 'none'], np.nan)

        data.dropna(axis = 0, how='any', inplace=True)
        # cleaning dates
        data['date_of_birth'] = pd.to_datetime(data['date_of_birth'], errors='coerce')
        data['join_date'] = pd.to_datetime(data['join_date'], errors='coerce')
        ## dates that are not possible join_date cant be before date_of_birth. join-date and birth_date cant be before the current date
        # for column_index in range(len(data)):
        #     if data['join_date'].values[column_index] < data['date_of_birth'].values[column_index]:
        #         data['join_date'].values[column_index] = pd.NaT
        #     else:
        #         pass
        today_datetime = pd.to_datetime(date.today())



        for column_index in range(len(data)):
            join_date_value = data['join_date'].values[column_index]
            DOB_value = data['date_of_birth'].values[column_index]

            # Check if the value is not NaT before performing the comparison
            if not pd.isna(join_date_value) and join_date_value > today_datetime:
                data['join_date'].values[column_index] = pd.NaT
            elif not pd.isna(DOB_value) and DOB_value > today_datetime:
                data['date_of_birth'].values[column_index] = pd.NaT
            elif join_date_value < DOB_value:
                data['join_date'].values[column_index] = False
            else:
                pass

        # Use boolean indexing to remove rows where 'join_date' is False
        data = data[data['join_date'] != False]

        data.dropna(subset= ['date_of_birth', 'join_date'], axis=0, how='any', inplace=True)
        data.loc[~data['phone_number'].str.match(self.regex_expression), 'phone_number'] = np.nan
        data.dropna(axis=0, how='any', inplace=True)

        return data





##################################v2 10964
    def clean_user_data(self, data):
        # makes data all lower case
        columns_to_lower = ['first_name', 'last_name', 'company', 'email_address', 'address', 'country', 'country_code', 'phone_number', 'join_date', 'user_uuid']
        data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
        # removing nulls
        data_columns = ['index', 'first_name', 'last_name', 'date_of_birth', 'company', 'email_address', 'address', 'country', 'country_code', 'phone_number', 'join_date', 'user_uuid']
        data[data_columns] = data[data_columns].replace(['', 'nan', 'null', 'none'], np.nan)

        data.dropna(axis = 0, how='any', inplace=True)
        # cleaning dates
        data['date_of_birth'] = pd.to_datetime(data['date_of_birth'], errors='coerce')
        data['join_date'] = pd.to_datetime(data['join_date'], errors='coerce')
        ## dates that are not possible join_date cant be before date_of_birth. join-date and birth_date cant be before the current date
        # for column_index in range(len(data)):
        #     if data['join_date'].values[column_index] < data['date_of_birth'].values[column_index]:
        #         data['join_date'].values[column_index] = pd.NaT
        #     else:
        #         pass
        today_datetime = pd.to_datetime(date.today())



        data = data[~(data['join_date'] < data['date_of_birth'])]

        # Remove rows where dates are after the current date
        current_date = date.today()
        data = data[~(data['date_of_birth'] > today_datetime)]
        data = data[~(data['join_date'] > today_datetime)]

        data.dropna(subset= ['date_of_birth', 'join_date'], axis=0, how='any', inplace=True)
        data.loc[~data['phone_number'].str.match(self.regex_expression), 'phone_number'] = np.nan
        data.dropna(axis=0, how='any', inplace=True)

        return data
#########################################v3 10964
    regex_expression = r'^(?:(?:\(?(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?(?:\(?0\)?[\s-]?)?)|(?:\(?0))(?:(?:\d{5}\)?[\s-]?\d{4,5})|(?:\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3}))|(?:\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4})|(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}))(?:[\s-]?(?:x|ext\.?|\#)\d{3,4})?$'

    def clean_user_data(self, data):
        # makes data all lower case
        columns_to_lower = ['first_name', 'last_name', 'company', 'email_address', 'address', 'country', 'country_code', 'phone_number', 'join_date', 'user_uuid']
        data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
        # removing nulls
        data_columns = ['index', 'first_name', 'last_name', 'date_of_birth', 'company', 'email_address', 'address', 'country', 'country_code', 'phone_number', 'join_date', 'user_uuid']
        data[data_columns] = data[data_columns].replace(['', 'nan', 'null', 'none'], np.nan)

        data.dropna(axis = 0, how='any', inplace=True)
        # cleaning dates
        data['date_of_birth'] = pd.to_datetime(data['date_of_birth'], errors='coerce')
        data['join_date'] = pd.to_datetime(data['join_date'], errors='coerce')
        ## dates that are not possible join_date cant be before date_of_birth. join-date and birth_date cant be before the current date
        # for column_index in range(len(data)):
        #     if data['join_date'].values[column_index] < data['date_of_birth'].values[column_index]:
        #         data['join_date'].values[column_index] = pd.NaT
        #     else:
        #         pass
        today_datetime = pd.to_datetime(date.today())

        # Use boolean indexing to filter rows based on conditions
        condition1 = ~((~data['join_date'].isna()) & (data['join_date'] > today_datetime))
        condition2 = ~((~data['date_of_birth'].isna()) & (data['date_of_birth'] > today_datetime))
        condition3 = ~((~data['date_of_birth'].isna()) & (~data['join_date'].isna()) & (data['join_date'] < data['date_of_birth']))

        data = data[condition1 & condition2 & condition3]

        data.dropna(subset=['date_of_birth', 'join_date'], axis=0, how='any', inplace=True)

    
        data.loc[~data['phone_number'].str.match(self.regex_expression), 'phone_number'] = np.nan
        data.dropna(axis=0, how='any', inplace=True)

        return data

##########################################v4 10964
    regex_expression = r'^(?:(?:\(?(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?(?:\(?0\)?[\s-]?)?)|(?:\(?0))(?:(?:\d{5}\)?[\s-]?\d{4,5})|(?:\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3}))|(?:\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4})|(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}))(?:[\s-]?(?:x|ext\.?|\#)\d{3,4})?$'

    def clean_user_data(self, data):
        # makes data all lower case
        columns_to_lower = ['first_name', 'last_name', 'company', 'email_address', 'address', 'country', 'country_code', 'phone_number', 'join_date', 'user_uuid']
        data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
        # removing nulls
        data_columns = ['index', 'first_name', 'last_name', 'date_of_birth', 'company', 'email_address', 'address', 'country', 'country_code', 'phone_number', 'join_date', 'user_uuid']
        data[data_columns] = data[data_columns].replace(['', 'nan', 'null', 'none'], np.nan)

        data.dropna(axis = 0, how='any', inplace=True)
        # cleaning dates
        data['date_of_birth'] = pd.to_datetime(data['date_of_birth'], errors='coerce')
        data['join_date'] = pd.to_datetime(data['join_date'], errors='coerce')
        ## dates that are not possible join_date cant be before date_of_birth. join-date and birth_date cant be before the current date
        # for column_index in range(len(data)):
        #     if data['join_date'].values[column_index] < data['date_of_birth'].values[column_index]:
        #         data['join_date'].values[column_index] = pd.NaT
        #     else:
        #         pass
        today_datetime = pd.to_datetime(date.today())

        # Use boolean indexing to filter rows based on conditions
        data = data[~((~data['join_date'].isna()) & (data['join_date'] > today_datetime))]
        data = data[~((~data['date_of_birth'].isna()) & (data['date_of_birth'] > today_datetime))]
        data = data[~((~data['date_of_birth'].isna()) & (~data['join_date'].isna()) & (data['join_date'] < data['date_of_birth']))]

        # data = data[condition1 & condition2 & condition3]

        data.dropna(subset=['date_of_birth', 'join_date'], axis=0, how='any', inplace=True)

    
        data.loc[~data['phone_number'].str.match(self.regex_expression), 'phone_number'] = np.nan
        data.dropna(axis=0, how='any', inplace=True)

        return data





































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

    def clean_user_data(self, data):
        # makes data all lower case
        columns_to_lower = ['first_name', 'last_name', 'company', 'email_address', 'address', 'country', 'country_code', 'phone_number', 'join_date', 'user_uuid']
        data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
        # removing nulls
        data_columns = ['index', 'first_name', 'last_name', 'date_of_birth', 'company', 'email_address', 'address', 'country', 'country_code', 'phone_number', 'join_date', 'user_uuid']
        data[data_columns] = data[data_columns].replace(['', 'nan', 'null', 'none'], np.nan)

        data.dropna(axis = 0, how='any', inplace=True)
        # cleaning dates
        data['date_of_birth'] = pd.to_datetime(data['date_of_birth'], errors='coerce')
        data['join_date'] = pd.to_datetime(data['join_date'], errors='coerce')
        ## dates that are not possible join_date cant be before date_of_birth. join-date and birth_date cant be before the current date
        # for column_index in range(len(data)):
        #     if data['join_date'].values[column_index] < data['date_of_birth'].values[column_index]:
        #         data['join_date'].values[column_index] = pd.NaT
        #     else:
        #         pass
        today_datetime = pd.to_datetime(date.today())

        # Use boolean indexing to filter rows based on conditions
        data = data[~((~data['join_date'].isna()) & (data['join_date'] > today_datetime))]
        data = data[~((~data['date_of_birth'].isna()) & (data['date_of_birth'] > today_datetime))]
        data = data[~((~data['date_of_birth'].isna()) & (~data['join_date'].isna()) & (data['join_date'] < data['date_of_birth']))]
    
        # data = data[condition1 & condition2 & condition3]

        data.dropna(subset=['date_of_birth', 'join_date'], axis=0, how='any', inplace=True)

    
        data.loc[~data['phone_number'].str.match(self.regex_expression), 'phone_number'] = np.nan
        data.dropna(axis=0, how='any', inplace=True)

        return data


    # def clean_card_data(self, data):
    #     # makes data all lower case
    #     columns_to_lower = ['card_number', 'expiry_date', 'card_provider', 'date_payment_confirmed']
    #     data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
    #     # removing nulls
    #     data_columns = ['card_number', 'expiry_date', 'card_provider', 'date_payment_confirmed']
    #     data[data_columns] = data[data_columns].replace(['', 'nan', 'null', 'none'], np.nan)

    #     data.dropna(axis = 0, how='any', inplace=True)

    #     # cleaning dates
    #     data['expiry_date'] = pd.to_datetime(data['expiry_date'], format='%m/%y', errors='coerce')
    #     data['date_payment_confirmed'] = pd.to_datetime(data['date_payment_confirmed'], errors='coerce')

    #     today_datetime = pd.to_datetime(date.today())

    #     data = data[~((~data['date_payment_confirmed'].isna()) & (data['date_payment_confirmed'] > today_datetime))]

    #     # checking card_numbers
    #     for card_index in range(len(data)):
    #         if str(data['card_number'].values[card_index]).isnumeric() == False:
    #             data['card_number'].values[card_index] = False
    #         else:
    #             pass
        
    #     data = data[~(data['card_number'] == False)]

    #     data.dropna(axis = 0, how='any', inplace = True)

    #     return data
    


    def called_clean_store_data(self, data):
        #droping columns
        data.drop(columns = 'lat', inplace=True)
        # making everything lowercase
        columns_to_lower = ['address', 'longitude', 'locality', 'store_code','staff_numbers', 'opening_date', 'store_type', 'latitude','country_code', 'continent']
        data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
        # removing nulls
        data_columns = ['index', 'address', 'longitude', 'locality', 'store_code','staff_numbers', 'opening_date', 'store_type', 'latitude','country_code', 'continent']
        data[data_columns] = data[data_columns].replace(['', 'nan', 'null', 'none'], np.nan)

        data.dropna(axis = 0, how='any', inplace=True)
        # coreccting incorrectly spelt continents
        data['continent'].replace('eeeurope', 'europe', inplace=True)
        data['continent'].replace('eeamerica', 'america', inplace=True)

        # country code can only be 2 in legth as they are only GB, EU, US
        data = data[data['country_code'].str.len() == 2]

        # cleaning dates
        data['opening_date'] = pd.to_datetime(data['opening_date'], errors='coerce')

        today_datetime = pd.to_datetime(date.today())

        data = data[~((~data['opening_date'].isna()) & (data['opening_date'] > today_datetime))]

        # Convert columns to numeric
        data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce') # ignore if coerce not work
        data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')
        data['staff_numbers'] = pd.to_numeric(data['staff_numbers'], errors='coerce')

        return data


    def clean_products_data(self, data):
        #droping columns
        data.drop(columns = 'Unnamed: 0', inplace=True)
        # making everything lowercase
        columns_to_lower = ['product_name', 'product_price', 'weight', 'category','EAN', 'date_added', 'uuid', 'removed', 'product_code']
        data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
        # removing nulls
        data_columns = ['product_name', 'product_price', 'weight', 'category','EAN', 'date_added', 'uuid', 'removed', 'product_code']
        data[data_columns] = data[data_columns].replace(['', 'nan', 'null', 'none'], np.nan)

        data.dropna(axis = 0, how='any', inplace=True)

        # remove white spaces and punctuation
        data["weight"] = data['weight'].str.replace('[^\w\s]','')

        # converting kg,g and ml in to kg and removing their weight notation
        data['weight'] = data['weight'].apply(self.convert_to_kg)

        # cleaning uuid
        data = data[data['uuid'].str.len() == 36] # possible misake
        # data.dropna(subset=['weight'],axis=0, how='any', inplace = True) # 1807
        # data.dropna(subset=['weight'],axis=0, how='any', inplace = True) # 
        data.drop_duplicates(subset=['uuid'], inplace=True)

        data['date_added'] = pd.to_datetime(data['date_added'], errors='coerce')

        today_datetime = pd.to_datetime(date.today())

        data = data[~((~data['date_added'].isna()) & (data['date_added'] > today_datetime))]


        return data



    def convert_to_kg(self, value):
            if isinstance(value, str):
                if 'kg' in value:
                    return float(value[:-2])
                elif 'x' in value:  
                    return np.nan
                elif 'g' in value:
                    try:
                        return float(value[:-1]) / 1000.00
                    except ValueError:
                        return np.nan
                elif 'lb' in value:
                    return float(value[:-2]) / 1000.00
                else:
                    return np.nan
                
    def clean_orders_data(self,data):
        # droping columns
        data.drop(columns = 'first_name', inplace = True)
        data.drop(columns = 'last_name', inplace = True)
        data.drop(columns = '1', inplace = True)
        data.drop(columns = 'level_0', inplace = True)
        data.drop(columns = 'index', inplace =True)

        columns_to_lower = ['date_uuid', 'user_uuid', 'card_number', 'store_code', 'product_code','product_quantity']
        data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
        # removing nulls
        data_columns = ['date_uuid', 'user_uuid', 'card_number', 'store_code', 'product_code','product_quantity']
        data[data_columns] = data[data_columns].replace(['', 'nan', 'null', 'none'], np.nan)

        data.dropna(axis = 0, how='any', inplace=True)        

        return data
    

    def clean_date_details(self, data):
        # making everything lowercase
        columns_to_lower = ['timestamp', 'month', 'year', 'day', 'time_period', 'date_uuid']
        data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
        # removing nulls
        data_columns = ['timestamp', 'month', 'year', 'day', 'time_period', 'date_uuid']
        data[data_columns] = data[data_columns].replace(['', 'nan', 'null', 'none'], np.nan)

        data.dropna(axis=0, how='any', inplace=True)


        data = data[data['date_uuid'].str.len() == 36] 

        return data










        




    def clean_card_data(self, pdf_data):
        columns_to_lower = ['card_provider']
        pdf_data[columns_to_lower] = pdf_data[columns_to_lower].apply(lambda x: x.str.lower())
        for card_index in range(len(pdf_data)):
            if str(pdf_data['card_number'].values[card_index]).isnumeric() == False:
                pdf_data['card_number'].values[card_index] = np.nan
            else:
                pass
        # pdf_data['card_number'] = pd.to_numeric(pdf_data['card_number'], errors='coerce')
        # pdf_data.drop_duplicates(subset=['card_number'], inplace=True)
        pdf_data['date_payment_confirmed'] = pd.to_datetime(pdf_data['date_payment_confirmed'], format='%Y-%m-%d', errors='coerce')
        # pdf_data.dropna(subset=['date_payment_confirmed'], inplace=True)
        # pdf_data.reset_index(drop=True, inplace=True)        
        # pdf_data.dropna(subset=['card_number'], inplace=True)
        # pdf_data.dropna(axis=0, how='any', inplace=True)
        pdf_data.dropna(axis = 0, how='any', inplace = True)
        #show(pdf_data)

        return pdf_data

