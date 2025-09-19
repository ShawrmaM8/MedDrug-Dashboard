# SQLite connection & schema

import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).parent.parent / "data/processed/drug_data.db"


def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()

    # Expanded Drugs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drugs (
        drug_id INTEGER PRIMARY KEY,
        name TEXT,
        drug_class TEXT,
        brand TEXT,
        disease TEXT,
        dosage TEXT,
        side_effects_score REAL,
        cluster INTEGER
    )
    """)

    # Pricing table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        price_id INTEGER PRIMARY KEY,
        drug_id INTEGER,
        price_per_dose REAL,
        region TEXT,
        FOREIGN KEY (drug_id) REFERENCES drugs(drug_id)
    )
    """)

    # Effectiveness table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS effectiveness (
        eff_id INTEGER PRIMARY KEY,
        drug_id INTEGER,
        score REAL,
        predicted INTEGER DEFAULT 0,  -- 1 if predicted
        FOREIGN KEY (drug_id) REFERENCES drugs(drug_id)
    )
    """)

    conn.commit()
    conn.close()


def insert_data(df):
    conn = create_connection()
    cursor = conn.cursor()

    # Insert drugs
    for _, row in df.iterrows():
        cursor.execute("""
        INSERT OR REPLACE INTO drugs (drug_id, name, drug_class, brand, disease, dosage, side_effects_score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (row['drug_id'], row['name'], row['drug_class'], row['brand'], row['disease'], row['dosage'],
              row['side_effects_score']))

    # Insert prices
    for _, row in df.iterrows():
        cursor.execute("""
        INSERT OR REPLACE INTO prices (price_id, drug_id, price_per_dose, region)
        VALUES (?, ?, ?, ?)
        """, (row['price_id'], row['drug_id'], row['price_per_dose'], row['region']))

    # Insert effectiveness (score may be NaN)
    for _, row in df.iterrows():
        cursor.execute("""
        INSERT OR REPLACE INTO effectiveness (eff_id, drug_id, score)
        VALUES (?, ?, ?)
        """, (row['eff_id'], row['drug_id'], row['score'] if pd.notna(row['score']) else None))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_db()
    print("SQLite DB initialized.")