import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import page_predictions
import page_recommandations
import home_page

# Configuration de base
st.set_page_config(
    page_title="Dashboard Churn Télécom", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chargement du modèle et du preprocesseur
model = joblib.load('churn_model.joblib')
pipeline = joblib.load('preprocessor.joblib')

# Fonction de chargement des données
@st.cache_data
def load_data(data):
    
    # Prétraitement des données
    # data_preprocessed = preprocessor.transform(data)
    
    # Prédictions
    predictions = model.predict(data)
    proba_predictions = model.predict_proba(data)[:, 1]
    
    # Ajout des colonnes de prédiction
    data['Churn_Prediction'] = predictions
    data['Churn_Probability'] = proba_predictions
    
    return data

# Sidebar de filtres
def sidebar_filters(df):
    st.sidebar.title("📊 Filtres")
    
    # Filtres
    network_types = df['Network type subscription in Month 2'].unique()
    network_filter = st.sidebar.multiselect(
        "Type de Réseau", 
        options=network_types, 
        default=network_types
    )
    
    risk_levels = pd.cut(
        df['Churn_Probability'], 
        bins=[0, 0.3, 0.6, 1], 
        labels=['Faible', 'Moyen', 'Élevé']
    )
    df['Risk_Level'] = risk_levels
    
    risk_filter = st.sidebar.multiselect(
        "Niveau de Risque", 
        options=['Faible', 'Moyen', 'Élevé'], 
        default=['Faible', 'Moyen', 'Élevé']
    )
    
    # Segments 
    df['Segment'] = pd.qcut(
        df['Total Spend in Months 1 and 2 of 2017'], 
        q=4, 
        labels=['Bas', 'Moyen-Inf', 'Moyen-Sup', 'Élevé']
    )
    
    segment_filter = st.sidebar.multiselect(
        "Segment Client", 
        options=['Bas', 'Moyen-Inf', 'Moyen-sup', 'Élevé'], 
        default=['Bas', 'Moyen-Inf', 'Moyen-sup', 'Élevé']
    )

    
    # Filtrage
    filtered_df = df[
        (df['Network type subscription in Month 2'].isin(network_filter)) &
        (df['Risk_Level'].isin(risk_filter)) &
        (df['Segment'].isin(segment_filter))
    ]
    
    # Nombre de clients sélectionnés
    st.sidebar.metric("Clients sélectionnés", filtered_df.shape[0])
    
    return filtered_df


# Main
def main():

    # chargement et traitement de données
    data = pd.read_csv('data/nig_clean.csv')

    df = load_data(data)
    
    # Ajout d'un style CSS pour personnaliser la barre de navigation
    st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3498db;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Création de la barre de navigation avec st.tabs
    tabs = st.tabs(["📊 Accueil & KPIs", "🔮 Prédictions", "📋 Recommandations"])
    
    # Filtres 
    filtered_df = sidebar_filters(df)
    
    # Affichage du contenu en fonction de l'onglet sélectionné
    with tabs[0]:
        home_page.home_page(filtered_df)
    
    with tabs[1]:
        page_predictions.predictions_page(filtered_df)
    
    with tabs[2]:
        page_recommandations.recommendations_page(filtered_df)

if __name__ == "__main__":
    main()