import streamlit as st
import plotly.express as px

from utils.data_loader import load_data

df = load_data()

country = st.selectbox(
    "Select Country",
    sorted(df.country.unique())
)

country_df = df[df.country == country]

st.title(country)

fig = px.line(
    country_df,
    x="year",
    y="nuclear_electricity",
    title="Nuclear Generation Trend"
)

st.plotly_chart(fig, use_container_width=True)

fig2 = px.line(
    country_df,
    x="year",
    y="renewables_electricity",
    title="Renewables Trend"
)

st.plotly_chart(fig2, use_container_width=True)
