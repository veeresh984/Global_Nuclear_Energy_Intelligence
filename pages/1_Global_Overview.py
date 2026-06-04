import streamlit as st
import plotly.express as px

from utils.data_loader import load_data

df = load_data()

st.title("🌍 Global Overview")

global_year = (
    df.groupby("year")
      .agg({
          "nuclear_electricity":"sum",
          "renewables_electricity":"sum",
          "co2_mtonne":"sum"
      })
      .reset_index()
)

fig = px.line(
    global_year,
    x="year",
    y=[
        "nuclear_electricity",
        "renewables_electricity"
    ],
    title="Global Electricity Trends"
)

st.plotly_chart(fig, use_container_width=True)

fig2 = px.area(
    global_year,
    x="year",
    y="co2_mtonne",
    title="Global CO₂ Emissions"
)

st.plotly_chart(fig2, use_container_width=True)
