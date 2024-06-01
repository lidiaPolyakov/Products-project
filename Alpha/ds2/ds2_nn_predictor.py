from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, LeakyReLU
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import AUC, Accuracy
from tensorflow.keras.models import load_model

from predictor import Predictor

class DS2NNPredictor(Predictor):
    def __init__(self, preprocessor, path):
        super().__init__(preprocessor, path)

    def build_model(self, X_train, y_train):
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

        model = Sequential([
            Input(shape=(X_train.shape[1],)),
            Dense(128),
            LeakyReLU(alpha=0.01),
            Dense(64),
            LeakyReLU(alpha=0.01),
            Dense(1, activation='sigmoid')
        ])

        model.compile(optimizer=Adam(learning_rate=0.5), loss='binary_crossentropy', metrics=[Accuracy(), AUC()])
        model.fit(X_train, y_train, epochs=10, batch_size=50, validation_data=(X_val, y_val))
        return model

    def save_model(self, model_path):
        if model_path is not None:
            self.model.save(model_path)
    
    def load_model(self, model_path):
        if model_path is not None:
            return load_model(model_path)
        return self.model
