import os
import joblib

from sklearn.naive_bayes import GaussianNB

from Predictor import Predictor

class DS4NaiveBayesPredictor(Predictor):
    def __init__(self, df4, target_column='hospital_death'):
        super().__init__(df4, target_column, test_size=0.3)

    def build_model(self, X_train, y_train):
        gnb_classifier = GaussianNB()
        model = gnb_classifier.fit(X_train, y_train)
        return model

    def save_model(self, model_path):
        if model_path is None: return
        if '/' in model_path:
            os.makedirs(model_path[:model_path.rfind('/')], exist_ok=True)
        joblib.dump(self.model, model_path) 

    def load_model(self, model_path):
        if model_path is not None:
            return joblib.load(model_path)
        return self.model
