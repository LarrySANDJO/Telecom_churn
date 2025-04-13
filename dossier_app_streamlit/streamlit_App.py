import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import page_predictions
import page_recommandations
import home_page
from streamlit_option_menu import option_menu
from script_pipeline import *
from functions import *


# Configuration de base---------------------------------------------------

st.set_page_config(
    page_title="Dashboard Churn Télécom", 
    page_icon="📞", 
    layout="wide",
    initial_sidebar_state="expanded"
)



#-------------------------------------------- chargement css

# Chargement du css personnalise (modifications des classe et id par defaut de streamlit)

st.markdown("""
<style>

/* Variables globales */
/*:root {
    --auchan-red: #e63946;
    --auchan-red-dark: #e63946;
    --auchan-red-light: #fde8eb;
    --background-light: #f8f9fa;
    --shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
    --border-radius: 8px;
}*/



.main {
    padding: 1.5rem;
}

/* Sidebar */
.sidebar .sidebar-content {
    background-color: white;
    padding: 1rem;
}

.sidebar-logo {
    padding: 1rem;
    margin-bottom: 2rem;
}

.sidebar-logo img {
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-sm);
    transition: transform 0.3s ease;
}

.sidebar-logo img:hover {
    transform: scale(1.02);
}

.sidebar-logo .caption {
    text-align: center;
    margin-top: 0.5rem;
    color: var(--auchan-red);
    font-weight: 500;
}

/* Header */
.dashboard-header {
    background-color:#0A04AA;
    color: white;
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    box-shadow: var(--shadow-md);
}

.dashboard-header h1 {
    text-align: center;
    font-size: 3rem;
    color: white;
    font-weight: 600;
    margin: 0;
    text-transform: uppercase;
}

.dashboard-header h2 {
    text-align: center;
    font-size: 2rem;
    color: white;
    font-weight: 600;
    margin: 0;
    text-transform: uppercase;
}

.dashboard-header h3 {
    text-align: center;
    font-size: 1.5rem;
    color: white;
    font-weight: 600;
    margin: 0;
    text-transform: uppercase;
}

/* Menu de navigation */
#MainMenu {
    background-color: white;
    border-radius: var(--border-radius);
    padding: 0.5rem;
    margin-bottom: 2rem;
    box-shadow: var(--shadow-sm);
}

.nav-link {
    color: var(--auchan-red) !important;
    transition: all 0.3s ease;
    border-radius: var(--border-radius);
    margin: 0.2rem;
}

.nav-link:hover {
    background-color: var(--auchan-red-light) !important;
    transform: translateY(-1px);
}

.nav-link.active {
    background-color:#e63946;
    color: white !important;
    box-shadow: var(--shadow-sm);
}

.nav-link .icon {
    margin-right: 0.5rem;
}

/* Cards */
.custom-card {
    background: white;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-sm);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    transition: transform 0.3s ease;
}

.custom-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.card-title {
    color: var(--auchan-red);
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

/* Boutons */
.stButton > button {
    background-color: red;
    color: white;
    border: none;
    padding: 0.5rem 1.5rem;
    border-radius: 10px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background-color: red;
    transform: translateY(-1px);
    box-shadow: var(--shadow-sm);
}

/* Widgets Streamlit */
.stSelectbox, .stTextInput, .stDateInput, stMultiSelect {
    background-color: white;
    border-radius: var(--border-radius);
    padding: 0.5rem;
    margin-bottom: 1rem;
}

/* Tables */
.dataframe {
    border: none !important;
    box-shadow: var(--shadow-sm);
    border-radius: var(--border-radius);
}

.dataframe th {
    background-color: var(--auchan-red) !important;
    color: white !important;
}

.dataframe tr:hover {
    background-color: var(--auchan-red-light) !important;
}

/* Footer */
.footer {
    background-color: white;
    padding: 1.5rem;
    margin-top: 2rem;
    border-radius: var(--border-radius) var(--border-radius) 0 0;
    box-shadow: var(--shadow-sm);
    text-align: center;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
    animation: fadeIn 0.5s ease forwards;
}
/* marche pas ! */
.nav-item{
    background-color:#e63946;


}
.stSidebar{
    background-color:#ACAEB0;
}

            


/* Conteneurs personnalisés */
[data-testid="metric-container"] {
    box-shadow: 0 0 4px #686664;
    padding: 10px;
}
.plot-container > div {
    box-shadow: 0 0 2px #070505;
    padding: 5px;
    border-color: #000000;
}

/* Expander */
div[data-testid="stExpander"] div[role="button"] p {
    font-size: 1.2rem;
    color: rgb(0, 0, 0);
    border-color: #000000;
}

/* Pied de page */
.footer {
    background-color: white;
    padding: 1.5rem;
    margin-top: 2rem;
    border-radius: var(--border-radius) var(--border-radius) 0 0;
    box-shadow: var(--shadow-sm);
    text-align: center;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
    animation: fadeIn 0.5s ease forwards;
}
</style>
""", unsafe_allow_html=True)





# Logo de l'appli-------------------------------------------------------------

st.sidebar.image(
        "dossier_app_streamlit/image.png",
        caption="NIGERIA TELECOM BI"
    )

#------------------------------------

#

def display_header():
    st.markdown("""
        <div class="dashboard-header animate-fade-in">
            <h1 style = "font-weight: bold;">DASHBOARD D'ANALYSE DU "CHURN CLIENT" CHEZ NIGERIA TELECOM</h1>
        </div>
    """, unsafe_allow_html=True)

#--------------------------------------------Affichage de l'en-tête 

display_header()
    
    
    
 

# Chargement du modèle et du preprocesseur
model = joblib.load('dossier_app_streamlit/churn_model.pkl')
pipeline = joblib.load('dossier_app_streamlit/preprocessor.joblib')

# Fonction de chargement des données
@st.cache_data
def load_data(data):
    
    # # Prétraitement des données
    data_preprocessed = pipeline.transform(data)
    #data_preprocessed = data_preprocessed.drop(columns=["Customer ID"])
    
    # # Prédictions
    predictions = model.predict(data_preprocessed)
    proba_predictions = model.predict_proba(data_preprocessed)[:, 1]
    
    # # Ajout des colonnes de prédiction
    data['Churn_Prediction'] = predictions
    data['Churn_Probability'] = proba_predictions
    
    return data

# Features importances colums
def features_importances_colums(data):
    
    # # Prétraitement des données
    data_preprocessed = pipeline.transform(data)
    
    return data_preprocessed.columns

# Sidebar de filtres
def sidebar_filters(df):
    st.sidebar.markdown("""
        <div class="dashboard-header animate-fade-in">
            <h3 style = "font-weight: bold;">Filtres</h3>
        </div>
    """, unsafe_allow_html=True)
    
    
    # Style du st.multiselect
    st.markdown("""
    <style>
    /* Sélectionne les tags de sélection multiselect */
    div[data-baseweb="tag"] {
        background-color: #1d4ed8 !important;  /* bleu */
        color: white !important;              /* texte blanc */
        border: none !important;
    }

    /* Cible l'icône de fermeture (la croix) */
    div[data-baseweb="tag"] svg {
        fill: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
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
        labels=['Faible', 'Moyen', 'Élevé'],
        include_lowest=True
    )
    df['Risk_Level'] = risk_levels
    
    risk_filter = st.sidebar.multiselect(
        "Niveau de Risque", 
        options=['Faible', 'Moyen', 'Élevé'], 
        default=['Faible', 'Moyen', 'Élevé']
    )
    
    # Segments 
    # Création de la variable segment basée sur les clusters
    df['Segment'] = pd.cut(df['Total Spend in Months 1 and 2 of 2017'],
                       bins=[0, 2332.63, 9969.21, float('inf')],
                       labels=["Faible", "Moyenne", "Élevé"],
                       right=False)

# Explication des seuils:
# - "Faible": dépenses < 2332.63 (min du cluster 2)
# - "Moyenne": 2332.63 ≤ dépenses < 9969.21 (min du cluster 1)
# - "Élevé": dépenses ≥ 9969.21
    
    
    segment_filter = st.sidebar.multiselect(
        "Segment Client", 
        options=["Faible", "Moyenne", "Élevé"], 
        default=["Faible", "Moyenne", "Élevé"]
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
    data = pd.read_csv('dossier_app_streamlit/data/nig_clean.csv')
    
    churn_status = data['Churn Status']
    
    data = data.drop(columns=['Churn Status', 'Unnamed: 0'])

    df = load_data(data)
    
    df['Churn Status'] = churn_status
        
    
    # Pages de navigation---------------------------------------------------------------------
    
    page = option_menu( # voir help du package streamlit_option_menu
        menu_title=None,
        options=["Accueil & KPIs", "Prédictions",  "Recommandations"],
        icons=["house", "tags-fill", "wifi", "cpu"],
        menu_icon=None,
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important"},
            "icon": {"font-size": "1.3rem"},
            "nav-link": {"font-size": "1.2em", "text-align": "center", "margin": "0px"},
            "nav-link-selected": {"background-color": "#0A04AA"},
        }
    )
    
    st.markdown("---")

    
    
    # Donnees filtrees-------------------------------------
    
    filtered_df = sidebar_filters(df)
    
    feature_names = features_importances_colums(data)
    
    
    # Affichage des pages------------------------------------
    
    if page == "Prédictions":
        page_predictions.predictions_page(filtered_df, feature_names)
    elif page == "Recommandations":
        page_recommandations.recommendations_page(filtered_df)
    else:
        home_page.home_page(filtered_df)
    
    
    
    

if __name__ == "__main__":
    main()