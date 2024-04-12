import pandas as pd
import os
import joblib
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.svm import SVC 

class DS4SVMPredictor:
    def __init__(self, df4, target_column='hospital_death'):
        self.df4 = df4.copy()
        self.target_column = target_column
        self.preprocessed_data = self.preprocess_data()

    def preprocess_data(self):
        numeric_columns = self.df4.select_dtypes(include=['number']).columns
        categorical_columns = self.df4.select_dtypes(exclude=['number']).columns

        numeric_data = self.df4[numeric_columns]
        imputer_numeric = SimpleImputer(strategy='median') # Median strategy to impute missing values in numeric columns.
        numeric_data_imputed = pd.DataFrame(imputer_numeric.fit_transform(numeric_data), columns=numeric_columns)

        categorical_data = self.df4[categorical_columns]
        imputer_categorical = SimpleImputer(strategy='most_frequent')
        categorical_data_imputed = pd.DataFrame(imputer_categorical.fit_transform(categorical_data), columns=categorical_columns)
        categorical_data_imputed[self.target_column] = categorical_data_imputed[self.target_column].astype('int')

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

    def train_model(self, model_path=None):
        X = self.preprocessed_data.drop("hospital_death", axis=1)  # Features
        y = self.preprocessed_data["hospital_death"]  # Target variable

        # Splitting the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Displaying the shapes of the train and test sets
        X_train.shape, X_test.shape, y_train.shape, y_test.shape

        svm_model = SVC(probability=True) #  Initializes a support vector classifier.
        svm_model.fit(X_train, y_train) #  Learns the parameters of the SVM model to best separate the data into different classes.

        # Uses the trained SVM model to make predictions on the test data
        y_pred = svm_model.predict(X_test)

        # Evaluating the model
        accuracy = accuracy_score(y_test, y_pred)

        print(f'Accuracy: {accuracy}')
        print(classification_report(y_test, y_pred))

        if model_path is not None:
            if '/' in model_path:
                os.makedirs(model_path[:model_path.rfind('/')], exist_ok=True)
            joblib.dump(svm_model, model_path)

    def __preprocess_row(self, row):
        row = row.copy()
        categorical_columns = list(self.label_encoders.keys())
        numeric_columns = list(self.scalers.keys())
        columns = categorical_columns + numeric_columns
        for column in columns:
            value = row[column]
            if value is None or value.isna().iloc[0]:
                continue
            if column in categorical_columns:
                row[column] = self.label_encoders[column].transform(value)
            elif column in numeric_columns:
                value_df = pd.DataFrame({column: value})
                row[column] = self.scalers[column].transform(value_df)[0, 0]
        return row
    
    def __impute_row(self, row):
        # for each column, impute the value if it's missing by the dataset's median
        row = row.copy()
        for column in self.df4.columns:
            if column not in row.columns or not row[column].isna().iloc[0]:
                continue
            categorical_columns = self.label_encoders.keys()
            numeric_columns = self.scalers.keys()
            if column in categorical_columns:
                row[column] = self.df4[column].mode().iloc[0]
            elif column in numeric_columns:
                row[column] = self.df4[column].median()
        return row

    def predict(self, row, model_path=None):
        if model_path is not None:
            model = joblib.load(model_path)
        else:
            model = self.model
        row_preprocessed = self.__impute_row(row.to_frame().transpose())
        row_preprocessed = self.__preprocess_row(row_preprocessed)
        row_preprocessed = row_preprocessed.drop(self.target_column, axis=1, errors='ignore')  # Drop target if it's included
        return model.predict(row_preprocessed)
