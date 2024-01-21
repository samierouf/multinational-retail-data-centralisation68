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





