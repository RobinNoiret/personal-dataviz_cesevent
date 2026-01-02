"""
KPI calculation module for CES'Event donations
"""

import pandas as pd
from datetime import timedelta


def calculate_main_kpis(df: pd.DataFrame) -> dict:
    """
    Calculate main KPIs for the donations.

    Args:
        df: Donations DataFrame

    Returns:
        Dictionary with main KPIs
    """
    total_amount = df['amount'].sum()
    total_donations = len(df)
    mean_donation = df['amount'].mean()
    median_donation = df['amount'].median()

    return {
        'total_amount': total_amount,
        'total_donations': total_donations,
        'mean_donation': mean_donation,
        'median_donation': median_donation
    }


def calculate_rate_per_hour(df: pd.DataFrame) -> float:
    """
    Calculate the average amount collected per hour.

    Args:
        df: Donations DataFrame

    Returns:
        Amount per hour
    """
    if len(df) == 0:
        return 0.0

    time_range = df['datetime'].max() - df['datetime'].min()
    hours = time_range.total_seconds() / 3600

    if hours == 0:
        return 0.0

    total_amount = df['amount'].sum()
    return total_amount / hours


def get_campus_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate performance metrics by campus.
    Note: This function is deprecated as campus data has been removed.
    Returns an empty DataFrame.

    Args:
        df: Donations DataFrame

    Returns:
        Empty DataFrame
    """
    return pd.DataFrame()


def get_hourly_donations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get donation statistics by hour of day.

    Args:
        df: Donations DataFrame

    Returns:
        DataFrame with hourly statistics
    """
    hourly = df.groupby('hour').agg({
        'amount': ['sum', 'count', 'mean']
    }).round(2)

    hourly.columns = ['total_amount', 'donation_count', 'mean_amount']
    hourly = hourly.reset_index()

    return hourly


def get_amount_distribution(df: pd.DataFrame, bins: list = None) -> pd.DataFrame:
    """
    Get the distribution of donation amounts.

    Args:
        df: Donations DataFrame
        bins: Custom bins for grouping amounts

    Returns:
        DataFrame with amount distribution
    """
    if bins is None:
        bins = [0, 5, 10, 20, 50, 100, 500, float('inf')]

    labels = [f"{bins[i]}-{bins[i+1]}" if bins[i+1] != float('inf') else f"{bins[i]}+"
              for i in range(len(bins) - 1)]

    df_copy = df.copy()
    df_copy['amount_range'] = pd.cut(df_copy['amount'], bins=bins, labels=labels, include_lowest=True)

    distribution = df_copy.groupby('amount_range', observed=True).agg({
        'amount': ['count', 'sum']
    }).round(2)

    distribution.columns = ['donation_count', 'total_amount']
    distribution = distribution.reset_index()

    return distribution


def get_top_donors(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Get top donors by donation amount.

    Args:
        df: Donations DataFrame
        n: Number of top donors to return

    Returns:
        DataFrame with top donors
    """
    # Filter donations with names
    named_donations = df[df['name'].notna()].copy()

    if len(named_donations) == 0:
        return pd.DataFrame(columns=['name', 'total_amount', 'donation_count'])

    # Group by name and aggregate
    top_donors = named_donations.groupby('name').agg({
        'amount': ['sum', 'count']
    }).round(2)

    top_donors.columns = ['total_amount', 'donation_count']
    top_donors = top_donors.reset_index()

    # Sort and get top n
    top_donors = top_donors.sort_values('total_amount', ascending=False).head(n)

    return top_donors


def get_timeline_data(df: pd.DataFrame, freq: str = 'H') -> pd.DataFrame:
    """
    Get cumulative timeline data.

    Args:
        df: Donations DataFrame
        freq: Frequency for resampling ('H' for hourly, 'D' for daily)

    Returns:
        DataFrame with timeline data
    """
    timeline = df.set_index('datetime')[['amount', 'donation_number']].resample(freq).agg({
        'amount': 'sum',
        'donation_number': 'count'
    })

    timeline['cumulative_amount'] = timeline['amount'].cumsum()
    timeline['cumulative_count'] = timeline['donation_number'].cumsum()

    return timeline.reset_index()
