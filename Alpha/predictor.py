import os
from abc import ABC, abstractmethod
from sklearn.metrics import classification_report
class Predictor(ABC):
    def __init__(self, preprocessor, path):
        self.path = path
        self.target_column = preprocessor.target_column
        self.model = None
        self.preprocessor = preprocessor

    def train_model(self):
        if os.path.isfile(self.path) and self.load_model(self.path) is not None:
            return

        X_train, y_train = self.preprocessor.get_train_encoded
        self.model = self.build_model(X_train, y_train)
        self.save_model(self.path)

    def evaluate_model(self):
        if self.path is not None:
            self.model = self.load_model(self.path)
        X_test, y_test = self.preprocessor.get_test_encoded
        y_pred = self.model.predict(X_test)
        y_pred = (y_pred > 0.5).astype(int)
        report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
        report['name'] = self.__class__.__name__
        return report

    def predict(self, row):
        """
        Load the model if a path is provided, preprocess the row, and predict using the model.
        """
        if self.path is not None and os.path.isfile(self.path):
            model = self.load_model(self.path)
        else:
            model = self.model
        row_preprocessed = self.preprocessor.impute_row(row.to_frame().transpose())
        row_preprocessed = self.preprocessor.preprocess_row(row_preprocessed)
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
