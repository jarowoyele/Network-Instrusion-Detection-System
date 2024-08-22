import pickle
import numpy as np
import pandas as pd

class IntrusionDetectionModel:
    def __init__(self, model_path):
        with open(model_path, 'rb') as f:
            self.model, self.scaler = pickle.load(f)

    def predict(self, features):
        if isinstance(features, dict):
            features = pd.DataFrame([features])
        features_scaled = self.scaler.transform(features)
        return self.model.predict(features_scaled)[0]

# Initialize the model
model = IntrusionDetectionModel('data/intrusion_detection_model.pkl')