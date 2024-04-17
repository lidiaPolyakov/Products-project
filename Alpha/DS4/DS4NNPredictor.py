import joblib

from sklearn.model_selection import train_test_split

from imblearn.over_sampling import SMOTE

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import AUC, Accuracy
from tensorflow.keras.layers import LeakyReLU

from Predictor import Predictor

class DS4NNPredictor(Predictor):
    def __init__(self, df4, target_column='hospital_death'):
        super().__init__(df4, target_column)

    def build_model(self, X, y):

        # Splitting the dataset into train, validation, and test sets
        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

        # smote = SMOTE(random_state=42)
        # X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

        model = Sequential([
            Dense(128, input_shape=(X_train.shape[1],)),
            LeakyReLU(alpha=0.01),  # Try also ELU
            Dense(64),
            LeakyReLU(alpha=0.01),
            Dense(1, activation='sigmoid')
        ])

        # Compile the model
        model.compile(optimizer=Adam(learning_rate=0.5), loss='binary_crossentropy', metrics=[Accuracy(), AUC()])

        # Train the model
        model.fit(X_train, y_train, epochs=10, batch_size=50, validation_data=(X_val, y_val))

        return model, X_test, y_test

    def predict(self, row, model_path=None):

        if model_path is not None:
            model = joblib.load(model_path)
        else:
            model = self.model
        
        row_preprocessed = self.__impute_row(row.to_frame().transpose())
        row_preprocessed = self.__preprocess_row(row_preprocessed)
        row_preprocessed = row_preprocessed.drop(self.target_column, axis=1, errors='ignore')  # Drop target if it's included

        # Predict
        prediction = model.predict(row_preprocessed)
        print(prediction)


        
        result = []
        for cls, prob in zip(classes, probabilities):
            result.append({
                'class': int(cls),
                'probability': float(prob)
            })
        return result