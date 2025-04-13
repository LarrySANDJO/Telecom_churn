
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