# Sync functions to PostgreSQL

# db/cloud_sync.py
import psycopg2
from sqlite_db import create_connection, DB_PATH

# Placeholder: Replace with real credentials (e.g., AWS RDS PostgreSQL)
CLOUD_CONFIG = {
    "host": "your_postgres_host",
    "database": "drug_db",
    "user": "your_user",
    "password": "your_password",
    "port": 5432
}


def sync_to_cloud():
    # Connect local SQLite
    import pandas as pd
    sqlite_conn = create_connection()

    # Load data from SQLite
    drugs_df = pd.read_sql("SELECT * FROM drugs", sqlite_conn)
    prices_df = pd.read_sql("SELECT * FROM prices", sqlite_conn)
    eff_df = pd.read_sql("SELECT * FROM effectiveness", sqlite_conn)

    # Connect cloud DB
    cloud_conn = psycopg2.connect(**CLOUD_CONFIG)
    cloud_cursor = cloud_conn.cursor()

    # Assume same schema in cloud; create if not exists (for demo)
    cloud_cursor.execute("""
    CREATE TABLE IF NOT EXISTS drugs (
        drug_id INTEGER PRIMARY KEY,
        name TEXT,
        drug_class TEXT,
        brand TEXT,
        disease TEXT,
        dosage TEXT,
        side_effects_score REAL,
        cluster INTEGER
    );
    CREATE TABLE IF NOT EXISTS prices (
        price_id INTEGER PRIMARY KEY,
        drug_id INTEGER,
        price_per_dose REAL,
        region TEXT
    );
    CREATE TABLE IF NOT EXISTS effectiveness (
        eff_id INTEGER PRIMARY KEY,
        drug_id INTEGER,
        score REAL,
        predicted INTEGER DEFAULT 0
    );
    """)

    # Sync drugs
    for _, row in drugs_df.iterrows():
        cloud_cursor.execute("""
        INSERT INTO drugs VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (drug_id) DO UPDATE SET
        name=EXCLUDED.name, drug_class=EXCLUDED.drug_class, brand=EXCLUDED.brand,
        disease=EXCLUDED.disease, dosage=EXCLUDED.dosage, side_effects_score=EXCLUDED.side_effects_score,
        cluster=EXCLUDED.cluster;
        """, tuple(row))

    # Sync prices
    for _, row in prices_df.iterrows():
        cloud_cursor.execute("""
        INSERT INTO prices VALUES (%s, %s, %s, %s)
        ON CONFLICT (price_id) DO UPDATE SET
        drug_id=EXCLUDED.drug_id, price_per_dose=EXCLUDED.price_per_dose, region=EXCLUDED.region;
        """, tuple(row))

    # Sync effectiveness
    for _, row in eff_df.iterrows():
        cloud_cursor.execute("""
        INSERT INTO effectiveness VALUES (%s, %s, %s, %s)
        ON CONFLICT (eff_id) DO UPDATE SET
        drug_id=EXCLUDED.drug_id, score=EXCLUDED.score, predicted=EXCLUDED.predicted;
        """, tuple(row))

    cloud_conn.commit()
    cloud_cursor.close()
    cloud_conn.close()
    sqlite_conn.close()
    print("Cloud sync complete.")


if __name__ == "__main__":
    sync_to_cloud()

