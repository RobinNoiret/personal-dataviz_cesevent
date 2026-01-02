"""
Visualization functions using Plotly for CES'Event donations
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# Color scheme
COLORS = {
    'primary': '#D3614E',
    'background': '#1E1E1E',
    'secondary_bg': '#2A2A2A',
    'tertiary_bg': '#3A3A3A',
    'text': '#FFFFFF',
    'grid': '#444444'
}

# Default layout template
LAYOUT_TEMPLATE = {
    'plot_bgcolor': COLORS['background'],
    'paper_bgcolor': COLORS['background'],
    'font': {'color': COLORS['text'], 'family': 'Arial, sans-serif'},
    'xaxis': {'gridcolor': COLORS['grid'], 'linecolor': COLORS['grid']},
    'yaxis': {'gridcolor': COLORS['grid'], 'linecolor': COLORS['grid']},
    'margin': {'l': 50, 'r': 30, 't': 50, 'b': 50}
}


def create_timeline_chart(timeline_df: pd.DataFrame) -> go.Figure:
    """
    Create cumulative timeline chart for donations.

    Args:
        timeline_df: DataFrame with timeline data

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=timeline_df['datetime'],
        y=timeline_df['cumulative_amount'],
        mode='lines',
        name='Montant cumulé',
        line=dict(color=COLORS['primary'], width=3),
        fill='tozeroy',
        fillcolor=f"rgba(211, 97, 78, 0.2)"
    ))

    fig.update_layout(
        **LAYOUT_TEMPLATE,
        title='Évolution cumulative des donations',
        hovermode='x unified'
    )

    fig.update_xaxes(title='Date et heure')
    fig.update_yaxes(title='Montant cumulé (€)')

    return fig


def create_campus_bar_chart(campus_df: pd.DataFrame) -> go.Figure:
    """
    Create bar chart for campus performance.

    Args:
        campus_df: DataFrame with campus statistics

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=campus_df['campus_name'],
        y=campus_df['total_amount'],
        text=campus_df['total_amount'].apply(lambda x: f"{x:.2f}€"),
        textposition='auto',
        marker_color=COLORS['primary'],
        hovertemplate='<b>%{x}</b><br>Montant: %{y:.2f}€<br>Donations: %{customdata}<extra></extra>',
        customdata=campus_df['donation_count']
    ))

    fig.update_layout(
        **LAYOUT_TEMPLATE,
        title='Montant total collecté par campus',
        showlegend=False
    )

    fig.update_xaxes(title='Campus')
    fig.update_yaxes(title='Montant total (€)')

    return fig


def create_campus_pie_chart(campus_df: pd.DataFrame) -> go.Figure:
    """
    Create pie chart for campus distribution.

    Args:
        campus_df: DataFrame with campus statistics

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=campus_df['campus_name'],
        values=campus_df['total_amount'],
        hole=0.4,
        marker=dict(
            colors=px.colors.sequential.Reds_r,
            line=dict(color=COLORS['background'], width=2)
        ),
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Montant: %{value:.2f}€<br>Pourcentage: %{percent}<extra></extra>'
    ))

    fig.update_layout(
        **LAYOUT_TEMPLATE,
        title='Répartition par campus (%)',
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        )
    )

    return fig


def create_amount_histogram(df: pd.DataFrame) -> go.Figure:
    """
    Create histogram for donation amount distribution with explicit bins.

    Args:
        df: Donations DataFrame

    Returns:
        Plotly figure
    """
    import numpy as np

    # Define base bins
    base_bins = [0, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200, 500]

    # Add max value if it's larger than the last bin
    max_amount = df['amount'].max()
    if max_amount > base_bins[-1]:
        bins = base_bins + [max_amount + 1]
    else:
        # Remove bins larger than max amount and add max
        bins = [b for b in base_bins if b <= max_amount] + [max_amount + 0.01]

    # Create histogram data
    hist_data, bin_edges = np.histogram(df['amount'], bins=bins)

    # Create bin labels
    bin_labels = []
    for i in range(len(bin_edges) - 1):
        if bin_edges[i+1] <= 500:
            bin_labels.append(f"{int(bin_edges[i])}-{int(bin_edges[i+1])}€")
        else:
            bin_labels.append(f">{int(bin_edges[i])}€")

    # Create bar chart instead of histogram for clarity
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=bin_labels,
        y=hist_data,
        marker_color=COLORS['primary'],
        opacity=0.8,
        text=hist_data,
        textposition='auto',
        hovertemplate='Tranche: %{x}<br>Nombre: %{y}<extra></extra>'
    ))

    fig.update_layout(
        **LAYOUT_TEMPLATE,
        title='Distribution des montants de donations',
        showlegend=False
    )

    fig.update_xaxes(title='Tranche de montant', tickangle=-45)
    fig.update_yaxes(title='Nombre de donations')

    return fig


def create_hourly_chart(hourly_df: pd.DataFrame) -> go.Figure:
    """
    Create line chart for hourly donations.

    Args:
        hourly_df: DataFrame with hourly statistics

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=hourly_df['hour'],
        y=hourly_df['total_amount'],
        mode='lines+markers',
        name='Montant total',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=8),
        hovertemplate='Heure: %{x}h<br>Montant: %{y:.2f}€<br>Donations: %{customdata}<extra></extra>',
        customdata=hourly_df['donation_count']
    ))

    fig.update_layout(
        **LAYOUT_TEMPLATE,
        title='Donations par heure de la journée',
        showlegend=False
    )

    fig.update_xaxes(
        title='Heure',
        tickmode='linear',
        tick0=0,
        dtick=1,
        range=[-0.5, 23.5]
    )
    fig.update_yaxes(title='Montant total (€)')

    return fig


def create_top_donors_chart(top_donors_df: pd.DataFrame) -> go.Figure:
    """
    Create bar chart for top donors.

    Args:
        top_donors_df: DataFrame with top donors

    Returns:
        Plotly figure
    """
    if len(top_donors_df) == 0:
        # Return empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="Aucun donateur identifié",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS['text'])
        )
        fig.update_layout(**LAYOUT_TEMPLATE, title='Top donateurs')
        return fig

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=top_donors_df['name'],
        x=top_donors_df['total_amount'],
        orientation='h',
        text=top_donors_df['total_amount'].apply(lambda x: f"{x:.2f}€"),
        textposition='auto',
        marker_color=COLORS['primary'],
        hovertemplate='<b>%{y}</b><br>Montant: %{x:.2f}€<br>Donations: %{customdata}<extra></extra>',
        customdata=top_donors_df['donation_count']
    ))

    fig.update_layout(
        **LAYOUT_TEMPLATE,
        title='Top donateurs',
        height=max(400, len(top_donors_df) * 40),
        showlegend=False
    )

    fig.update_xaxes(title='Montant total (€)')
    fig.update_yaxes(title='', autorange="reversed")

    return fig


def create_donations_count_chart(timeline_df: pd.DataFrame) -> go.Figure:
    """
    Create chart for cumulative donation count over time.

    Args:
        timeline_df: DataFrame with timeline data

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=timeline_df['datetime'],
        y=timeline_df['cumulative_count'],
        mode='lines',
        name='Nombre cumulé',
        line=dict(color='#FFA07A', width=3),
        fill='tozeroy',
        fillcolor='rgba(255, 160, 122, 0.2)'
    ))

    fig.update_layout(
        **LAYOUT_TEMPLATE,
        title='Évolution du nombre de donations',
        hovermode='x unified'
    )

    fig.update_xaxes(title='Date et heure')
    fig.update_yaxes(title='Nombre de donations')

    return fig
