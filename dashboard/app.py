# dashboard/app.py
import streamlit as st
import pandas as pd
from db.sqlite_db import create_connection
from dashboard.utils import get_filtered_data, plot_scatter, plot_histogram, plot_boxplot, display_kpi, display_top_drugs

st.set_page_config(page_title="Drug Price-to-Effectiveness Dashboard", layout="wide")

conn = create_connection()

# Get unique values for filters
diseases = pd.read_sql("SELECT DISTINCT disease FROM drugs", conn)['disease'].tolist()
classes = pd.read_sql("SELECT DISTINCT drug_class FROM drugs", conn)['drug_class'].tolist()
regions = pd.read_sql("SELECT DISTINCT region FROM prices", conn)['region'].tolist()
brands = pd.read_sql("SELECT DISTINCT brand FROM drugs", conn)['brand'].tolist()

# Filters in sidebar
st.sidebar.title("Filters")
disease = st.sidebar.selectbox("Disease", ['All'] + diseases)
drug_class = st.sidebar.selectbox("Drug Class", ['All'] + classes)
region = st.sidebar.selectbox("Region", ['All'] + regions)
brand = st.sidebar.selectbox("Brand", ['All'] + brands)

filters = {'disease': disease, 'drug_class': drug_class, 'region': region, 'brand': brand}

df = get_filtered_data(conn, filters)

st.title("Drug Price-to-Effectiveness Dashboard")

# KPI
display_kpi(df)

# Visualizations
col1, col2 = st.columns(2)
with col1:
    plot_scatter(df)
with col2:
    plot_histogram(df)

plot_boxplot(df)

# Top drugs
display_top_drugs(df)

# Optional LLM summary (placeholder)
if st.button("Generate LLM Summaries (Optional)"):
    st.info("LLM integration: Use OpenAI/GPT API to summarize side effects or trials. Not implemented in skeleton.")

conn.close()