from abc import ABC, abstractmethod
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

class Predictor(ABC):
    def __init__(self, dataframe, path, target_column, test_size):
        self.df = dataframe.copy()
        self.path = path
        self.target_column = target_column
        self.model = None
        self.label_encoders = {}
        self.scalers = {}
        self.preprocessed_data = self.__preprocess_data()
        
        X = self.preprocessed_data.drop(self.target_column, axis=1)
        y = self.preprocessed_data[self.target_column]
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    def train_model(self):
        if self.load_model(self.path) is not None:
            return

        if self.target_column not in self.preprocessed_data.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in data.")

        self.model = self.build_model(self.X_train, self.y_train)
        self.save_model(self.path)

    def evaluate_model(self):
        if self.path is not None:
            self.model = self.load_model(self.path)
        y_pred = self.model.predict(self.X_test)
        y_pred = (y_pred > 0.5).astype(int)
        return classification_report(self.y_test, y_pred, output_dict=True, zero_division=0)

    def predict(self, row):
        """
        Load the model if a path is provided, preprocess the row, and predict using the model.
        """
        if self.path is not None:
            model = self.load_model(self.path)
        else:
            model = self.model
        row_preprocessed = self.__impute_row(row.to_frame().transpose())
        row_preprocessed = self.__preprocess_row(row_preprocessed)
        row_preprocessed = row_preprocessed.drop(self.target_column, axis=1, errors='ignore')  # Drop target if it's included
        return model.predict(row_preprocessed).reshape(1)[0]

    @abstractmethod
    def build_model(self, X_train, y_train):
        """
        Abstract method for building the model, specific to each derived class.
        :param X: feature columns for training
        :param y: target column for training
        :return: model
        """
        pass

    @abstractmethod
    def save_model(self, model_path):
        """
        Abstract method for saving the model to a file.
        :param model_path: path to save the model
        """
        pass
    
    @abstractmethod
    def load_model(self, model_path):
        """
        Abstract method for loading the model from a file.
        :param model_path: path to load the model
        :return: model
        """
        pass

    def __preprocess_data(self):
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

        preprocessed_data = pd.concat([numeric_data_imputed, categorical_data_imputed], axis=1)

        label_encoders = {}
        for col in categorical_columns:
            le = LabelEncoder()
            preprocessed_data[col] = le.fit_transform(preprocessed_data[col])
            label_encoders[col] = le
        self.label_encoders = label_encoders
        
        scalers = {}
        for col in numeric_columns:
            scaler = StandardScaler()
            preprocessed_data[col] = scaler.fit_transform(preprocessed_data[[col]])
            scalers[col] = scaler
        self.scalers = scalers
        
        return preprocessed_data

    def __preprocess_row(self, row):
        """
        Helper method to preprocess a single row, using fitted encoders and scalers.
        """
        row = row.copy()
        categorical_columns = list(self.label_encoders.keys())
        numeric_columns = list(self.scalers.keys())
        columns = categorical_columns + numeric_columns
        for column in columns:
            value = row[column]
            if pd.isna(value).iloc[0]:
                continue
            if column in categorical_columns:
                row[column] = self.label_encoders[column].transform([value.iloc[0]])
            elif column in numeric_columns:
                value_df = pd.DataFrame({column: [ float(value.iloc[0]) ]})
                row[column] = self.scalers[column].transform(value_df)[0, 0]
        return row

    def __impute_row(self, row):
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
        return row
