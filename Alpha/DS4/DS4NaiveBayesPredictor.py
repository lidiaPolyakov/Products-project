from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split

from Predictor import Predictor

class DS4NaiveBayesPredictor(Predictor):
    def __init__(self, df4, target_column='hospital_death'):
        super().__init__(df4, target_column)

    def build_model(self, X, y):

        # Splitting the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Initializes a Gaussian Naive Bayes classifier.
        gnb_classifier = GaussianNB()

        # Learns the parameters of the Gaussian Naive Bayes model to best separate the data into different classes.
        model = gnb_classifier.fit(X_train, y_train)

        return model, X_test, y_test

    def predict(self, row, model_path=None):
        return super().predict(row, model_path)
