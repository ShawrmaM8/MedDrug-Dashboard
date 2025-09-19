# etl/clean_data.py
import pandas as pd
from pathlib import Path


def clean_and_enrich(raw_data):
    print("Cleaning and enriching data...")

    drugs = raw_data['drugs']
    prices = raw_data['prices']
    effectiveness = raw_data['effectiveness']

    # Merge datasets
    df = drugs.merge(prices, on='drug_id', how='left').merge(effectiveness, on='drug_id', how='left')

    # Normalize prices (assume already in USD per dose)
    # Handle missing values basically (ML will predict effectiveness)
    df['side_effects_score'] = df['side_effects_score'].fillna(df['side_effects_score'].mean())

    # Calculate initial ratio where possible
    df['ratio'] = df['price_per_dose'] / df['score']  # Will be NaN where score missing

    processed_path = Path(__file__).parent.parent.parent / "data/processed"
    processed_path.mkdir(parents=True, exist_ok=True)
    df.to_csv(processed_path / 'cleaned_data.csv', index=False)

    return df