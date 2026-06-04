import streamlit as st
from utils.data_loader import load_data

df = load_data()

latest = df[df.year == df.year.max()]

st.title("🤖 AI Insights")

top_nuclear = latest.nlargest(
    10,
    "nuclear_electricity"
)

st.subheader(
    "Top Nuclear Nations"
)

st.dataframe(
    top_nuclear[
        [
            "country",
            "nuclear_electricity",
            "decarbonisation_score"
        ]
    ]
)

high_carbon = latest.nlargest(
    10,
    "co2_mtonne"
)

st.subheader(
    "High Carbon Risk Countries"
)

st.dataframe(high_carbon)
