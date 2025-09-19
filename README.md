## Drug Price-to-Effectiveness Dashboard

### Setup
1. Create virtual env: `python -m venv venv; source venv/bin/activate`
2. Install deps: `pip install -r requirements.txt`
3. Run: `./run_local.sh`

### Features
- ETL with synthetic data (expand to real APIs).
- ML: RandomForest for predictions, KMeans clustering.
- Dashboard: Filters, scatter/hist/box plots, KPI, top drugs.
- Cloud: Sync to PostgreSQL (configure in cloud_sync.py).

For production: Deploy to AWS/Azure, add real data sources, integrate LLM (e.g., OpenAI for summaries).
