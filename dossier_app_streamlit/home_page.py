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
        st.metric("Taux de Churn", f"{filtered_df['Churn Status'].mean()*100:.1f}%")

    with col2:
        st.metric("Nombre et taux d'actifs", f"{(filtered_df['Churn Status'] == 0).sum()*100}({((filtered_df['Churn Status'] == 0).sum() / filtered_df.shape[0] * 100):.1f}%)")
    
    with col3:
        active_clients = filtered_df[filtered_df['Churn Status'] == 0]
    
        st.metric("Ancienneté Moyenne", f"{active_clients['Customer tenure in month'].mean():.1f} mois")

    with col4:
        st.metric("Taux de plaintes", f"{active_clients['Total Call centre complaint calls'].mean():.1f}%")
    
   
     # Deuxième ligne de graphiques
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Répartition par segment")
        
        # Graphique de répartition par segment
        segment_counts = active_clients['Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Count']
        
        fig = px.pie(
            segment_counts, 
            values='Count', 
            names='Segment',
            color='Segment',
            color_discrete_map={
                'Élevé': 'green', 
                'Moyen-Haut': 'blue',
                'Moyen-Bas': 'orange', 
                'Bas': 'red'
            }
        )
        
        # Labels et pourcentages bien visibles à l'intérieur des secteurs
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            insidetextfont=dict(size=14, family="Arial Black")  # Texte en gras
        )
        
        # Suppression de la légende
        fig.update_layout(showlegend=False)

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Contribution churn par segment")
        
        # Graphique de contribution au churn par segment
        churn_by_segment = filtered_df.groupby('Segment')['Churn Status'].sum().reset_index()
        total_churn = churn_by_segment['Churn Status'].sum()
        churn_by_segment['Contribution'] = churn_by_segment['Churn Status'] / total_churn
        
        churn_by_segment = churn_by_segment.sort_values(by='Contribution', ascending=False)
    
        
        fig = px.bar(
            churn_by_segment,
            x='Segment',
            y='Contribution',
            color='Segment',
            color_discrete_map={
                'Élevé': 'green', 
                'Moyen-Haut': 'blue',
                'Moyen-Bas': 'orange', 
                'Bas': 'red'
            }
        )
        
        # Labels des pourcentages en gras sur les barres
        fig.update_traces(
            texttemplate='<b>%{y:.1%}</b>', 
            textposition='outside'
        )
        
        # Supprimer la légende, le nom de l'axe des abscisses et les graduations sur l'axe des ordonnées
        fig.update_layout(
            yaxis_tickformat='.0%',
            showlegend=False,  # Suppression de la légende
            xaxis=dict(
                title=None,  # Suppression du nom de l'axe des abscisses
                tickfont=dict(size=14, family="Arial Black")  # Mettre les modalités en gras
            ),
            yaxis=dict(
                title_font=dict(size=16, family='Arial', weight='bold'),  # Nom de l'axe en gras
                showticklabels=False  # Suppression des graduations de l'axe des ordonnées
            )
        )

        st.plotly_chart(fig, use_container_width=True)


    
    with col3:
        
        st.subheader("Churn par Segment")
    
        # Calculer le taux de churn par segment
        churn_by_segment = filtered_df.groupby('Segment')['Churn Status'].mean().reset_index()
        churn_by_segment = churn_by_segment.sort_values(by='Churn Status', ascending=False)
    
        # Créer un graphique à barres avec des couleurs distinctes pour chaque segment
        churn_chart = px.bar(
            churn_by_segment,
            x='Segment',
            y='Churn Status',
            color='Segment',
            color_discrete_map={
                'Élevé': 'green', 
                'Moyen-Haut': 'blue',
                'Moyen-Bas': 'orange', 
                'Bas': 'red'
            }
        )
        
        # Labels des pourcentages en gras sur les barres
        churn_chart.update_traces(
            texttemplate='<b>%{y:.1%}</b>', 
            textposition='outside'
        )
        
        # Supprimer la légende, le nom de l'axe des abscisses et les graduations sur l'axe des ordonnées
        churn_chart.update_layout(
            yaxis_tickformat='.0%',
            showlegend=False,  # Suppression de la légende
            xaxis=dict(
                title=None,  # Suppression du nom de l'axe des abscisses
                tickfont=dict(size=14, family="Arial Black")  # Mettre les modalités en gras
                ),
            yaxis=dict(
                title_font=dict(size=16, family='Arial', weight='bold'), # Nom de l'axe en gras
                showticklabels=False 
            )
        )
    
        # Afficher le graphique
        st.plotly_chart(churn_chart, use_container_width=True)
        
        
        
    # Troisième ligne de graphiques
    col1, col2 = st.columns(2)

    with col1:
        # Dépenses totales
        active_clients["Total Spend"] = (
        active_clients["Total SMS Spend"] +
        active_clients["Total Data Spend"] +
        active_clients["Total Onnet spend"] +
        active_clients["Total Offnet spend"]
        )

        # Pourcentage des services
        service_percentages = active_clients[[
        "Total SMS Spend", "Total Data Spend", "Total Onnet spend", "Total Offnet spend"
        ]].sum() / active_clients["Total Spend"].sum() * 100

        # Création du DataFrame pour le Pie Chart
        service_df = pd.DataFrame({
        "Service": ["SMS", "Data", "Appels Onnet", "Appels Offnet"],
        "Pourcentage": service_percentages.values
        })

        # Attribution des couleurs en fonction du niveau de dépenses
        color_map = {
        "Data": "green",       # Plus élevé
        "Appels Onnet": "yellow",  
        "Appels Offnet": "orange",
        "SMS": "red"           # Plus faible
        }

        #  PIE CHART (DÉPENSES PAR SERVICE)
        fig_service = px.pie(
            service_df, 
            names="Service", 
            values="Pourcentage", 
            title="Répartition des dépenses par service",
            color="Service",
            color_discrete_map=color_map
        )

        # Personnalisation des labels
        fig_service.update_traces(
            textinfo="label+percent",  # Afficher labels et % sur les secteurs
            texttemplate="<b>%{label} : %{percent:.1%}</b>",  
            insidetextfont=dict(size=14)  
        )

        # Supprimer la légende
        fig_service.update_layout(showlegend=False)
        
        st.plotly_chart(fig_service, use_container_width=True)
    
    with col2:

        # Somme des dépenses par segment, triées dans l'ordre décroissant
        segment_spend = active_clients.groupby("Segment")["Total Spend"].sum().reset_index()
        segment_spend = segment_spend.sort_values(by="Total Spend", ascending=False)

        # Ajout des pourcentages
        segment_spend["Pourcentage"] = (segment_spend["Total Spend"] / segment_spend["Total Spend"].sum()) * 100

        # Création du graphique en barres
        fig_segment = px.bar(
            segment_spend, 
            x="Segment", 
            y="Pourcentage", 
            title="Dépenses totales par segment",
            text_auto=".1f",  # Affichage des valeurs au-dessus des barres
            color_discrete_sequence=["#1f77b4"]  # Une seule couleur pour toutes les barres
        )

        # Personnalisation
        fig_segment.update_traces(
            texttemplate="<b>%{y:.2f}%</b>",  # Affichage des pourcentages en gras
            textposition="outside"
        )

        fig_segment.update_layout(
            xaxis=dict(
                title=None,  
                tickfont=dict(size=14, family="Arial Black")  
                ),
            yaxis=dict(
                showticklabels=False , 
                title_font=dict(size=16, family="Arial", weight="bold")  
            )
        )

        st.plotly_chart(fig_segment, use_container_width=True)
