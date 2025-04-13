import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from functions import *

# Page 3: Recommandations
def recommendations_page(filtered_df):
    st.markdown("""
            <div class="dashboard-header animate-fade-in">
                <h2 style = "text-align: center;font-weight: bold;">📋 Recommandations</h2>
            </div>
        """, unsafe_allow_html=True)
    
    
    # Filtrer uniquement les clients actifs (Churn Status == 0)
    active_clients = filtered_df[filtered_df['Churn Status'] == 0]
    active_count = active_clients.shape[0]    
    
    # Sélections du nombre de clients à afficher
    num_risk_clients = st.slider("Nombre de clients à risque à afficher", 1, active_count, 5)
    
    
    display_stylized_title("Clients les plus à risque")
    
    clients_risque = filtered_df.sort_values(by="Churn_Probability", ascending=False).head( num_risk_clients)
    clients_risque["Risque"] = clients_risque["Churn_Probability"].apply(lambda x: "Critique" if x > 0.7 else ("Élevé" if x > 0.5 else "Modéré"))

    fig_risque = px.bar(clients_risque, x="Customer ID", y="Churn_Probability", color="Risque",
                        color_discrete_map={"Critique": "red", "Élevé": "orange", "Modéré": "yellow"})
    fig_risque.update_layout(showlegend=False, xaxis_title="", yaxis_title="Probabilité de churn")
    st.plotly_chart(fig_risque, use_container_width=True)


    num_old_clients = st.slider("Nombre de clients les plus anciens à afficher", 1, active_count, 5)   
    st.subheader("Clients les plus anciens")
    clients_anciens = filtered_df.sort_values(by="Customer tenure in month", ascending=False).head(num_old_clients)
    st.dataframe(clients_anciens[["Customer ID", "Customer tenure in month"]])


    num_young_clients = st.slider("Nombre de clients les plus récents à afficher", 1, active_count, 5)   
    st.subheader("Clients les plus récents")
    clients_jeunes = filtered_df.sort_values(by="Customer tenure in month", ascending=True).head(num_old_clients)
    st.dataframe(clients_jeunes[["Customer ID", "Customer tenure in month"]])



    num_big_spenders = st.slider("Nombre de clients à forte valeur à afficher", 1, active_count, 5)
    st.subheader("Les clients à forte")
    gros_clients = filtered_df.sort_values(by="Total Spend in Months 1 and 2 of 2017", ascending=False).head(num_big_spenders)
    st.dataframe(gros_clients[["Customer ID", "Total Spend in Months 1 and 2 of 2017"]])
    
    
    num_big_spenders = st.slider("Nombre de clients à faible valeur à afficher", 1, active_count, 5)
    st.subheader("Les clients à plus faible valeur")
    faiVal_clients = filtered_df.sort_values(by="Total Spend in Months 1 and 2 of 2017", ascending=True).head(num_big_spenders)
    st.dataframe(faiVal_clients[["Customer ID", "Total Spend in Months 1 and 2 of 2017"]])
    
    
    # Créer la variable "ratio Offnet/Onnet"
    filtered_df['ratio_offnet_onnet'] = filtered_df['Total Offnet spend'] / filtered_df['Total Onnet spend'].replace(0, 1)

    # Clients avec un ratio Offnet/Onnet > 3 (triés par ordre décroissant)
    num_high_ratio_clients = st.slider("Nombre de clients avec un ratio Offnet/Onnet > 3", 1, active_count, 5)
    st.subheader("Clients avec un ratio Offnet/Onnet > 3")
    high_ratio_clients = filtered_df[filtered_df['ratio_offnet_onnet'] > 3]
    high_ratio_clients = high_ratio_clients.sort_values(by="ratio_offnet_onnet", ascending=False)
    st.dataframe(high_ratio_clients[["Customer ID", "Total Offnet spend", "Total Onnet spend", "ratio_offnet_onnet"]])

    
    # Clients avec un ratio Offnet/Onnet < 1 (triés par ordre croissant)
    num_low_ratio_clients = st.slider("Nombre de clients avec un ratio Offnet/Onnet < 1", 1, active_count, 5)
    st.subheader("Clients avec un ratio Offnet/Onnet < 1")
    low_ratio_clients = filtered_df[filtered_df['ratio_offnet_onnet'] < 1]
    low_ratio_clients = low_ratio_clients.sort_values(by="ratio_offnet_onnet", ascending=True)
    st.dataframe(low_ratio_clients[["Customer ID", "Total Offnet spend", "Total Onnet spend", "ratio_offnet_onnet"]])

    
    # cients avec migrations à risque
    # 1. Filtrer les clients avec migration 3G → 2G
    migration_3g_to_2g = active_clients[
        (active_clients['Network type subscription in Month 1'] == '3G') & 
        (active_clients['Network type subscription in Month 2'] == '2G')
    ]

    # 2. Sélecteur interactif pour le nombre de clients à afficher
    num_clients = st.slider(
        "Nombre de clients à analyser (3G → 2G)", 
        min_value=1, 
        max_value=len(migration_3g_to_2g), 
        value=min(5, len(migration_3g_to_2g))
    )

    # 3. Afficher le tableau des clients concernés
    st.subheader("Clients migrant de la 3G à la 2G")
    st.dataframe(
        migration_3g_to_2g[[
            'Customer ID', 
            'Network type subscription in Month 1', 
            'Network type subscription in Month 2',
            'Total Spend in Months 1 and 2 of 2017',
            'Churn Status'  
        ]].head(num_clients),
        height=300
    )