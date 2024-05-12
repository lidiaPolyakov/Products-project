import os
import joblib

import xgboost as xgb

from predictor import Predictor

class DS2XGBoostPredictor(Predictor):
    def __init__(self, df2, path, target_column='VITAL_STATUS'):
        super().__init__(df2, path, target_column, test_size=0.3)

    def build_model(self, X_train, y_train):
        xgb_classifier = xgb.XGBClassifier(
            n_estimators=1000,
            learning_rate=0.1,
            use_label_encoder=False,
            eval_metric='logloss',
            max_depth=6
        )
        model = xgb_classifier.fit(X_train, y_train)
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
