import numpy as np
import pandas as pd
import datetime
from datetime import datetime
from scipy import stats
from scipy.stats import yeojohnson

class DataFrameTransform:

    '''
    Class to change the dataframe
    
    Methods:
        remove_columns(data, colmns_to_remove): removes columns from dataframe
        remove_null_rows(data, nulls_in_column): removes rows with nulls in specific columns
        fix_next_payment_dates(data, date_to_fix, previous_date): next_payment_date is fixed using last_payment_date
        replace_nulls_with_mean(data, column_name): nulls are replaced with mean.
        replace_nulls_with_median(data, column_name):nulls are replaced with median.
        replace_nulls_with_mode(data, column_name):nulls are replaced with mode.
        log_transformation(data, column_name): applies log transformationn to data.
        box_cox_transformation(data, column_name): applies Box-Cox transformation to data.
        yeo_johnson_transformation(data, column_name): applies Yeo-Johnson transformation to data.
        remove_outliers(data, column_name): removes outliers from data.
    '''

    def remove_columns(self, data, colmns_to_remove):
        '''
        Function removes selected columns from dataframe

        Args:
            data (pd.Dataframe): dataframe containing the column.
            column_name (str): name of column you want to remove.

        Return
            pd.Datrame: dataframe returned with selected column now removed
        '''
        colmns_to_remove = colmns_to_remove
        data.drop(colmns_to_remove, axis=1 ,inplace = True)
        return data
    
    def remove_null_rows(self, data, nulls_in_column):
        '''
        Function removes rows that contain nulls in sekected columns

        Args:
            data (pd.Dataframe): dataframe containing the column
            column_name (str): name of column that contains nulls.

        Return
            pd.Datrame: dataframe returned with selected rows that had nulls in selected columns now removed
        '''
        nulls_in_column = nulls_in_column
        data.dropna(subset=nulls_in_column, inplace=True, how='any')
        return data

    def fix_next_payment_dates(self, data, date_to_fix, previous_date):
        '''
        Function imputes missing data in next_payment_date column by adding one month to last_payment_date

        Args:
            data (pd.Dataframe): dataframe containing the columns.
            date_to_fix (str): name of column you want fix.
            previous_date (str): name of column to use to fix date_to_fix.

        Return:
            pd.Datrame: dataframe returned with selected rows that had nulls in selected columns replaced
        '''
        for index in data.index:
            if pd.isnull(data.at[index, date_to_fix]):
                data.at[index, date_to_fix] = data.at[index, previous_date] + pd.DateOffset(months=1)
        return data
    
    def replace_nulls_with_mean(self, data, column_name):
        '''
        Function imputes missing data in column with the mean
        
        Args:
            data (pd.Dataframe): dataframe containing the column
            column_name (str): name of the column that contains nulls that you want to replace
             
        Return:
            pd.Datrame: dataframe returned with selected rows that had nulls in selected columns replaced
        '''
        mean_value = data[column_name].mean()
        data[column_name] = data[column_name].fillna(mean_value)
        return data
    
    def replace_nulls_with_median(self, data, column_name):
        '''
        Function imputes missing data in column with the median
        
        Args:
            data (pd.Dataframe): dataframe containing the column
            column_name (str): name of the column that contains nulls that you want to replace
        
        Return:
            pd.Datrame: dataframe returned with selected rows that had nulls in selected columns replaced
        '''
        data[column_name] = data[column_name].fillna(data[column_name].median())
        return data
    
    def replace_nulls_with_mode(self, data, column_name):
        '''
        Function imputes missing data in column with the mode
        
        Args:
            data (pd.Dataframe): dataframe containing the column
            column_name (str): name of the column that contains nulls that you want to replace
        
        Return:
            pd.Datrame: dataframe returned with selected rows that had nulls in selected columns replaced
        '''
        mode = data[column_name].mode()
        # Select the first mode value if multiple modes exist
        mode_value = mode[0] if not mode.empty else None
        data[column_name] = data[column_name].fillna(mode_value)
        return data

    def log_transformation(self,data, column_name):
        '''
        Function applies log transformation on column.
        
        Args:
            data (pd.Dataframe): dataframe containing the column.
            column_name (str): name of the column that you want to change.
        
        Return:
            pd.Datfarame: dataframe with log transformed column returned
        '''
        data[column_name] = data[column_name].map(lambda i: np.log(i) if i > 0 else 0)
        return data
    
    def box_cox_transformation(self, data, column_name):
        '''
        Function applies Box-Cox transformation on column.
        
        Args:
            data (pd.Dataframe): dataframe containing the column.
            column_name (str): name of the column that you want to change.
        
        Return:
            pd.Datfarame: dataframe with Box-Cox transformed column returned
        '''
        boxcox_data = stats.boxcox(data[column_name])# transformed_data, optimal_lambda= stats.boxcox(data[column_name])
        data[column_name] = pd.Series(boxcox_data[0])# boxcox_data[0] transformed_data

        return data
    
    def yeo_johnson_transformation(self, data, column_name):
        '''
        Function applies Yeo-Johnson transformation on column.
        
        Args:
            data (pd.Dataframe): dataframe containing the column.
            column_name (str): name of the column that you want to change.
        
        Return:
            pd.Datfarame: dataframe with Yeo-Johnson transformed column returned
        '''
        yj_data = data[column_name]
        yj_data = stats.yeojohnson(yj_data)# transformed_data, optimal_lambda= stats.yeojohnson(data[column_name])
        data[column_name] = pd.Series(yj_data[0])
        return data
    
    def remove_outliers(self, data, column_name):
        '''
        Function removes ouliers using their z-score. Data that has a z-zscore below -3 or grater that 3 are removed
        
        Args: 
            data (pd.Dataframe): dataframe containing the column.
            column_name (str): name of the column that you want to remove outliers from
        
        Return:
            pd.Dataframe: Dataframe that has outliers in the chossen column removed
        '''
        cloumn_mean = np.mean(data[column_name])
        column_std = np.std(data[column_name])
        z_score = (data[column_name] - cloumn_mean) / column_std
        data['z_score'] = z_score
        mask = (data['z_score'] > -3) & (data['z_score'] < 3)
        data = data[mask]

        return data

     