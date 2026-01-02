"""
CES'Event Donations Dashboard - Main Streamlit Application
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.load_data import load_donations, get_data_summary
from src.compute_kpis import (
    calculate_main_kpis,
    calculate_rate_per_hour,
    get_hourly_donations,
    get_top_donors,
    get_timeline_data
)
from src.visualizations import (
    create_timeline_chart,
    create_amount_histogram,
    create_hourly_chart,
    create_top_donors_chart,
    create_donations_count_chart,
    COLORS
)


# Page configuration
st.set_page_config(
    page_title="CES'Event Donations Dashboard",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme
st.markdown(f"""
    <style>
        .stApp {{
            background-color: {COLORS['background']};
        }}
        .stMetric {{
            background-color: {COLORS['secondary_bg']};
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid {COLORS['primary']};
        }}
        .stMetric label {{
            color: {COLORS['text']} !important;
            font-size: 1rem !important;
        }}
        .stMetric [data-testid="stMetricValue"] {{
            color: {COLORS['primary']} !important;
            font-size: 2rem !important;
        }}
        h1, h2, h3 {{
            color: {COLORS['text']} !important;
        }}
        .metric-container {{
            background-color: {COLORS['secondary_bg']};
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }}
    </style>
""", unsafe_allow_html=True)


def format_currency(amount: float) -> str:
    """Format amount as currency."""
    return f"{amount:,.2f}€".replace(',', ' ')


def main():
    """Main application function."""

    # Header
    st.title("CES'Event - Dashboard des Donations")
    st.markdown("---")

    # Load data
    try:
        df = load_donations("data/donations.json")
    except FileNotFoundError as e:
        st.error(f"Erreur: {str(e)}")
        st.info("Veuillez ajouter votre fichier donations.json dans le dossier data/")
        st.stop()
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {str(e)}")
        st.stop()

    # Calculate KPIs
    main_kpis = calculate_main_kpis(df)
    rate_per_hour = calculate_rate_per_hour(df)
    data_summary = get_data_summary(df)

    # Display main KPIs in columns
    st.header("Indicateurs Clés")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Montant Total Collecté",
            value=format_currency(main_kpis['total_amount']),
            help="Somme totale de toutes les donations reçues durant l'événement"
        )

    with col2:
        st.metric(
            label="Nombre de Donations",
            value=f"{main_kpis['total_donations']:,}".replace(',', ' '),
            help="Nombre total de contributions individuelles"
        )

    with col3:
        st.metric(
            label="Don Moyen",
            value=format_currency(main_kpis['mean_donation']),
            help="Montant moyen par donation (moyenne arithmétique)"
        )

    with col4:
        st.metric(
            label="Don Médian",
            value=format_currency(main_kpis['median_donation']),
            help="Montant médian - 50% des donations sont au-dessus et 50% en-dessous de cette valeur"
        )

    with col5:
        st.metric(
            label="Taux par Heure",
            value=format_currency(rate_per_hour),
            help="Montant moyen collecté par heure sur la période totale de l'événement"
        )

    st.markdown("---")

    # Timeline section
    st.header("Évolution Temporelle")

    timeline_data = get_timeline_data(df, freq='H')

    col1, col2 = st.columns(2)

    with col1:
        fig_timeline = create_timeline_chart(timeline_data)
        st.plotly_chart(fig_timeline, use_container_width=True)

    with col2:
        fig_count = create_donations_count_chart(timeline_data)
        st.plotly_chart(fig_count, use_container_width=True)

    st.markdown("---")

    # Distribution and hourly patterns
    st.header("Analyses Détaillées")

    col1, col2 = st.columns(2)

    with col1:
        fig_histogram = create_amount_histogram(df)
        st.plotly_chart(fig_histogram, use_container_width=True)

    with col2:
        hourly_data = get_hourly_donations(df)
        fig_hourly = create_hourly_chart(hourly_data)
        st.plotly_chart(fig_hourly, use_container_width=True)

    st.markdown("---")

    # Top donors section
    st.header("Top Donateurs")

    top_donors = get_top_donors(df, n=10)

    if len(top_donors) > 0:
        col1, col2 = st.columns([2, 1])

        with col1:
            fig_top_donors = create_top_donors_chart(top_donors)
            st.plotly_chart(fig_top_donors, use_container_width=True)

        with col2:
            st.subheader("Tableau des Top Donateurs")
            display_top = top_donors.copy()
            display_top['total_amount'] = display_top['total_amount'].apply(format_currency)
            display_top.columns = ['Nom', 'Montant Total', 'Nb Donations']
            st.dataframe(display_top, use_container_width=True, hide_index=True)
    else:
        st.info("Aucun donateur identifié (pas de noms dans les données)")

    st.markdown("---")

    # Footer with data info
    st.caption(f"""
    Données du {data_summary['date_range']['start'].strftime('%d/%m/%Y %H:%M')}
    au {data_summary['date_range']['end'].strftime('%d/%m/%Y %H:%M')} |
    {data_summary['verified_count']} donations vérifiées
    """)


if __name__ == "__main__":
    main()
