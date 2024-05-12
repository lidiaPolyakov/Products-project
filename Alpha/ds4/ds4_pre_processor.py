import pandas as pd

class DS4PreProcessor:
    def __init__(self, df4):
        self.df4 = df4.copy()
        self.df4_dict = pd.read_csv("Alpha/datasets/dataset4 dictionary.csv")
        self.__preprocess()

    @property
    def preprocessed_df4(self):
        return self.__categorize_columns()

    def __preprocess(self):
        self.__process_binary_variables()
        self.__update_data_types()
        self.__process_numeric_to_categorical()
        self.__process_string_to_categorical()

    def __process_binary_variables(self):
        booleans = self.df4_dict[self.df4_dict['Data Type'] == 'binary']["Variable Name"]
        for boolean in booleans:
            if boolean in self.df4.columns:
                self.df4[boolean] = self.df4[boolean].astype("category")

    def __update_data_types(self):
        '''Update specific columns to integer and float types as needed'''
        if self.df4['apache_2_diagnosis'].dropna().apply(lambda x: x == int(x)).all():
            self.df4_dict.loc[self.df4_dict['Variable Name'] == "apache_2_diagnosis", 'Data Type'] = "integer"
        self.df4_dict.loc[self.df4_dict['Variable Name'].isin(["bmi", "apache_3j_diagnosis"]), 'Data Type'] = "float"

    def __process_numeric_to_categorical(self):
        '''Identify numeric columns to be converted to categorical'''
        numeric_apache_covariates = self.df4_dict[
            (self.df4_dict["Category"] == "APACHE covariate") &
            (self.df4_dict["Data Type"].isin(["numeric", "integer"]))
        ]["Variable Name"]

        for col in numeric_apache_covariates:
            if col in self.df4.columns:
                unique_counts = self.df4[col].nunique()
                if unique_counts < 100 and self.df4[col].dropna().apply(float.is_integer).all():
                    self.df4[col] = self.df4[col].astype('category')

    def __process_string_to_categorical(self):
        '''Convert string variables to categorical'''
        string_variables = self.df4_dict[self.df4_dict['Data Type'] == 'string']["Variable Name"]
        for category in string_variables:
            if category in self.df4.columns:
                self.df4[category] = self.df4[category].astype('category')

    def __categorize_columns(self):
        '''Categorize columns into numeric, categoric, and boolean types'''

        data_types_df = self.df4.dtypes.to_frame().rename(columns={0: 'Data Type'})

        numeric = data_types_df[
            ~data_types_df.index.isin(self.df4_dict[self.df4_dict["Category"] == "identifier"]["Variable Name"].tolist()) &
            ((data_types_df["Data Type"] == "int64") | (data_types_df["Data Type"] == "float64"))
        ]

        categoric = data_types_df[
            (data_types_df["Data Type"] == "category")
        ]

        booleans = data_types_df[
            (data_types_df["Data Type"] == "bool")
        ]
        numeric_df = self.df4[numeric.index].copy()
        categoric_df = self.df4[categoric.index].copy()
        booleans_df = self.df4[booleans.index].copy()
        return pd.concat([numeric_df, categoric_df, booleans_df], axis=1, sort=False)