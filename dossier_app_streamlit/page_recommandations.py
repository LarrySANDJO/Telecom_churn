import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page 3: Recommandations
def recommendations_page(filtered_df):
    st.title("📋 Recommandations")
    
    # Clients à risque
    high_risk = filtered_df[filtered_df['Risk_Level'] == 'Élevé']
    st.subheader("Clients à Haut Risque")
    st.dataframe(high_risk[['Customer ID', 'Churn_Probability', 'Total Spend in Months 1 and 2 of 2017']])
