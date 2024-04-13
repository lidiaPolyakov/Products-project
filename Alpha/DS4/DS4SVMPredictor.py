from sklearn.model_selection import train_test_split
from sklearn.svm import SVC 

from Predictor import Predictor

class DS4SVMPredictor(Predictor):
    def __init__(self, df4, target_column='hospital_death'):
        super().__init__(df4, target_column)

    def build_model(self, X, y):

        # Splitting the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initializes a support vector classifier.
        svm_model = SVC(probability=True)

        # Learns the parameters of the SVM model to best separate the data into different classes.
        svm_model.fit(X_train, y_train)

        return svm_model, X_test, y_test

    def predict(self, row, model_path=None):
        return super().predict(row, model_path)
