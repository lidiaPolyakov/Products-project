import os
import joblib

from sklearn.svm import SVC 

from Predictor import Predictor

class DS4SVMPredictor(Predictor):
    def __init__(self, df4, target_column='hospital_death'):
        super().__init__(df4, target_column, test_size=0.2)

    def build_model(self, X_train, y_train):
        svm_model = SVC(probability=True)
        svm_model.fit(X_train, y_train)
        return svm_model

    def save_model(self, model_path):
        if model_path is None: return
        if '/' in model_path:
            os.makedirs(model_path[:model_path.rfind('/')], exist_ok=True)
        joblib.dump(self.model, model_path) 

    def load_model(self, model_path):
        if model_path is not None:
            return joblib.load(model_path)
        return self.model
