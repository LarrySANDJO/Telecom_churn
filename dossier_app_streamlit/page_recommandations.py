import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page 3: Recommandations
def recommendations_page(filtered_df):
    st.title("📋 Recommandations")
    
    # Filtrer uniquement les clients actifs (Churn Status == 0)
    active_clients = filtered_df[filtered_df['Churn Status'] == 0]
    active_count = active_clients.shape[0]    
    
    # Sélections du nombre de clients à afficher
    num_risk_clients = st.slider("Nombre de clients à risque à afficher", 1, active_count, 5)
    
    st.subheader("Clients les plus à risque")
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


    num_big_spenders = st.slider("Nombre de plus gros clients à afficher", 1, active_count, 5)
    st.subheader("Les plus gros clients (dépenses)")
    gros_clients = filtered_df.sort_values(by="Total Spend in Months 1 and 2 of 2017", ascending=False).head(num_big_spenders)
    st.dataframe(gros_clients[["Customer ID", "Total Spend in Months 1 and 2 of 2017"]])