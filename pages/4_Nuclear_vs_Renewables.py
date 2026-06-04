import streamlit as st
import plotly.express as px

from utils.data_loader import load_data

df = load_data()

latest = df[df.year == df.year.max()]

fig = px.scatter(
    latest,
    x="renewables_electricity",
    y="nuclear_electricity",
    size="population",
    color="decarbonisation_score",
    hover_name="country",
    title="Nuclear vs Renewables"
)

st.plotly_chart(fig, use_container_width=True)
