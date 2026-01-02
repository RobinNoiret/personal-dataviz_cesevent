"""
Data loading and cleaning module for CES'Event donations
"""

import json
import pandas as pd
from datetime import datetime
from pathlib import Path


def load_donations(file_path: str = "data/donations.json") -> pd.DataFrame:
    """
    Load donations data from JSON file and convert to DataFrame.

    Args:
        file_path: Path to the donations JSON file

    Returns:
        pandas DataFrame with cleaned donation data
    """
    # Check if file exists
    if not Path(file_path).exists():
        raise FileNotFoundError(
            f"File {file_path} not found. Please add your donations.json file to the data/ directory."
        )

    # Load JSON data
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Clean and transform data
    df = clean_donations(df)

    return df


def clean_donations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and transform the donations DataFrame.

    Args:
        df: Raw donations DataFrame

    Returns:
        Cleaned DataFrame with proper types and calculated fields
    """
    # Make a copy to avoid modifying the original
    df = df.copy()

    # Convert amount to float, handling empty strings
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0.0)

    # Convert timestamp (milliseconds) to datetime
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Extract date and hour
    df['date'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    df['day_name'] = df['datetime'].dt.day_name()

    # Convert campus_confidence to float
    df['campus_confidence'] = df['campus_confidence'].astype(float)

    # Filter out zero or negative amounts
    df = df[df['amount'] > 0].copy()

    # Sort by datetime
    df = df.sort_values('datetime').reset_index(drop=True)

    # Add cumulative amount
    df['cumulative_amount'] = df['amount'].cumsum()

    # Add donation number
    df['donation_number'] = range(1, len(df) + 1)

    return df


def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Get a summary of the dataset.

    Args:
        df: Donations DataFrame

    Returns:
        Dictionary with dataset statistics
    """
    return {
        'total_donations': len(df),
        'date_range': {
            'start': df['datetime'].min(),
            'end': df['datetime'].max()
        },
        'total_amount': df['amount'].sum(),
        'unique_campuses': df['campus_name'].nunique(),
        'campuses': df['campus_name'].unique().tolist(),
        'verified_count': df['verified'].sum(),
        'unverified_count': (~df['verified']).sum()
    }
