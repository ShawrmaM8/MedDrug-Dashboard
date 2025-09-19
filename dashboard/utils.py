# dashboard/utils.py
import streamlit as st
import plotly.express as px


def get_filtered_data(conn, filters):
    query = """
    SELECT d.name, d.drug_class, d.brand, d.disease, d.cluster, 
           p.price_per_dose, p.region, e.score, e.predicted
    FROM drugs d 
    JOIN prices p USING(drug_id) 
    JOIN effectiveness e USING(drug_id)
    WHERE 1=1
    """
    params = []
    if filters['disease'] and filters['disease'] != 'All':
        query += " AND d.disease = ?"
        params.append(filters['disease'])
    if filters['drug_class'] and filters['drug_class'] != 'All':
        query += " AND d.drug_class = ?"
        params.append(filters['drug_class'])
    if filters['region'] and filters['region'] != 'All':
        query += " AND p.region = ?"
        params.append(filters['region'])
    if filters['brand'] and filters['brand'] != 'All':
        query += " AND d.brand = ?"
        params.append(filters['brand'])

    df = pd.read_sql_query(query, conn, params=params)
    df['ratio'] = df['price_per_dose'] / df['score']
    return df


def plot_scatter(df):
    fig = px.scatter(df, x='price_per_dose', y='score', color='cluster',
                     hover_data=['name', 'disease', 'drug_class', 'brand', 'region', 'predicted'],
                     title='Price vs Effectiveness (Clustered)')
    fig.update_traces(marker=dict(size=12, opacity=0.8))
    st.plotly_chart(fig, use_container_width=True)


def plot_histogram(df):
    fig = px.histogram(df, x='score', color='predicted', title='Effectiveness Distribution (Actual vs Predicted)')
    st.plotly_chart(fig, use_container_width=True)


def plot_boxplot(df):
    fig = px.box(df, x='drug_class', y='ratio', color='region', title='Price/Effectiveness Ratio by Class and Region')
    st.plotly_chart(fig, use_container_width=True)


def display_kpi(df):
    avg_ratio = df['ratio'].mean()
    st.metric("Average Price/Effectiveness Ratio", f"{avg_ratio:.2f}")


def display_top_drugs(df, top_n=10):
    st.subheader(f"Top {top_n} Cost-Effective Drugs (Lowest Ratio)")
    top_df = df.sort_values('ratio').head(top_n)[
        ['name', 'disease', 'drug_class', 'price_per_dose', 'score', 'ratio', 'predicted']]
    st.dataframe(top_df)