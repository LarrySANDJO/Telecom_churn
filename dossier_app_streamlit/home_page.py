import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "plotly_white"

# Page 1: Accueil & KPIs
def home_page(filtered_df):
    st.title("📊 Tableau de Bord du Churn")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Taux de Churn", f"{filtered_df['Churn Status'].mean()*100:.1f}%")

    with col2:
        st.metric("Nombre et taux d'actifs", f"{(filtered_df['Churn Status'] == 0).sum()}({((filtered_df['Churn Status'] == 0).sum() / filtered_df.shape[0] * 100):.1f}%)")
    
    with col3:
        active_clients = filtered_df[filtered_df['Churn Status'] == 0]
    
        st.metric("Ancienneté Moyenne", f"{active_clients['Customer tenure in month'].mean():.1f} mois")

    with col4:
        st.metric("Nombre et taux de plaintes", f"{(filtered_df['Total Call centre complaint calls']).sum()}({active_clients['Total Call centre complaint calls'].mean():.1f}%")
    
    
    # Les styles communs pour les graphiques en barres
    def style_plotly_figure(fig, title_text, yaxis_title_text, xaxis_title_text=''):
        fig.update_layout(
            title=dict(
                text=title_text,
                font=dict(size=20, family='Arial Black', color='black', weight='bold')
            ),
            xaxis=dict(
                title=xaxis_title_text,
                title_font=dict(
                    size=16,
                    family='Arial',
                    color='black',
                    weight='bold'
                ),
                tickfont=dict(
                    family="Arial Black",
                    size=12,
                    color='black'
                )
            ),
            yaxis=dict(
                title=yaxis_title_text,
                title_font=dict(
                    size=16,
                    family='Arial',
                    color='black',
                    weight='bold'
                ),
                showticklabels=False,  # Pas de chiffres sur l’axe Y
                showgrid=False
            ),
            font=dict(
                family="Arial Black",
                size=12,
                color='black'
            ),
            showlegend=False
        )

        fig.update_traces(
            texttemplate='<b>%{text:.1f}%</b>',
            textposition='outside',
            textfont=dict(
                family='Arial, sans-serif',
                size=12,
                color='black'
            )
        )
        return fig

    
    # Style commun aux secteurs
    def style_pie_chart(fig, title_text):
        fig.update_layout(
            title=dict(
                text=title_text,
                font=dict(size=20, family='Arial Black', color='black', weight='bold')
            ),
            font=dict(
                family="Arial Black",
                size=12,
                color='black'
            ),
            showlegend=False  # Suppression de la légende
        )
        
        # Personnalisation des étiquettes et pourcentages dans les secteurs
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            insidetextfont=dict(size=14, family="Arial Black")  # Texte en gras
        )
        
        return fig

    
     # Deuxième ligne de graphiques
    col1, col2, col3 = st.columns(3)
    
    with col1:
        
        # Graphique de répartition par segment
        segment_counts = active_clients['Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Count']
        
        # Créer le graphique en secteurs
        fig = px.pie(
            segment_counts, 
            values='Count', 
            names='Segment',
            color='Segment'  # Utilise 'Segment' comme base de couleur
        )

        # Appliquer la mise en forme avec la fonction de style
        fig = style_pie_chart(
            fig,
            title_text="Répartition des clients par segment de dépense"
        )

        # Afficher le graphique dans Streamlit
        st.plotly_chart(fig, use_container_width=True)


    with col2:
        
        # Graphique de repartition au churn par segment
        churn_by_segment = filtered_df.groupby('Segment')['Churn Status'].sum().reset_index()
        total_churn = churn_by_segment['Churn Status'].sum()
        churn_by_segment['Contribution'] = churn_by_segment['Churn Status'] / total_churn*100
        
        churn_by_segment = churn_by_segment.sort_values(by='Contribution', ascending=False)
    
        
        fig = px.bar(
            churn_by_segment,
            x='Segment',
            y='Contribution',
            text='Contribution',
            color='Segment'
        )

        fig = style_plotly_figure(
            fig,
            title_text="Répartition du churn par segment",
            yaxis_title_text="Pourcentage",
            xaxis_title_text="segment de dépense"
        )

        st.plotly_chart(fig, use_container_width=True)



    
    with col3:
    
        # Calculer le taux de churn par segment
        churn_by_segment = filtered_df.groupby('Segment')['Churn Status'].mean().reset_index()
        churn_by_segment = churn_by_segment.sort_values(by='Churn Status', ascending=False)
    
        # Créer le graphique à barres
        churn_chart = px.bar(
            churn_by_segment,
            x='Segment',
            y='Churn Status',
            text='Churn Status', 
            color='Segment'
        )

        # Appliquer la mise en forme avec ta fonction personnalisée
        churn_chart = style_plotly_figure(
            churn_chart,
            title_text="Taux de churn par Segment",
            yaxis_title_text="Pourcentage",
            xaxis_title_text="segment de dépense"
        )

        # Afficher le graphique dans Streamlit
        st.plotly_chart(churn_chart, use_container_width=True)

        
        
    # Troisième ligne de graphiques
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
        fig = px.pie(
            service_df, 
            values="Pourcentage", 
            names="Service",
            color="Service" 
        )

        # Appliquer la mise en forme avec la fonction de style
        fig = style_pie_chart(
            fig,
            title_text="Répartition des dépenses par service"
        )

        # Afficher le graphique dans Streamlit
        st.plotly_chart(fig, use_container_width=True)

    with col2:

        # Somme des dépenses par segment, triées dans l'ordre décroissant
        segment_spend = active_clients.groupby("Segment")["Total Spend"].sum().reset_index()
        segment_spend = segment_spend.sort_values(by="Total Spend", ascending=False)

        # Ajout des pourcentages
        segment_spend["Pourcentage"] = (segment_spend["Total Spend"] / segment_spend["Total Spend"].sum()) * 100

        # Création du graphique en barres
        # Créer le graphique à barres
        fig_segment = px.bar(
            segment_spend, 
            x="Segment", 
            y="Pourcentage", 
            text="Pourcentage",
            color='Segment'  # Utilise 'Segment' comme base de couleur
        )

        # Appliquer la mise en forme avec ta fonction personnalisée
        fig_segment = style_plotly_figure(
            fig_segment,
            title_text="Répartition des dépenses totales par segment",
            yaxis_title_text="<b>Pourcentage des dépenses</b>",
            xaxis_title_text="segment de dépense"
        )

        # Afficher le graphique dans Streamlit
        st.plotly_chart(fig_segment, use_container_width=True)

    with col3:
        # Filtrer les clients dont le réseau concurrent préféré est resté le même entre les mois 1 et 2
        same_competitor = filtered_df[
            filtered_df['Most Loved Competitor network in in Month 1'] == 
            filtered_df['Most Loved Competitor network in in Month 2']
        ]

        # Calcul de la distribution des réseaux concurrents
        competitor_dist = same_competitor['Most Loved Competitor network in in Month 2'].value_counts(normalize=True).reset_index()
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
            title=''  # On laisse vide ici car on le gère dans la fonction
        )

        fig4 = style_plotly_figure(
            fig4,
            title_text='<b>Répartition par réseaux concurrents les plus préférés</b>',
            yaxis_title_text='<b>Pourcentage de clients</b>',
            xaxis_title_text="Réseaux concurrents"
        )

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
            category_orders={'Complaint_Category': sorted_categories}
        )

        # Personnalisation du graphique
        # Appliquer la mise en forme avec ta fonction personnalisée
        fig = style_plotly_figure(
            fig,
            title_text="Taux de churn par niveau de plainte",
            yaxis_title_text="Pourcentage",
            xaxis_title_text="niveau de plainte"
        )

        fig.update_layout(
            showlegend=True,
            legend_title='',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )
        # Afficher le graphique dans Streamlit
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
            category_orders={'Tenure_Category': sorted_categories},
        )
        
        

        # Personnalisation du graphique
        fig = style_plotly_figure(
            fig,
            title_text="Taux de Churn par niveau d\'ancienneté",
            yaxis_title_text="Pourcentage",
            xaxis_title_text="niveau d\'ancienneté"
        )

        fig.update_layout(
            showlegend=True,
            legend_title='',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )
        # Afficher le graphique dans Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
    with col3:
        
        # Créer un dataframe qui croise Churn Status et Most Loved Competitor
        
        same_competitor = filtered_df[
            filtered_df['Most Loved Competitor network in in Month 1'] == 
            filtered_df['Most Loved Competitor network in in Month 2']
        ]
        
        churn_competitor_df = same_competitor.groupby(['Churn Status', 'Most Loved Competitor network in in Month 2']).size().reset_index()
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
        )

        
        # Personnalisation du graphique
        fig = style_plotly_figure(
            fig,
            title_text="concurrents préférés par statut de churn",
            yaxis_title_text="Pourcentage",
            xaxis_title_text="statut de churn"
        )

        fig.update_layout(
            showlegend=True,
            legend_title='',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=0.97,
                xanchor='right',
                x=1
            )
        )
        # Afficher le graphique dans Streamlit
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
            text='Pourcentage'
        )

        # Personnaliser le graphique
        # Personnalisation du graphique
        fig5 = style_plotly_figure(
            fig5,
            title_text="Répartition des dépenses par type de réseau (Mois 2)",
            yaxis_title_text="Pourcentage",
            xaxis_title_text="Type de réseau"
        )

        # Afficher le graphique
        st.plotly_chart(fig5, use_container_width=True)
    
    
    
        
    # Calcul du ratio avec +1 pour éviter division par zéro
    filtered_df['Ratio Offnet/Onnet'] = (
        (filtered_df['Total Offnet spend'] + 1) / (filtered_df['Total Onnet spend'] + 1)
    )

    
    col1, col2 = st.columns(2)

    # Histogramme du ratio Offnet/Onnet
    with col1:
        st.subheader("Histogramme du ratio Offnet / Onnet")
        
        # Créer une colonne de catégories
        def categorize_ratio(r):
            if r < 1:
                return "Offnet < Onnet"
            elif r <= 3:
                return "Offnet ≈ Onnet à 3x"
            else:
                return "Offnet > 3x Onnet"

        filtered_df['Ratio Category'] = filtered_df['Ratio Offnet/Onnet'].apply(categorize_ratio)
                
        ratio_counts = filtered_df['Ratio Category'].value_counts().reset_index()
        ratio_counts.columns = ['Ratio Category', 'Count']
        ratio_counts['Percentage'] = 100 * ratio_counts['Count'] / ratio_counts['Count'].sum()

        fig_ratio = px.pie(
            ratio_counts,
            names='Ratio Category',
            values='Count',
            hole=0.5,  # donut style
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        fig_ratio.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont=dict(size=14, family='Arial Black'),
            pull=[0.05, 0.02, 0.08]  # léger effet d'explosion
        )

        fig_ratio.update_layout(
            title_text="Répartition des utilisateurs selon le ratio Offnet/Onnet",
            title_font=dict(size=20, family='Arial Black'),
            showlegend=False
        )

        st.plotly_chart(fig_ratio, use_container_width=True)
        
        
    #  Diagramme en barres du ratio moyen par segment
    with col2:
        st.subheader("Ratio moyen par segment")
        mean_ratio = filtered_df.groupby('Segment')['Ratio Offnet/Onnet'].mean().reset_index()
        mean_ratio.columns = ['Segment', 'Ratio moyen']

        # Arrondir et formater le texte sans le %
        mean_ratio['Ratio moyen'] = mean_ratio['Ratio moyen'].round(2)
        mean_ratio = mean_ratio.sort_values('Ratio moyen', ascending=False)
        mean_ratio['text_label'] = mean_ratio['Ratio moyen'].astype(str)

        fig_bar = px.bar(
            mean_ratio,
            x='Segment',
            y='Ratio moyen',
            text='text_label',  # on affiche ce texte sans le %
            color='Segment',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )


        fig_bar = style_plotly_figure(
            fig_bar,
            title_text="Ratio moyen Offnet/Onnet par segment",
            yaxis_title_text="Ratio moyen",
            xaxis_title_text="Segment"
        )
        
        fig_bar.update_traces(
            texttemplate='<b>%{text}</b>',  # Sans le %
            textposition='outside',
            textfont=dict(
                family='Arial, sans-serif',
                size=12,
                color='black'
            )
        )

        st.plotly_chart(fig_bar, use_container_width=True)