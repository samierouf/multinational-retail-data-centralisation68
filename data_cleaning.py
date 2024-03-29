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
from pandasgui import show
connector = DatabaseConnector()
extractor = DataExtractor()

class DataCleaning:
    """
    A class for cleaning and preprocessing various data sources.

    Attributes:
        regex_expression (str): Regular expression pattern for validating phone numbers.

    Methods:
        __init__(self) -> None: Initializes the DataCleaning class.
        clean_user_data(data): Cleans and preprocesses user data.
        clean_card_data(pdf_data): Cleans and preprocesses card data.
        called_clean_store_data(data): Cleans and preprocesses store data.
        clean_products_data(data): Cleans and preprocesses products data.
        clean_orders_data(data): Cleans and preprocesses orders data.
        clean_date_details(data): Cleans and preprocesses date details data.
        correct_join_dates(pdf_data): Manually corrects join dates in a DataFrame.
        correct_payment_dates(data): Manually corrects payment dates in a DataFrame.
        convert_to_kg(value): Converts weight values to kilograms.
        math_in_weight(data): Performs mathematical operations on weight values.
        remove_stray_fullstop(weight): Removes stray full stops from weight values.
        valid_category(data): Filters rows based on valid category values.
        convert_weight(data): Converts and updates weight values in a DataFrame.
    """

    def __init__(self) -> None:
        
        self.regex_expression = r'^(?:(?:\(?(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?(?:\(?0\)?[\s-]?)?)|(?:\(?0))(?:(?:\d{5}\)?[\s-]?\d{4,5})|(?:\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3}))|(?:\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4})|(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}))(?:[\s-]?(?:x|ext\.?|\#)\d{3,4})?$'




    def clean_user_data(self, data):
        """
        this function cleans and preprocesses the user data.

        Args:
            data (pd.DataFrame): Input DataFrame containing user data.

        Returns:
            pd.DataFrame: Cleaned and preprocessed user data.
        """
        # correct dates
        data = self.correct_join_dates(data)
        data['date_of_birth'] = pd.to_datetime(data['date_of_birth'], errors='coerce')
        data['join_date'] = pd.to_datetime(data['join_date'], format='%Y-%m-%d', errors='coerce')
        data.dropna(subset=['join_date'], inplace=True)
        # clean other data
        data.loc[~data['phone_number'].str.match(self.regex_expression), 'phone_number'] = np.nan
        data = data[data['user_uuid'].str.len() == 36]

        return data   

    def clean_card_data(self, pdf_data):
        """
        this function cleans and preprocesses the card data.

        Args:
            data (pd.DataFrame): Input DataFrame containing the card data.

        Returns:
            pd.DataFrame: cleaned and preprocessed card data.
        """
        
        # making everything lowercase
        columns_to_lower = ['card_provider']
        pdf_data[columns_to_lower] = pdf_data[columns_to_lower].apply(lambda x: x.str.lower())

        # Replace '?' in card_number
        # pdf_data['card_number'] = pdf_data['card_number'].apply(lambda x: re.sub(r'\?', '', str(x)))
        pdf_data['card_number'] = pdf_data['card_number'].astype(str).str.replace(r'\?','', regex = True)

        # Check if the values in card_number are numeric, if not assign NaN
        for card_index in range(len(pdf_data)):
            if str(pdf_data['card_number'].values[card_index]).isnumeric() == False:
                pdf_data['card_number'].values[card_index] = np.nan
            else:
                pass
        # Drop rows with NaN values in card_number
        pdf_data.dropna(subset=['card_number'], axis=0, how='any', inplace=True)

        pdf_data = self.correct_payment_dates(pdf_data)
        # Convert date_payment_confirmed to the correct format
        pdf_data['date_payment_confirmed'] = pd.to_datetime(pdf_data['date_payment_confirmed'], errors='coerce')


        # Drop rows with NaN values in date_payment_confirmed
        pdf_data.dropna(subset=['date_payment_confirmed'], axis=0, how='any', inplace=True)

        return pdf_data

    def called_clean_store_data(self, data):
        """
        Cleans and preprocesses store data.

        Args:
            data (pd.DataFrame): Input DataFrame containing store data.

        Returns:
            pd.DataFrame: Cleaned and preprocessed store data.
        """
        #droping columns
        data.drop(columns = 'lat', inplace=True)
        # making everything lowercase
        columns_to_lower = ['address', 'longitude', 'locality','staff_numbers', 'opening_date', 'store_type', 'latitude','country_code', 'continent']
        data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())

        data['continent'].replace('eeeurope', 'europe', inplace=True)
        data['continent'].replace('eeamerica', 'america', inplace=True)

        # country code can only be 2 in legth as they are only GB, EU, US
        data = data[data['country_code'].str.len() == 2]
        # data['staff_numbers'] = data['staff_numbers'].astype(str).str.replace(r'\D', '')
        data.loc[:, 'staff_numbers'] = data['staff_numbers'].astype(str).str.replace(r'\D', '')

        # cleaning dates
        data.loc[:, 'opening_date'] = pd.to_datetime(data['opening_date'], errors='coerce')

        today_datetime = pd.to_datetime(date.today())

        data = data[~((~data['opening_date'].isna()) & (data['opening_date'] > today_datetime))]

        # Convert columns to numeric
        data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce') # ignore if coerce not work
        data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')
        data['staff_numbers'] = pd.to_numeric(data['staff_numbers'], errors='coerce')

        return data

    def clean_products_data(self, data):
        """
        Cleans and preprocesses products data.

        Args:
            data (pd.DataFrame): Input DataFrame containing products data.

        Returns:
            pd.DataFrame: Cleaned and preprocessed products data.
        """
        # replcing stes taht are in the wrong format
        data.loc[[307, 1217], 'date_added'] = ['2018-10-22', '2017-09-06']

        data.dropna(subset=['date_added'], axis=0, how='any', inplace=True)
        data['date_added'] = pd.to_datetime(data['date_added'], errors='ignore')
        data['weight'] = data['weight'].apply(self.remove_stray_fullstop) 
        data = self.valid_category(data) 
        data = self.convert_weight(data)
        data.loc[:, 'weight'] = pd.to_numeric(data['weight'], errors='coerce')
        
        return data
    
    def clean_orders_data(self,data):
        """
        this function cleans and preprocesses orders data.

        Args:
            pdf_data (pd.DataFrame): Input DataFrame containing orders data.

        Returns:
            pd.DataFrame: Cleaned and preprocessed orders data.
        """
        # droping columns
        data.drop(columns = 'first_name', inplace = True)
        data.drop(columns = 'last_name', inplace = True)
        data.drop(columns = '1', inplace = True)
        data.drop(columns = 'level_0', inplace = True)
        data.drop(columns = 'index', inplace =True)      

        return data

    def clean_date_details(self, data):
        """
        Cleans and preprocesses date details data.

        Args:
            pdf_data (pd.DataFrame): Input DataFrame containing date details data.

        Returns:
            pd.DataFrame: Cleaned and preprocessed date details data.
        """
        # making everything lowercase
        columns_to_lower = ['timestamp', 'month', 'year', 'day', 'time_period', 'date_uuid']
        data[columns_to_lower] = data[columns_to_lower].apply(lambda x: x.str.lower())
        # removing nulls
        data_columns = ['timestamp', 'month', 'year', 'day', 'time_period', 'date_uuid']
        data[data_columns] = data[data_columns].replace(['', 'nan', 'null', 'none'], np.nan)
        data.dropna(axis=0, how='any', inplace=True)
        # uuid is max 36 in length
        data = data[data['date_uuid'].str.len() == 36] 

        return data
    


    ##### UTILILTY functions
    @staticmethod
    def correct_join_dates(self, pdf_data):
        """
        corrects join dates in the user data.

        Args:
            pdf_data (pd.DataFrame): Input DataFrame containing 'join_date' column.

        Returns:
            pd.DataFrame: DataFrame with corrected 'join_date' values.
        """

        date_mapping = { #  dates to be corrected
            "2006 September 03": '2006-09-03',
            "2006/10/04": '2006-10-04',
            "2001 October 14": '2001-10-14',
            "1998 June 28": '1998-06-28',
            "2017/01/15": '2017-01-15',
            "2022 October 04": '2022-10-04',
            "2008/12/23": '2008-12-23',
            "2008 December 05": '2008-12-05',
            "1994 February 12": '1994-02-12',
            "2008/05/09": '2008-05-09',
            "November 1994 28": '1994-11-28',
            "February 2019 03": '2019-02-03',
            "July 2002 21": '2002-07-21',
            "May 1999 31": '1999-05-31',
            "May 1994 27": '1994-05-27',
            "2019/09/12": '2019-09-12',
            "2009/06/23": '2009-06-23',
            "2021/10/09": '2021-10-09',
            "March 2011 04": '2011-03-04',
            "December 1992 09": '1992-12-09',
            "2009/03/05": '2009-03-05',
            "1997/07/14": '1997-07-14',
            "October 2022 26": '2022-10-26'
        }

        pdf_data['join_date'] = pdf_data['join_date'].replace(date_mapping)

        return pdf_data
    
    @staticmethod
    def correct_payment_dates(self, data):
        """
        corrects payment dates in the card data.

        Args:
            data (pd.DataFrame): Input DataFrame containing column.

        Returns:
            pd.DataFrame: DataFrame with corrected values.
        """
        date_mapping = { # dates to be corrected
        "December 2021 17": '2021-12-17',
        "2005 July 01": '2005-07-01',
        "December 2000 01": '2000-12-01',
        "2008 May 11": '2008-05-11',
        "October 2000 04": '2000-10-04',
        "September 2016 04": '2016-09-04',
        "2017/05/15": '2017-05-15',
        "May 1998 09": '1998-05-09'
                        }
        
        data['date_payment_confirmed'] = data['date_payment_confirmed'].replace(date_mapping)
        data.dropna(subset=['date_payment_confirmed'], axis=0, how='any', inplace=True)

        return data

    @staticmethod
    def convert_to_kg(self, value):
        """
        converts the weight values to kg if they are not already kg and strips their units of measuerments.

        Args:
            value (str): input weight values.

        Returns:
            float or np.nan: converted weight in kg or np.nan if the conversion is not possible.
        """
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
            
    
    @staticmethod
    def remove_stray_fullstop(self, weight):
        """
        remove stray full stops from the given weight values.

        Args:
            weight (str or pd.NA): Input weight values.

        Returns:
            str : cleaned weight values.
        """
        if pd.notna(weight) and isinstance(weight, str):
            return weight.replace(' .', '')
        else:
            return weight
        

    @staticmethod
    def valid_category(self, data):# if it does not work use ## .astype(str)
        """
        checks to see if datat in category column is valid
        Args:
            pd,dataframe : input dataframe contang category column
        Returns:
            dataframe : dataframe with valid data in category column
         """
        data = data[data['category'].str.lower().isin(['homeware', 'toys-and-games', 'food-and-drink', 'pets', 'sports-and-leisure', 'health-and-beauty', 'diy'])]

        return data


    @staticmethod
    def convert_weight(self, data):
        """
         weights with 'x' in them are treated as an equation to retun a new value.

        Args:
            data (pd.DataFrame): input DataFrame containing weight column.

        Returns:
            pd.DataFrame: dataframe with processed weight values.
        """
        # Identify rows where the 'weight' column contains 'x'
        mask = data['weight'].str.contains('x', na=False)
        # Split the 'weight' column into temporary columns using 'x' as a separator
        temp_cols = data.loc[mask, 'weight'].str.split('x', expand=True)
        # Extract numeric values and convert them to numeric type
        numeric_cols = temp_cols.apply(lambda x: pd.to_numeric(x.str.extract(r'(\d+\.?\d*)', expand=False), errors='coerce'), axis=1)
        # Calculate the product of numeric values
        final_weight = numeric_cols.prod(axis=1)
        # Update the 'weight' column with the calculated values
        data.loc[mask, 'weight'] = final_weight

        return data
    
