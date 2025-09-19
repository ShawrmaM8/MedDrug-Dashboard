# etl/pipeline.py
from fetch_data import fetch_raw_data
from clean_data import clean_and_enrich
from db.sqlite_db import initialize_db, insert_data

def run_etl():
    initialize_db()
    raw_data = fetch_raw_data()
    clean_data = clean_and_enrich(raw_data)
    insert_data(clean_data)
    print("ETL complete. Data ready in SQLite.")

if __name__ == "__main__":
    run_etl()