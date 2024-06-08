import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from abc import ABC, abstractmethod

class Preprocessor(ABC):
    def __init__(self, dataframe, target_column, test_size=0.2):
        self.df = dataframe.copy()
        self.target_column = target_column
        self.label_encoders = {}
        self.scalers = {}
        
        if self.target_column not in self.df.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in data.")
        
        numeric_columns = self.df.select_dtypes(include=['number']).columns
        categorical_columns = self.df.select_dtypes(exclude=['number']).columns

        imputer_numeric = SimpleImputer(strategy='median')
        numeric_data_imputed = pd.DataFrame(imputer_numeric.fit_transform(self.df[numeric_columns]), columns=numeric_columns)

        imputer_categorical = SimpleImputer(strategy='most_frequent')
        categorical_data_imputed = pd.DataFrame(imputer_categorical.fit_transform(self.df[categorical_columns]), columns=categorical_columns)

        try:
            categorical_data_imputed[self.target_column] = pd.to_numeric(categorical_data_imputed[self.target_column], errors='raise').astype('int')
        except ValueError:
            categorical_data_imputed[self.target_column] = categorical_data_imputed[self.target_column].astype('category')

        self.__preprocessed_data = pd.concat([numeric_data_imputed, categorical_data_imputed], axis=1)

        X = self.__preprocessed_data.drop(self.target_column, axis=1)
        y = self.__preprocessed_data[self.target_column]

        self.__X_train, self.__X_test, self.__y_train, self.__y_test = train_test_split(X, y, test_size=test_size, random_state=42)

        self.__X_train_encoded = self.__X_train.copy()
        self.__X_test_encoded = self.__X_test.copy()

        label_encoders = {}
        for column in categorical_columns:
            le = LabelEncoder()
            self.__preprocessed_data[column] = le.fit_transform(self.__preprocessed_data[column])
            if column in self.__X_train.columns:
                self.__X_train_encoded[column] = le.transform(self.__X_train[column])
            if column in self.__X_test.columns:
                self.__X_test_encoded[column] = le.transform(self.__X_test[column])
            label_encoders[column] = le
        self.label_encoders = label_encoders
        
        scalers = {}
        for column in numeric_columns:
            scaler = StandardScaler()
            self.__preprocessed_data[column] = scaler.fit_transform(self.__preprocessed_data[[column]])
            if column in self.__X_train.columns:
                self.__X_train_encoded[column] = scaler.transform(self.__X_train[[column]])
            if column in self.__X_test.columns:
                self.__X_test_encoded[column] = scaler.transform(self.__X_test[[column]])
            scalers[column] = scaler
        self.scalers = scalers
        
        self.__y_train_encoded = self.label_encoders[self.target_column].transform(self.__y_train)
        self.__y_test_encoded = self.label_encoders[self.target_column].transform(self.__y_test)

    def preprocess_row(self, row):
        """
        Helper method to preprocess a single row, using fitted encoders and scalers.
        """
        row = row.copy()
        categorical_columns = list(self.label_encoders.keys())
        numeric_columns = list(self.scalers.keys())
        columns = set(categorical_columns + numeric_columns)
        columns.discard(self.target_column)
        for column in columns:
            value = row[column]
            if pd.isna(value).iloc[0]:
                continue
            if column in categorical_columns:
                row[column] = self.label_encoders[column].transform([value.iloc[0]])
            elif column in numeric_columns:
                value_df = pd.DataFrame({column: [ float(value.iloc[0]) ]})
                row[column] = self.scalers[column].transform(value_df)[0, 0]
        X_train = self.get_train_encoded[0]
        return row.reindex(X_train.columns, axis=1, fill_value=0)

    def impute_row(self, row):
        """
        Helper method to impute missing values in a single row, based on the training dataset median or mode.
        """
        row = row.copy()
        for column in self.df.columns:
            if column not in row or pd.isna(row[column]).iloc[0]:
                if column in self.label_encoders:
                    row[column] = self.df[column].mode()[0]
                elif column in self.scalers:
                    row[column] = self.df[column].median()
        X_train = self.get_train_encoded[0]
        return row.reindex(X_train.columns, axis=1, fill_value=0)

    @property
    def get_preprocessed_data(self):
        return self.__preprocessed_data.copy()

    @property
    def get_train(self):
        return self.__X_train.copy(), self.__y_train.copy()
    
    @property
    def get_test(self):
        return self.__X_test.copy(), self.__y_test.copy()
    
    @property
    def get_train_encoded(self):
        return self.__X_train_encoded.copy(), self.__y_train_encoded.copy()
    
    @property
    def get_test_encoded(self):
        return self.__X_test_encoded.copy(), self.__y_test_encoded.copy()

    @abstractmethod
    def number_of_rows(self):
        """
        return the number of rows in the preprocessed dataset
        """
        pass