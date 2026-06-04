import streamlit as st
import plotly.express as px

from utils.data_loader import load_data

df = load_data()

latest = df[df.year == df.year.max()]

top = (
    latest
    .sort_values(
        "decarbonisation_score",
        ascending=False
    )
    .head(20)
)

fig = px.bar(
    top,
    x="country",
    y="decarbonisation_score",
    color="carbon_intensity_tier"
)

st.plotly_chart(fig, use_container_width=True)
