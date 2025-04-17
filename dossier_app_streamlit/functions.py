
import streamlit as st


def display_custom_metric(label, value, color):
    """
    return st.markdown
    """
    st.markdown(
        f"""
        <div style="background-color: {color}; padding: 20px; border-radius: 10px; margin: 5px 0;">
            <p style="font-size: 9px; margin: 0; color: white;">{label}</p>
            <h2 style="margin: 0; color: white; font-weight: bold">{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
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


def display_stylized_title(title_text, background="#0A04AA", color="white"):
    st.markdown(f"""
    <div style='
        background-color: {background};
        padding: 10px 20px;
        border-radius: 10px;
        color: {color};
        font-family: Arial Black;
        font-size: 20px;
        text-align: center;
        margin-bottom: 20px;
    '>
        {title_text}
    </div>
    """, unsafe_allow_html=True)
    
def afficher_guide_utilisateur():
    # CSS personnalisé pour l'expander
    
    
    # CSS personnalisé pour modifier l'apparence de l'expander
    st.markdown("""
    <style>
    .streamlit-expanderHeader {
        background-color: #f0f8ff;
        color: black;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    with st.expander("Guide d'utilisation"):

        st.markdown("""
        # Guide Technique - Dashboard d'Analyse d'Attrition Client

        Ce document présente un briefing du calcul des indicateurs et la construction des visualisations du dashboard.

        ## Indicateurs de Performance (KPIs)

        - **Taux de Churn actuel** : Pourcentage de clients perdus sur la période de 2 mois étudiée
        - **Taux d'actifs** : Pourcentage de clients toujours présents dans la base
        - **Ancienneté moyenne** : Durée moyenne d'engagement des clients (en mois)
        - **Taux de plaintes** : Proportion de clients ayant déposé une réclamation

        ## Segmentation Client

        - **Méthode** : Clustering basé sur les dépenses des 2 premiers mois de 2017
        - **Segments** :
        - Dépense "Faible" : < 2 332,63 (clients peu engageants)
        - Dépense "Moyenne" : 2 332,63 ≤ dépenses < 9 969,21 (clients modérément actifs)
        - Dépense "Élevé" : ≥ 9 969,21 (clients hautement rentables)

        ## Visualisations Analytiques

        ### Page d'accueil (KPIs)

        1. **Segmentation Client** 
        - Données : Pourcentage de clients dans chaque segment de dépense

        2. **Churn par segment**
        - Données : Pourcentage de churn par segment de dépense

        3. **Churn et réclamations**
        - Données : Taux de churn par niveau de plaintes
        - Segmentation :
            - 0 : Aucune plainte
            - 1-3 : Faible plainte
            - >3 : Niveau élevé

        4. **Churn et ancienneté**
        - Données : Taux de churn par durée d'ancienneté
        - Segmentation :
            - ≤12 mois : Nouveau
            - ≤36 mois : Établi
            - >36 mois : Fidèle

        5. **Concurrents préférés**
        - Données : Répartition des clients partis vers chaque concurrent

        6. **Rentabilité des réseaux**
        - Données : Contribution de chaque type de réseau au chiffre d'affaires

        7. **Répartition des dépenses par type de réseau**
        - Données : Pourcentage des dépenses totales par type de réseau au mois 2

        8. **Répartition des dépenses par service**
        - Données : Décomposition du panier moyen entre services (SMS, Data, appels Onnet/Offnet)

        9. **Contribution des segments aux dépenses totales**
        - Données : Valeur économique de chaque segment client

        10. **Migrations réseaux**
            - Type : Matrice de flux (Sankey ou heatmap)
            - Données : Migrations d'abonnements réseau (2G, 3G, Other) entre deux mois consécutifs

        ### Page de prédictions

        1. **KPI principal**
        - Nombre de clients prédits à haut risque (>60%)

        2. **Répartition des clients à haut risque par segment**
        - Données : Proportion de chaque segment parmi les clients à haut risque

        3. **Taux de clients prédits à haut risque par segment**
        - Données : Pour chaque segment, proportion des clients à haut risque

        4. **Analyse des facteurs d'influence**
        - Données : Variables influençant le plus la décision d'attrition
        
        ### Page de prédictions
        
        Cette page fournit concrètement les clients selon différents critères et 
        en fonction du nombre que l'on veut observer. Les filtres sur la barre latérale 
        permettent d'avoir des résultats plus fins selon les besoins.
                """)
        
        

