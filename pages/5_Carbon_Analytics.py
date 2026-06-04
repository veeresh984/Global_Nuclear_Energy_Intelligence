import streamlit as st
import plotly.express as px

from utils.data_loader import load_data

df = load_data()

latest = df[df.year == df.year.max()]

fig = px.treemap(
    latest,
    path=["carbon_intensity_tier","country"],
    values="co2_mtonne",
    color="co2_per_capita_t"
)

st.plotly_chart(fig, use_container_width=True)
