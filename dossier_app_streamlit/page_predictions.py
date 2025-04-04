import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib
import plotly.graph_objects as go

def predictions_page(filtered_df):
    st.title("🔮 prédictions de churn")
    
    # Chargement du modèle ( contient déjà le pipeline de traitement)
    model = joblib.load('churn_model.joblib')
    pipeline = joblib.load('preprocessor.joblib')
    
    # Première ligne de métriques
    col1, col2 = st.columns(2)

    # Filtrer uniquement les clients actifs (Churn Status == 0)
    active_clients = filtered_df[filtered_df['Churn Status'] == 0]
    active_count = active_clients.shape[0]
    
    with col1:
        # KPI: Taux de clients à haut risque (probabilité > 0.7)
        high_risk = active_clients[active_clients['Churn_Probability'] > 0.7].shape[0]
        st.metric("Clients à haut risque", f"{high_risk:,}({(high_risk / active_count * 100):.1f}%)")
    
    with col2:
        # KPI: Nombre d'actifs prédits
         st.metric("Nombre et taux  d'actifs", f"{(active_clients['Churn_Prediction'] == 0).sum()}({((active_clients['Churn_Prediction'] == 0).sum() / active_count * 100):.1f}%)")
        
        
    # Deuxième ligne de graphiques
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Répartition par segment")
        
        # Graphique de répartition par segment (prédite)
        active_clients_pred = active_clients[active_clients['Churn_Prediction'] == 0]
        segment_counts = active_clients_pred['Segment'].value_counts().reset_index()
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
        churn_by_segment = active_clients.groupby('Segment')['Churn_Prediction'].sum().reset_index()
        total_churn = churn_by_segment['Churn_Prediction'].sum()
        churn_by_segment['Contribution'] = churn_by_segment['Churn_Prediction'] / total_churn
        
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
        st.subheader("Facteurs influents sur le churn")
        # Importances des variables (si disponible dans le modèle)
        try:
            # Récupérer les importances des features si disponibles
            if hasattr(model['classifier'], 'feature_importances_'):
                # Liste des noms de features (à adapter selon votre modèle)
                feature_names = [
                    'Âge réseau', 'Ancienneté client', 'Dépenses totales', 
                    'Dépenses SMS', 'Dépenses data', 'Consommation data',
                    'Appels uniques', 'Dépenses Onnet', 'Dépenses Offnet', 
                    'Appels plaintes', 'Type réseau M1', 'Type réseau M2',
                    'Réseau concurrent M1', 'Réseau concurrent M2'
                ]
                
                importances = model['classifier'].feature_importances_
                
                # Ajuster selon le nombre réel
                if len(importances) < len(feature_names):
                    feature_names = feature_names[:len(importances)]
                elif len(importances) > len(feature_names):
                    importances = importances[:len(feature_names)]
                
                feature_imp = pd.DataFrame({'feature': feature_names, 'importance': importances})
                feature_imp['importance'] = feature_imp['importance'] * 100  
                feature_imp = feature_imp.sort_values('importance', ascending=False).head(10)
                
                # Graphique des importances
                fig = px.bar(
                    feature_imp, 
                    x='importance', 
                    y='feature', 
                    orientation='h',
                    text='importance'  # Afficher les valeurs d'importance sur les barres
                )
                
                # Personnalisation du graphique
                fig.update_traces(
                    texttemplate='<b>%{text:.1f}%</b>',  # Afficher les importances sur les barres avec 2 décimales
                    textposition='outside',  # Positionner les valeurs à l'intérieur des barres
                )
                
                # Mise en forme du graphique
                fig.update_layout(
                    xaxis=dict(
                        title_font=dict(size=16, family='Arial', weight='bold'),  # Nom de l'axe en gras
                        showticklabels=False  # Enlever les graduations sur l'axe des abscisses
                    ),
                    yaxis=dict(
                        title=None, 
                        tickfont=dict(size=14, family="Arial", weight="bold")  # Mettre les modalités en gras sur l'axe des ordonnées
                    ),
                    showlegend=False  # Enlever la légende
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Informations d'importance des variables non disponibles pour ce modèle")
        except Exception as e:
            st.error(f"Erreur lors de l'affichage des importances: {str(e)}")

    
    # Section de prédiction (pleine largeur)
    st.header("Prédictions")
    
    # Section des variables à entrer
    with st.expander("Veuillez saisir les données", expanded=True):
        # Organiser les variables en 3 colonnes
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Variables quantitatives - première colonne
            network_age = st.number_input(
                "Âge du réseau (mois)", 
                min_value=0, 
                max_value=240, 
                help="Durée sur le réseau (en mois)"
            )
            
            tenure = st.number_input( 
                "Ancienneté client (mois)", 
                min_value=0, 
                help="Ancienneté chez l'opérateur (mois)"
            )
            
            total_spend = st.number_input(
                "Dépenses totales (mois 1 et 2)", 
                min_value=0.0, 
                help="Total total des mois 1 et 2"
            )
            
            network_type_month1 = st.selectbox(
                "Type de réseau (mois 1)",
                options=["2G", "3G", "Other"],
                index=2,
                help="Type de réseau souscrit au mois 1"
            )
        
        with col2:
            # Variables quantitatives 
            sms_spend = st.number_input(
                "Dépenses SMS", 
                min_value=0.0, 
                help="Total des dépenses en SMS"
            )
            
            data_spend = st.number_input(
                "Dépenses data", 
                min_value=0.0, 
                help="Total des dépenses en data"
            )
            
            data_consumption = st.number_input(
                "Consommation data (Mo)", 
                min_value=0.0, 
                help="Volume total de données consommées en Mo"
            )
            
            network_type_month2 = st.selectbox(
                "Type de réseau (mois 2)",
                options=["2G", "3G", "Other"],
                index=2,
                help="Type de réseau souscrit pour le mois 2"
            )
        
        with col3:
            # Variables quantitatives 
            unique_calls = st.number_input(
                "Appels uniques", 
                min_value=0, 
                help="Nombre total d'appels uniques"
            )
            
            onnet_spend = st.number_input(
                "Dépenses Onnet", 
                min_value=0.0, 
                help="Dépenses pour appels vers le même réseau"
            )
            
            offnet_spend = st.number_input(
                "Dépenses Offnet", 
                min_value=0.0, 
                help="Dépenses pour appels vers d'autres réseaux"
            )
            
            complaint_calls = st.number_input(
                "Appels centre d'appels", 
                min_value=0, 
                help="Nombre d'appels pour des plaintes"
            )
        
        # Variables catégorielles pour les réseaux concurrents
        col1, col2 = st.columns(2)
        
        with col1:
            competitor_month1 = st.selectbox(
                "Réseau concurrent préféré (Mois 1)",
                options=["Uxaa", "Weematel", "Zintel", "Mango", "ToCall", "PQza", "Aucun"],
                index=6,
                help="Réseau concurrent le plus apprécié au mois 1"
            )
        
        with col2:
            competitor_month2 = st.selectbox(
                "Réseau concurrent préféré (Mois 2)",
                options=["Mango", "PQza", "ToCall", "Uxaa", "Weematel", "Zintel", "Aucun"],
                index=6,
                help="Réseau concurrent le plus apprécié au mois 2"
            )
    
    # Section des résultats de prédiction
    with st.container():
        st.subheader("Prédiction de churn")
        
        # Bouton pour déclencher la prédiction
        if st.button("Prédire le risque de churn", use_container_width=True):
            # Préparation des données pour la prédiction
            new_data = pd.DataFrame({
                'network_age': [network_age],
                'Customer tenure in month': [tenure],
                'Total Spend in Months 1 and 2 of 2017': [total_spend],
                'Total SMS Spend': [sms_spend],
                'Total Data Spend': [data_spend],
                'Total Data Consumption': [data_consumption],
                'Total Unique Calls': [unique_calls],
                'Total Onnet spend': [onnet_spend],
                'Total Offnet spend': [offnet_spend],
                'Total Call centre complaint calls': [complaint_calls],
                'Network type subscription in Month 1': [network_type_month1],
                'Network type subscription in Month 2': [network_type_month2],
                'Most Loved Competitor network in in Month 1': [competitor_month1],
                'Most Loved Competitor network in in Month 2': [competitor_month2]
            })
            
            # Appliquer le pipeline pour transformer les nouvelles données
            #new_data_transformed = pipeline.transform(new_data)

            
            # Faire la prédiction
            # Transformer les données avec le pipeline
            #new_data_transformed = pipeline.transform(new_data)

            # Prédire avec le modèle
            # prediction = model.predict(new_data_transformed)
            try:
                # Prédiction de la probabilité
                proba = model.predict_proba(new_data)[:, 1][0]
                prediction = model.predict(new_data)[0]
                
                # Déterminer les couleurs et messages selon la gravité
                if proba < 0.3:
                    color = "green"
                    risk_level = "✅Faible"
                elif proba < 0.5:
                    color = "orange"
                    risk_level = "📊Moyen"
                elif proba < 0.7:
                    color = "darkorange"
                    risk_level = "⚠️Élevé"
                else:
                    color = "red"
                    risk_level = "🚨Critique"
                
                # Affichage des résultats 
                col1, col2 = st.columns(2)
                
                with col1:
                    # Probabilité et niveau de risque
                    st.markdown(f"""
                    <div style="padding: 20px; border-radius: 10px; background-color: {color}25; border: 1px solid {color};">
                        <h3 style="color: {color}; margin-bottom: 10px;">Risque de churn: {risk_level}</h3>
                        <p style="font-size: 24px; font-weight: bold;">Probabilité: {proba*100:.1f}%</p>
                        <p>Statut: {"À risque" if prediction == 1 else "Stable"}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Jauge visuelle
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=proba*100,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Risque de Churn (%)"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': color},
                            'steps': [
                                {'range': [0, 30], 'color': "lightgreen"},
                                {'range': [30, 50], 'color': "lightyellow"},
                                {'range': [50, 70], 'color': "orange"},
                                {'range': [70, 100], 'color': "salmon"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 50
                            }
                        }
                    ))
                    fig.update_layout(height=250)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Recommandations basées sur le niveau de risque
                st.subheader("📢 Recommandations")
                if proba < 0.3:
                    st.success("✅Client stable. Continuez à suivre l'évolution de sa consommation.")
                elif proba < 0.5:
                    st.info("📊Risque de churn modéré. Envisagez des offres promotionnelles ciblées.")
                elif proba < 0.7:
                    st.warning("⚠️Risque de churn élevé. Contactez le client pour comprendre ses besoins.")
                else:
                    st.error("🚨Risque de churn critique. Intervention urgente requise. Proposez des offres de fidélisation personnalisées.")
                
            except Exception as e:
                st.error(f"Erreur lors de la prédiction: {str(e)}")
                st.write("Veuillez vérifier que les entrées correspondent aux attentes du modèle.")


    # Prediction dans le cas de données dans un fichier excel
    # Chargement et affichage du fichier Excel ou CSV
    uploaded_file = st.file_uploader("Importer un fichier Excel ou CSV", type=["xlsx", "csv"], key="file_upload")
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            new_data = pd.read_csv(uploaded_file)
        else:
            new_data = pd.read_excel(uploaded_file)
        
        st.write("### Aperçu des données importées")
        st.dataframe(new_data.head())
        
        # Appliquer la transformation avec le pipeline
        new_data_transformed = pipeline.transform(new_data)

        try:
            # Prédiction de la probabilité
            proba = model.predict_proba(new_data)[:, 1]
            prediction = model.predict(new_data)
            
            # Ajout des prédictions aux données
            new_data['Churn_Probability'] = proba
            new_data['Churn_Prediction'] = prediction
            
            # Boutons pour voir ou exporter les résultats
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👁 Voir les résultats"):
                    st.write("### Résultats des prédictions")
                    st.dataframe(new_data[['Customer ID', 'Churn_Probability', 'Churn_Prediction']])
            
            with col2:
                output_file = "predictions.csv"
                new_data.to_csv(output_file, index=False)
                with open(output_file, "rb") as file:
                    st.download_button(
                        label="📥 Télécharger les prédictions",
                        data=file,
                        file_name="predictions.csv",
                        mime="text/csv"
                    )
            
        except Exception as e:
            st.error(f"Erreur lors de la prédiction : {e}")