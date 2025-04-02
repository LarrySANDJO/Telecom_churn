import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

def prepare_data(df):
    """
    Prépare les données pour l'entraînement du modèle
    
    Args:
        df (pd.DataFrame): DataFrame original
    
    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    # Sélection des features
    numeric_features = [
    'network_age', 
    'Customer tenure in month', 
    'Total Spend in Months 1 and 2 of 2017',
    'Total SMS Spend', 
    'Total Data Spend', 
    'Total Data Consumption',
    'Total Unique Calls', 
    'Total Onnet spend', 
    'Total Offnet spend', 
    'Total Call centre complaint calls'
]

    categorical_features = [
    'Network type subscription in Month 1', 
    'Network type subscription in Month 2',
    'Most Loved Competitor network in in Month 1', 
    'Most Loved Competitor network in in Month 2'
]
    
    X = df[numeric_features + categorical_features]
    y = df['Churn Status']
    
    # Split des données
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test

def create_preprocessing_pipeline():
    """
    Crée le pipeline de prétraitement
    
    Returns:
        ColumnTransformer: Pipeline de prétraitement
    """
    # Sélection des features
    # Sélection des features
    numeric_features = [
    'network_age', 
    'Customer tenure in month', 
    'Total Spend in Months 1 and 2 of 2017',
    'Total SMS Spend', 
    'Total Data Spend', 
    'Total Data Consumption',
    'Total Unique Calls', 
    'Total Onnet spend', 
    'Total Offnet spend', 
    'Total Call centre complaint calls'
]

    categorical_features = [
    'Network type subscription in Month 1', 
    'Network type subscription in Month 2',
    'Most Loved Competitor network in in Month 1', 
    'Most Loved Competitor network in in Month 2'
]
    
    # Preprocessing des colonnes
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    return preprocessor

def train_model(X_train, y_train, preprocessor):
    """
    Entraîne le modèle de machine learning
    
    Args:
        X_train (pd.DataFrame): Données d'entraînement
        y_train (pd.Series): Labels d'entraînement
        preprocessor (ColumnTransformer): Pipeline de prétraitement
    
    Returns:
        Pipeline: Modèle complet
    """
    # Création du pipeline complet
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    # Entraînement
    model.fit(X_train, y_train)
    
    return model

def save_model_and_pipeline(model, preprocessor):
    """
    Sauvegarde le modèle et le pipeline
    
    Args:
        model (Pipeline): Modèle entraîné
        preprocessor (ColumnTransformer): Pipeline de prétraitement
    """
    joblib.dump(model, 'churn_model.joblib')
    joblib.dump(preprocessor, 'preprocessor.joblib')

# Exemple d'utilisation
def main():
    # Chargement des données 
    df = pd.read_csv('data/nig_data_churn_clean.csv')
    

    # Préparation des données
    X_train, X_test, y_train, y_test = prepare_data(df)
    
    # Création du pipeline de prétraitement
    preprocessor = create_preprocessing_pipeline()
    
    # Entraînement du modèle
    model = train_model(X_train, y_train, preprocessor)
    
    # Sauvegarde
    save_model_and_pipeline(model, preprocessor)

if __name__ == "__main__":
    main()



    
 