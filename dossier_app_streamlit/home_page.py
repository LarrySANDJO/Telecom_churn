import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page 1: Accueil & KPIs
def home_page(filtered_df):
    st.title("📊 Tableau de Bord du Churn")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Taux de Churn", f"{filtered_df['Churn_Prediction'].mean()*100:.1f}%")
    
    with col2:
        st.metric(
            "Clients à Haut Risque (>60%)", 
            f"{((filtered_df['Risk_Level'] == 'Élevé') & (filtered_df['Churn Status'] == 0)).sum()} "
            f"({((filtered_df['Risk_Level'] == 'Élevé') & (filtered_df['Churn Status'] == 0)).mean()*100:.1f}%)"
        )

    with col3:
        active_clients = filtered_df[filtered_df['Churn Status'] == 0]
    
        st.metric("Ancienneté Moyenne", f"{active_clients['Customer tenure in month'].mean():.1f} mois")
    
    with col4:
        st.metric("Taux de plaintes", f"{active_clients['Total Call centre complaint calls'].mean():.1f}%")
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Segmentation Client")
        seg_chart = px.pie(filtered_df, names='Segment', 
                           title='Répartition des Segments')
        st.plotly_chart(seg_chart, use_container_width=True)
    
    with col2:
        
        st.subheader("Churn par Segment")
    
        # Calculer le taux de churn par segment
        churn_by_segment = filtered_df.groupby('Segment')['Churn_Prediction'].mean()
    
        # Créer un graphique à barres avec des couleurs distinctes pour chaque segment
        churn_chart = px.bar(
            x=churn_by_segment.index, 
            y=churn_by_segment.values, 
            title='Taux de Churn par Segment',
            labels={'x': 'Segment', 'y': 'Taux de Churn'},  
            color=churn_by_segment.index,  # Changer les couleurs en fonction du segment
            color_discrete_map={'Élevé': 'green', 'Moyen-Haut':'blue','Moyen-Bas':'orange', 'Bas' : 'red'}  
        )
    
        # Ajouter les pourcentages au-dessus de chaque barre
        churn_chart.update_traces(texttemplate='%{y:.1%}', textposition='outside')
    
        # Supprimer les chiffres de l'axe des ordonnées (optionnel)
        churn_chart.update_layout(yaxis_showticklabels=False)
    
        # Afficher le graphique
        st.plotly_chart(churn_chart, use_container_width=True)