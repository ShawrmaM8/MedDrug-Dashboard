#!/bin/bash
# run_local.sh

# Install requirements if needed
pip install -r requirements.txt

# Run ETL
python etl/pipeline.py

# Run ML
python ml/predict_effectiveness.py
python ml/clustering.py

# Optional cloud sync
# python db/cloud_sync.py

# Launch dashboard
streamlit run dashboard/app.py