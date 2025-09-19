# ml/predict_effectiveness.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from db.sqlite_db import create_connection


def train_predictive_model():
    conn = create_connection()
    df = pd.read_sql_query("""
    SELECT d.drug_id, d.dosage, d.side_effects_score, d.drug_class, e.score
    FROM drugs d JOIN effectiveness e USING(drug_id)
    """, conn)

    # Prepare features
    encoder = OneHotEncoder(sparse_output=False)
    cat_features = encoder.fit_transform(df[['drug_class', 'dosage']])
    num_features = df[['side_effects_score']].values
    X = np.hstack((cat_features, num_features))
    y = df['score'].values

    # Split: Train on non-missing
    non_missing_idx = ~np.isnan(y)
    X_train = X[non_missing_idx]
    y_train = y[non_missing_idx]

    if len(y_train) > 0:
        model = RandomForestRegressor(random_state=42)
        model.fit(X_train, y_train)

        # Predict missing
        missing_idx = np.isnan(y)
        if np.any(missing_idx):
            X_missing = X[missing_idx]
            predictions = model.predict(X_missing)
            missing_drug_ids = df.loc[missing_idx, 'drug_id'].values

            cursor = conn.cursor()
            for drug_id, pred in zip(missing_drug_ids, predictions):
                cursor.execute("""
                UPDATE effectiveness SET score = ?, predicted = 1 WHERE drug_id = ?
                """, (pred, drug_id))
            conn.commit()

        print("Effectiveness predictions complete.")

    conn.close()


if __name__ == "__main__":
    train_predictive_model()