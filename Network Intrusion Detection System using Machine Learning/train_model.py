import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
import pickle

def train_model():
    # Load your dataset
    df = pd.read_csv('C:/Users/Joy Arowoyele/Desktop/nids/IDSdataset.csv')

    # Define features and target
    features = ['flow_duration', 'Header_Length', 'Protocol Type', 'Duration', 'Rate', 
                'fin_flag_number', 'syn_flag_number', 'rst_flag_number', 'psh_flag_number', 
                'ack_flag_number', 'ece_flag_number', 'cwr_flag_number', 'ack_count', 
                'syn_count', 'fin_count', 'urg_count', 'rst_count']
    X = df[features]
    y = df['label']

    X, y = SMOTE().fit_resample(X, y)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train the model
    xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Fit the models
    xgb_model.fit(X_train_scaled, y_train)
    rf_model.fit(X_train_scaled, y_train)

    # Step 3: Create an Ensemble
    ensemble_model = VotingClassifier(estimators=[
        ('xgb', xgb_model),
        ('rf', rf_model)
    ], voting='soft')  # 'soft' for averaging probabilities, 'hard' for majority voting

    ensemble_model.fit(X_train_scaled, y_train)
    # # Save the model and scaler
    # with open('data/trained_model.pkl', 'wb') as f:
    #     pickle.dump(ensemble_model, f)
    # with open('data/scaler.pkl', 'wb') as f:
    #     pickle.dump(scaler, f)
        
    # Save the model and scaler
    with open('data/intrusion_detection_model.pkl', 'wb') as f:
        pickle.dump((ensemble_model, scaler), f)

print("Model and scaler saved to intrusion_detection_model.pkl")

if __name__ == '__main__':
    train_model()