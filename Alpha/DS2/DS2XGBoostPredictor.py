import xgboost as xgb
from sklearn.model_selection import train_test_split

from Predictor import Predictor

class DS2XGBoostPredictor(Predictor):
    def __init__(self, df2, target_column='VITAL_STATUS'):
        super().__init__(df2, target_column)

    def build_model(self, X, y):
        
        # Splitting the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

        # Initializes a XGBoost classifier.
        xgb_classifier = xgb.XGBClassifier(
            n_estimators=1,
            learning_rate=0.1,
            use_label_encoder=False,
            eval_metric='logloss',
            max_depth=6
        )

        # Learns the parameters of the XGBoost model to best separate the data into different classes.
        model = xgb_classifier.fit(X_train, y_train)

        return model, X_test, y_test

    def predict(self, row, model_path=None):
        return super().predict(row, model_path)
