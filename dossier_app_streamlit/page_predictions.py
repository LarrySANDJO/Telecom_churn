import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page 2: Prédictions
def predictions_page(filtered_df):
    st.title("🔮 Prédictions Personnalisées")
    
    # Recherche par ID client
    st.subheader("Recherche Client")
    customer_id = st.text_input("Entrez l'ID du client")
    
    if customer_id:
        client = filtered_df[filtered_df['Customer ID'] == customer_id]
        if not client.empty:
            st.write(client)
            st.metric("Probabilité de Churn", f"{client['Churn_Probability'].values[0]*100:.1f}%")
        else:
            st.warning("Client non trouvé")
