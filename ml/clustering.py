# ml/clustering.py
import pandas as pd
from sklearn.cluster import KMeans
from db.sqlite_db import create_connection


def cluster_drugs():
    conn = create_connection()
    df = pd.read_sql_query("""
    SELECT d.drug_id, p.price_per_dose, e.score
    FROM drugs d 
    JOIN prices p USING(drug_id) 
    JOIN effectiveness e USING(drug_id)
    """, conn)

    if not df.empty:
        X = df[['price_per_dose', 'score']]
        kmeans = KMeans(n_clusters=5, random_state=42).fit(X)  # Increased clusters for better segmentation
        clusters = kmeans.labels_

        cursor = conn.cursor()
        for drug_id, cluster in zip(df['drug_id'], clusters):
            cursor.execute("UPDATE drugs SET cluster = ? WHERE drug_id = ?", (cluster, drug_id))
        conn.commit()

        print("Clustering complete.")

    conn.close()


if __name__ == "__main__":
    cluster_drugs()