import pandas as pd
import os
import joblib

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder

import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


class DS2XGBoostPredictor:
    def __init__(self, df2, target_column='VITAL_STATUS'):
        self.df2 = df2.copy()
        self.target_column = target_column
        self.preprocessed_data = self.preprocess_data()
    
    def preprocess_data(self):
        numeric_columns = self.df2.select_dtypes(include=['number']).columns
        categorical_columns = self.df2.select_dtypes(exclude=['number']).columns

        imputer_numeric = SimpleImputer(strategy='median')
        numeric_data_imputed = pd.DataFrame(imputer_numeric.fit_transform(self.df2[numeric_columns]), columns=numeric_columns)

        imputer_categorical = SimpleImputer(strategy='most_frequent')
        categorical_data_imputed = pd.DataFrame(imputer_categorical.fit_transform(self.df2[categorical_columns]), columns=categorical_columns)
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
    
    def train_model(self, model_path=None):
        if self.target_column not in self.preprocessed_data.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in data.")

        X = self.preprocessed_data.drop(self.target_column, axis=1)
        y = self.preprocessed_data[self.target_column]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        xgb_classifier = xgb.XGBClassifier(
            n_estimators=1,
            learning_rate=0.1,
            use_label_encoder=False,
            eval_metric='logloss',
            max_depth=6
        )
        model = xgb_classifier.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy}')
        print(classification_report(y_test, y_pred, zero_division=0))

        if model_path is not None:
            if '/' in model_path:
                os.makedirs(model_path[:model_path.rfind('/')], exist_ok=True)
            joblib.dump(model, model_path)
        else:
            self.model = model

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
        for column in self.df2.columns:
            if column not in row.columns or not row[column].isna().iloc[0]:
                continue
            categorical_columns = self.label_encoders.keys()
            numeric_columns = self.scalers.keys()
            if column in categorical_columns:
                row[column] = self.df2[column].mode().iloc[0]
            elif column in numeric_columns:
                row[column] = self.df2[column].median()
        return row

    def predict(self, row, model_path=None):
        if model_path is not None:
            model = joblib.load(model_path)
        else:
            model = self.model
        row_preprocessed = self.__impute_row(row.to_frame().transpose())
        row_preprocessed = self.__preprocess_row(row_preprocessed)
        row_preprocessed = row_preprocessed.drop(self.target_column, axis=1, errors='ignore')  # Drop target if it's included
        
        probabilities = model.predict_proba(row_preprocessed)[0]
        classes = model.classes_
        result = []
        for cls, prob in zip(classes, probabilities):
            result.append({
                'class': int(cls),
                'probability': float(prob)
            })
        return result
