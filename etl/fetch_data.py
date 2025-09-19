# etl/fetch_data.py
import pandas as pd
import numpy as np
from pathlib import Path


def fetch_raw_data():
    print(
        "Fetching raw data... Using synthetic data for demo. In production, replace with API calls to GoodRx, FDA, etc.")

    # Synthetic drugs data
    num_drugs = 50
    drugs = pd.DataFrame({
        'drug_id': range(1, num_drugs + 1),
        'name': [f'Drug_{i}' for i in range(1, num_drugs + 1)],
        'drug_class': np.random.choice(['Antibiotic', 'Analgesic', 'Antiviral', 'Anticancer'], num_drugs),
        'brand': np.random.choice(['BrandA', 'BrandB', 'Generic'], num_drugs),
        'disease': np.random.choice(['Infection', 'Pain', 'Virus', 'Cancer'], num_drugs),
        'dosage': np.random.choice(['10mg', '20mg', '50mg'], num_drugs),
        'side_effects_score': np.random.uniform(1, 10, num_drugs)  # For ML features
    })

    # Synthetic prices
    prices = pd.DataFrame({
        'price_id': range(1, num_drugs + 1),
        'drug_id': range(1, num_drugs + 1),
        'price_per_dose': np.random.uniform(5, 100, num_drugs),
        'region': np.random.choice(['US', 'EU', 'Asia'], num_drugs),
        'currency': 'USD'  # Normalized
    })

    # Synthetic effectiveness (with some missing)
    effectiveness = pd.DataFrame({
        'eff_id': range(1, num_drugs + 1),
        'drug_id': range(1, num_drugs + 1),
        'score': np.random.uniform(0.5, 1.0, num_drugs)
    })
    # Simulate missing data
    missing_idx = np.random.choice(num_drugs, 10, replace=False)
    effectiveness.loc[missing_idx, 'score'] = np.nan

    raw_path = Path(__file__).parent.parent.parent / "data/raw"
    raw_path.mkdir(parents=True, exist_ok=True)
    drugs.to_csv(raw_path / 'drugs.csv', index=False)
    prices.to_csv(raw_path / 'prices.csv', index=False)
    effectiveness.to_csv(raw_path / 'effectiveness.csv', index=False)

    return {
        'drugs': drugs,
        'prices': prices,
        'effectiveness': effectiveness
    }