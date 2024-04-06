import pandas as pd
import numpy as np

class DS2PreProcessor:
    def __init__(self, df2):
        self.df2 = df2.copy()
        self.__preprocess()

    @property
    def preprocessed_df2(self):
        return self.__categorize_columns()

    def __preprocess(self):
        self.__drop_unwanted_columns()
        self.__process_categorycal_columns()
        self.__convert_to_numerical()
        self.__convert_binary_to_category()

    def __drop_unwanted_columns(self):
        self.df2 = self.df2.drop(['PATIENT_ID', 'BlindedIDs', 'DC_STUDY_ID', 'MICROARRAY', 'WARNING', 'TESTTYPE'], axis=1)

    def __process_categorycal_columns(self):
        categorycal_columns = [
            "Stratagene", "SITE", "GENDER", "RACE", "ADJUVANT_CHEMO",
            "ADJUVANT_RT", "FIRST_PROGRESSION_OR_RELAPSE", "PATHOLOGIC_N_STAGE",
            "PATHOLOGIC_T_STAGE", "Histologic grade", "SMOKING_HISTORY",
            "SURGICAL_MARGINS", "VITAL_STATUS"
        ]
        for column in categorycal_columns:
            self.df2[column] = self.df2[column].astype('category')

    def __convert_to_numerical(self):
        for col in ['MTHS_TO_LAST_CLINICAL_ASSESSMENT', 'MONTHS_TO_LAST_CONTACT_OR_DEATH']:
            self.df2[col] = self.df2[col].replace('na', np.nan)
            self.df2[col] = self.df2[col].astype('float64')

    def __convert_binary_to_category(self):
        numeric_df = self.df2.select_dtypes(include=['int64', 'float64'])
        for column in numeric_df.columns:
            if len(numeric_df[column].unique()) == 2 and set(numeric_df[column].unique()) == {0, 1}:
                self.df2[column] = numeric_df[column].astype('category')
                numeric_df = numeric_df.drop(column, axis=1)

    def __categorize_columns(self):
        categorycal_df = self.df2.select_dtypes(include='category')
        numeric_df = self.df2.select_dtypes(include=['int64', 'float64'])
        return pd.concat([numeric_df, categorycal_df], axis=1, sort=False)
