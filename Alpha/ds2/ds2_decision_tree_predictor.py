import os
import joblib

from sklearn.tree import DecisionTreeClassifier

from predictor import Predictor

class DS2DecisionTreePredictor(Predictor):
    def __init__(self, preprocessor, path):
        super().__init__(preprocessor, path)

    def build_model(self, X_train, y_train):
        clf = DecisionTreeClassifier(random_state=42)
        model = clf.fit(X_train, y_train)
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
    
