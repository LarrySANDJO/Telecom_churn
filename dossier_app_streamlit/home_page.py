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
        
        # Graphique de répartition par segment
        segment_counts = active_clients['Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Count']
        
        fig = px.pie(
            segment_counts, 
            values='Count', 
            names='Segment',
            title="Répartition par segment",
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
        
        # Graphique de contribution au churn par segment
        churn_by_segment = filtered_df.groupby('Segment')['Churn Status'].sum().reset_index()
        total_churn = churn_by_segment['Churn Status'].sum()
        churn_by_segment['Contribution'] = churn_by_segment['Churn Status'] / total_churn
        
        churn_by_segment = churn_by_segment.sort_values(by='Contribution', ascending=False)
    
        
        fig = px.bar(
            churn_by_segment,
            x='Segment',
            y='Contribution',
            title="Contribution churn par segment",
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
    
        # Calculer le taux de churn par segment
        churn_by_segment = filtered_df.groupby('Segment')['Churn Status'].mean().reset_index()
        churn_by_segment = churn_by_segment.sort_values(by='Churn Status', ascending=False)
    
        # Créer un graphique à barres avec des couleurs distinctes pour chaque segment
        churn_chart = px.bar(
            churn_by_segment,
            x='Segment',
            y='Churn Status',
            title="Churn par Segment",
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
        
        
        
    # Quatrième ligne de graphiques
    col1, col2, col3 = st.columns(3)

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

    with col3:

        # Calculer les pourcentages
        competitor_dist = filtered_df['Most Loved Competitor network in in Month 2'].value_counts(normalize=True).reset_index()
        competitor_dist.columns = ['Réseau concurrent', 'Pourcentage']
        competitor_dist['Pourcentage'] = competitor_dist['Pourcentage'] * 100

        # Trier par pourcentage décroissant
        competitor_dist = competitor_dist.sort_values('Pourcentage', ascending=False)

        # Créer le graphique avec Plotly
        fig4 = px.bar(
            competitor_dist,
            x='Réseau concurrent',
            y='Pourcentage',
            text='Pourcentage',
            title='<b>Répartition par réseau concurrent préféré </b>'
        )

        # Personnaliser le graphique
        fig4.update_layout(
            xaxis_title='',  # Supprimer le nom de l'axe des abscisses
            yaxis_title='<b>Pourcentage de clients</b>',  # Nom de l'axe des ordonnées en gras
            font=dict(
                family="Arial, sans-serif",
                size=12
            ),
            # Supprimer les marques de graduation et chiffres sur l'axe des y
            yaxis=dict(
                showticklabels=False,
                showgrid=False
            ),
            # Mettre en gras les étiquettes de l'axe x
            xaxis=dict(
                tickfont=dict(
                    family="Arial Black",
                    size=12,
                    color='black',
                )
            )
        )

        # Mettre en forme les étiquettes de pourcentage au-dessus des barres
        fig4.update_traces(
            texttemplate='<b>%{text:.1f}%</b>',  # Format avec une décimale et en gras
            textposition='outside',  # Position au-dessus de la barre
            textfont=dict(
                family='Arial, sans-serif',
                size=12,
                color='black'
            )
        )

        # Afficher le graphique
        st.plotly_chart(fig4, use_container_width=True)
        
        
        
        
    
    # Troisième ligne de graphiques
    col1, col2, col3, col4 = st.columns(4)
    
    
    with col1:
    
        # Regrouper les plaintes en catégories
        def categorize_complaints(n):
            if n == 0:
                return "Aucune"
            elif n <= 3:
                return "Faible"
            else:
                return "Élevé"
            
        filtered_df['Complaint_Category'] = filtered_df['Total Call centre complaint calls'].apply(categorize_complaints)
       
        # Préparer les données pour un diagramme à barres groupées
        complaint_churn_data = []

        # Pour chaque catégorie de plainte, calculer les pourcentages
        for complaint_cat in filtered_df['Complaint_Category'].unique():
            # Filtrer les données pour cette catégorie
            cat_data = filtered_df[filtered_df['Complaint_Category'] == complaint_cat]
            
            # Calculer le total pour cette catégorie
            total_count = len(cat_data)
            
            # Calculer le nombre et pourcentage pour chaque statut de churn
            churn_count = cat_data[cat_data['Churn Status'] == 1].shape[0]
            non_churn_count = cat_data[cat_data['Churn Status'] == 0].shape[0]
            
            churn_percentage = (churn_count / total_count * 100)
            non_churn_percentage = (non_churn_count / total_count * 100)
            
            # Ajouter les données à notre liste
            complaint_churn_data.append({
                'Complaint_Category': complaint_cat,
                'Status': 'Churn',
                'Percentage': churn_percentage,
                'Color': 'red'
            })
            
            complaint_churn_data.append({
                'Complaint_Category': complaint_cat,
                'Status': 'Non-Churn',
                'Percentage': non_churn_percentage,
                'Color': 'green'
            })

        # Convertir en DataFrame
        chart_df = pd.DataFrame(complaint_churn_data)

        # Calculer les pourcentages de churn pour trier les catégories
        churn_percentages = {}
        for complaint_cat in filtered_df['Complaint_Category'].unique():
            cat_data = filtered_df[filtered_df['Complaint_Category'] == complaint_cat]
            churn_percentages[complaint_cat] = (cat_data[cat_data['Churn Status'] == 1].shape[0] / len(cat_data) * 100)

        # Trier les catégories par pourcentage de churn décroissant
        sorted_categories = sorted(churn_percentages.keys(), key=lambda x: churn_percentages[x], reverse=True)

        # Créer un mapping de catégories pour l'ordre
        category_order = {cat: i for i, cat in enumerate(sorted_categories)}
        chart_df['Category_Order'] = chart_df['Complaint_Category'].map(category_order)

        # Trier le DataFrame
        chart_df = chart_df.sort_values(by=['Category_Order', 'Status'])

        # Créer le diagramme à barres groupées
        fig = px.bar(
            chart_df,
            x='Complaint_Category',
            y='Percentage',
            color='Status',
            barmode='group',
            text='Percentage',
            color_discrete_map={'Churn': 'red', 'Non-Churn': 'green'},
            category_orders={'Complaint_Category': sorted_categories},
            title='churn par niveau de plaintes'
        )

        # Personnalisation du graphique
        fig.update_layout(
            xaxis_title='Niveau de plaintes',
            yaxis_title='Pourcentage',
            legend_title='',
            xaxis=dict(  
                tickfont=dict(size=12, 
                    color='black', 
                    family="Arial Black"),
                title_font=dict(size=16, family="Arial", weight="bold")    
                ),
            yaxis=dict(
                showticklabels=False , 
                title_font=dict(size=16, family="Arial", weight="bold")  
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )

        # Afficher les pourcentages au-dessus des barres
        fig.update_traces(
            texttemplate='<b>%{text:.2f}%</b>',
            textposition='outside'
        )

        # Afficher le graphique
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
    
        def categorize_tenure(months):
            if months <= 12:
                return "Nouveau"
            elif months <= 36:
                return "Etabli"
            else:
                return "Fidèle"
        
        filtered_df['Tenure_Category'] = filtered_df['Customer tenure in month'].apply(categorize_tenure)
        
        # Préparer les données pour un diagramme à barres groupées
        tenure_churn_data = []

        # Pour chaque catégorie d'ancienneté, calculer les pourcentages
        for tenure_cat in filtered_df['Tenure_Category'].unique():
            # Filtrer les données pour cette catégorie
            cat_data = filtered_df[filtered_df['Tenure_Category'] == tenure_cat]
            
            # Calculer le total pour cette catégorie
            total_count = len(cat_data)
            
            # Calculer le nombre et pourcentage pour chaque statut de churn
            churn_count = cat_data[cat_data['Churn Status'] == 1].shape[0]
            non_churn_count = cat_data[cat_data['Churn Status'] == 0].shape[0]
            
            churn_percentage = (churn_count / total_count * 100)
            non_churn_percentage = (non_churn_count / total_count * 100)
            
            # Ajouter les données à notre liste
            tenure_churn_data.append({
                'Tenure_Category': tenure_cat,
                'Status': 'Churn',
                'Percentage': churn_percentage,
                'Color': 'red'
            })
            
            tenure_churn_data.append({
                'Tenure_Category': tenure_cat,
                'Status': 'Non-Churn',
                'Percentage': non_churn_percentage,
                'Color': 'green'
            })

        # Convertir en DataFrame
        chart_df = pd.DataFrame(tenure_churn_data)

        # Calculer les pourcentages de churn pour trier les catégories
        churn_percentages = {}
        for tenure_cat in filtered_df['Tenure_Category'].unique():
            cat_data = filtered_df[filtered_df['Tenure_Category'] == tenure_cat]
            churn_percentages[tenure_cat] = (cat_data[cat_data['Churn Status'] == 1].shape[0] / len(cat_data) * 100)

        # Trier les catégories par pourcentage de churn décroissant
        sorted_categories = sorted(churn_percentages.keys(), key=lambda x: churn_percentages[x], reverse=True)

        # Créer un mapping de catégories pour l'ordre
        category_order = {cat: i for i, cat in enumerate(sorted_categories)}
        chart_df['Category_Order'] = chart_df['Tenure_Category'].map(category_order)

        # Trier le DataFrame
        chart_df = chart_df.sort_values(by=['Category_Order', 'Status'])

        # Créer le diagramme à barres groupées
        fig = px.bar(
            chart_df,
            x='Tenure_Category',
            y='Percentage',
            color='Status',
            barmode='group',
            text='Percentage',
            color_discrete_map={'Churn': 'red', 'Non-Churn': 'green'},
            category_orders={'Tenure_Category': sorted_categories},
            title='Churn par niveau d\'ancienneté'
        )

        # Personnalisation du graphique
        fig.update_layout(
            xaxis_title='Etat d\'ancienneté',
            yaxis_title='Pourcentage',
            legend_title='',
            xaxis=dict(  
                tickfont=dict(size=12, 
                    color='black', 
                    family="Arial Black"),
                title_font=dict(size=16, family="Arial", weight="bold")     
                ),
            yaxis=dict(
                showticklabels=False , 
                title_font=dict(size=16, family="Arial", weight="bold")  
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )

        # Afficher les pourcentages au-dessus des barres
        fig.update_traces(
            texttemplate='<b>%{text:.2f}%</b>',
            textposition='outside'
        )

        # Afficher le graphique
        st.plotly_chart(fig, use_container_width=True)
        
    with col3:
        
        # Créer un dataframe qui croise Churn Status et Most Loved Competitor
        churn_competitor_df = filtered_df.groupby(['Churn Status', 'Most Loved Competitor network in in Month 2']).size().reset_index()
        churn_competitor_df.columns = ['Churn Status', 'Réseau concurrent', 'Count']

        # Calculer les pourcentages pour chaque statut de churn
        churn_totals = churn_competitor_df.groupby('Churn Status')['Count'].transform('sum')
        churn_competitor_df['Pourcentage'] = (churn_competitor_df['Count'] / churn_totals * 100).round(1)

        # Renommer les valeurs de Churn Status pour l'affichage
        churn_competitor_df['Statut'] = churn_competitor_df['Churn Status'].map({1: 'Churn', 0: 'Non-Churn'})

        # Trier par pourcentage décroissant au sein de chaque groupe
        churn_competitor_df = churn_competitor_df.sort_values(['Churn Status', 'Pourcentage'], ascending=[True, False])

        # Créer le graphique avec Plotly
        fig = px.bar(
            churn_competitor_df,
            x='Statut',
            y='Pourcentage',
            color='Réseau concurrent',
            text='Pourcentage',
            barmode='stack',
            title='<b>Répartition des réseaux concurrents préférés par statut de churn</b>'
        )

        # Personnaliser le graphique
        fig.update_layout(
            xaxis_title='<b>Statut</b>',
            yaxis_title='<b>Pourcentage (%)</b>',
            font=dict(
                family="Arial, sans-serif",
                size=12
            ),
            # Supprimer les chiffres sur l'axe des y
            yaxis=dict(
                showticklabels=False,
                showgrid=False
            ),
            # Mettre en gras les étiquettes de l'axe x
            xaxis=dict(
                tickfont=dict(
                    family='Arial Black',
                    size=12,
                    color='black'
                )
            ),
            legend_title_text='',
            # Position de la légende
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=0.97,
                xanchor='right',
                x=1
            )
        )

        # Mettre en forme les étiquettes de pourcentage sur les barres
        fig.update_traces(
            texttemplate='<b>%{text:.1f}%</b>',
            textposition='inside',
            textfont=dict(
                family='Arial, sans-serif',
                size=11,
                color='white'
            )
        )

        # Afficher le graphique
        st.plotly_chart(fig, use_container_width=True)
        
    with col4:
        #  Classement des réseaux par ordre de rentabilité
      

        # Calculer la dépense totale par type de réseau
        network_revenue = filtered_df.groupby('Network type subscription in Month 2')['Total Spend in Months 1 and 2 of 2017'].sum().reset_index()
        total_revenue = network_revenue['Total Spend in Months 1 and 2 of 2017'].sum()
        network_revenue['Pourcentage'] = (network_revenue['Total Spend in Months 1 and 2 of 2017'] / total_revenue) * 100

        # Trier par rentabilité décroissante
        network_revenue = network_revenue.sort_values('Pourcentage', ascending=False)

        # Créer le graphique avec Plotly
        fig5 = px.bar(
            network_revenue,
            x='Network type subscription in Month 2',
            y='Pourcentage',
            text='Pourcentage',
            title='<b>Répartition des dépenses par type de réseau (Mois 2)</b>'
        )

        # Personnaliser le graphique
        fig5.update_layout(
            xaxis_title='<b>Type de réseau</b>',
            yaxis_title='<b>Pourcentage de la dépense totale (%)</b>',
            font=dict(
                family="Arial, sans-serif",
                size=12
            ),
            # Supprimer les chiffres sur l'axe des y
            yaxis=dict(
                showticklabels=False,
                showgrid=False
            ),
            # Mettre en gras les étiquettes de l'axe x
            xaxis=dict(
                tickfont=dict(
                    family='Arial Black',
                    size=12,
                    color='black'
                )
            )
        )

        # Mettre en forme les étiquettes de pourcentage au-dessus des barres
        fig5.update_traces(
            texttemplate='<b>%{text:.1f}%</b>',  # Format avec une décimale et en gras
            textposition='outside',  # Position au-dessus de la barre
            textfont=dict(
                family='Arial, sans-serif',
                size=12,
                color='black'
            )
        )

        # Afficher le graphique
        st.plotly_chart(fig5, use_container_width=True)