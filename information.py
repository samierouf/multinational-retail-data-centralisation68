import pandas as pd
from dataframe_transformtion import DataFrameTransform
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
dftrans = DataFrameTransform()


class DataFrameInfo:
    '''
    A class for getting infomation about the dataframe
    
    Method:
        is_data_skew(data, column_name): computes skew of data.
        describe_columns_types(data): returns dataframe of the columns and their data type.
        describe_data(data): descriptive statistics of the data.
        count_distinct_values(data): counts the distinct values in the columns.
        print_shape(data): prints shape of dataframe.
        generate_null_counts(data): creates a dataframe on the null count and their percentage representation.
        describe_data_type(data): dataframe containg th datat types of the columns.
        extract_statistics(data): dataframe containg the median, mean and standard deviation of the data.
        count_distinct(data): dataframe containg counts the distinct values in the columns
        compute_vif(data, considered_features): computes the vif of each column.

    '''

    def is_data_skew(self, data, column_name):
        '''
        Fucntion xomputes the skew of data in the column
        
        Args:
            data (pd.Dataframe): dataframe containing the column.
            column_name (str): name of the column that you want inspect the skew of.
        
        Return:
            str: the skew of {column_name} is : {skew}
        '''
        skew = data[column_name].skew()
        return f'the skew of {column_name} is : {skew}'
      
    def describe_columns_types(self, data):
        '''
        Function that returns the information of the data
        
        Args:
            data (pd.dataframe/series): data that you want infomation on
        
        Return:
            Column info
        '''
        return data.info()

    def describe_data(self, data):
        '''
        Function to generate descriptive statistics of the input data.

        Args:
            data (pd.DataFrame/pd.Series): The data to describe.

        Returns:
            pd.DataFrame: A DataFrame containing descriptive statistics. For each numeric column, statistics include count, mean, standard deviation, minimum, 25th percentile, median, 75th percentile, and maximum. For categorical columns, statistics include count, unique, top, and frequency.
        '''
        return data.describe(include = 'all')

    def count_distinct_values(self, data):
        '''
        Function to count the number of distinct values in each column of the input data.

        Args:
            data (pd.DataFrame): The data for which to count distinct values.

        Returns:
            pd.DataFrame: A DataFrame containing the count of distinct values for each column.
        '''
        distinct_counts = pd.DataFrame(data.apply(lambda x: len(x.unique())))
        return distinct_counts

    def print_shape(self, data):
        '''
        Function to print the shape of the input data (number of rows and columns).

        Args:
            data (pd.DataFrame/pd.Series): The data whose shape is to be printed.

        Returns:
            tuple: A tuple containing the number of rows and columns in the data.
        '''
        return data.shape

    def generate_null_counts(self, data):
        '''
        Function to generate null counts and percentages for each column in the input data.

        Args:
            data (pd.DataFrame): The input data.

        Returns:
            pd.DataFrame: A DataFrame containing the counts and percentages of null values for each column.
        '''
        null_counts = data.isnull().sum()
        percentage_nulls = (null_counts / len(data)) * 100
        null_info = pd.DataFrame({'Null Counts': null_counts, 'Percentage Nulls': percentage_nulls})
        return null_info

    def describe_data_type(self, data):
        '''
        Function to describe the data types of columns in the input data.

        Args:
            data (pd.DataFrame): The input data.

        Returns:
            pd.DataFrame: A DataFrame containing the column names and their corresponding data types.
        '''
        df = pd.DataFrame()
        df['Column_Name'] = data.columns
        for column in data.columns:
            df.loc[df['Column_Name'] == column, 'Data_Type'] = data[column].dtype
        return df

    def extract_statistics(self, data):
        '''
        Function to extract specific statistics from the input data.

        Args:
            data (pd.DataFrame): The input data.

        Returns:
            pd.DataFrame: A DataFrame containing the median, standard deviation, and mean for each column.
        '''
        df_stats = data.describe()
        df_stats = df_stats.loc[['50%', 'std', 'mean']]
        df_stats = df_stats.transpose()
        return df_stats
    
    def count_distinct(self, data):
        '''
        Function to count the number of distinct values in each column of the input data.

        Args:
            data (pd.DataFrame): The input data.

        Returns:
            pd.DataFrame: A DataFrame containing the column names and their corresponding distinct value counts.
        '''
        df = pd.DataFrame(columns=['Column_Name', 'Distinct_Count'])
        df['Column_Name'] = data.columns
        for column in data.columns:
                df.loc[df['Column_Name'] == column, 'Distinct_Count'] = len(data[column].unique())
        return df

    def compute_vif(self, data, considered_features):
        '''
        Function to compute the Variance Inflation Factor (VIF) for the selected features in the input data.

        Args:
            data (pd.DataFrame): The input data.
            considered_features (list): List of column names to consider for computing VIF.

        Returns:
            pd.DataFrame: A DataFrame containing the variable names and their corresponding VIF values.
        '''
        X = data[considered_features]
        # the calculation of variance inflation requires a constant
        X['intercept'] = 1
        # create dataframe to store vif values
        vif = pd.DataFrame()
        vif["Variable"] = X.columns
        vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
        vif = vif[vif['Variable']!='intercept']
        return vif
    