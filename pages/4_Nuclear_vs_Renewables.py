import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data

from utils.analytics import (
    get_latest_data,
    top_nuclear_countries,
    top_renewable_countries
)

from utils.charts import (
    bubble_chart,
    world_map,
    top_country_chart
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Nuclear vs Renewables",
    page_icon="⚛️",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

latest_df = get_latest_data(df)

# =====================================================
# VALIDATION
# =====================================================

required_cols = [
    "nuclear_electricity",
    "renewables_electricity"
]

missing = [
    col for col in required_cols
    if col not in latest_df.columns
]

if missing:

    st.error(
        f"Missing columns: {missing}"
    )

    st.stop()

# =====================================================
# HEADER
# =====================================================

st.title("⚛️ Nuclear vs 🌱 Renewables Intelligence")

st.markdown("""
Compare nuclear and renewable energy production
across countries and identify energy transition leaders.
""")

st.divider()

# =====================================================
# KPIs
# =====================================================

global_nuclear = latest_df[
    "nuclear_electricity"
].sum()

global_renewables = latest_df[
    "renewables_electricity"
].sum()

countries = latest_df[
    "country"
].nunique()

ratio = (
    global_nuclear /
    global_renewables
    if global_renewables > 0
    else 0
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Countries",
        countries
    )

with col2:
    st.metric(
        "Global Nuclear",
        f"{global_nuclear:,.0f}"
    )

with col3:
    st.metric(
        "Global Renewables",
        f"{global_renewables:,.0f}"
    )

with col4:
    st.metric(
        "Nuclear/Renewable Ratio",
        f"{ratio:.2f}"
    )

st.divider()

# =====================================================
# SCATTER ANALYSIS
# =====================================================

st.subheader(
    "Energy Transition Landscape"
)

size_col = (
    "population"
    if "population" in latest_df.columns
    else "nuclear_electricity"
)

color_col = (
    "decarbonisation_score"
    if "decarbonisation_score" in latest_df.columns
    else "renewables_electricity"
)

fig = bubble_chart(
    latest_df,
    "renewables_electricity",
    "nuclear_electricity",
    size_col,
    color_col,
    "country",
    "Nuclear vs Renewables"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# ENERGY QUADRANTS
# =====================================================

st.subheader(
    "Energy Transition Quadrants"
)

nuclear_avg = latest_df[
    "nuclear_electricity"
].mean()

renewable_avg = latest_df[
    "renewables_electricity"
].mean()

fig = px.scatter(
    latest_df,
    x="renewables_electricity",
    y="nuclear_electricity",
    hover_name="country",
    color=color_col,
    size=size_col
)

fig.add_vline(
    x=renewable_avg,
    line_dash="dash"
)

fig.add_hline(
    y=nuclear_avg,
    line_dash="dash"
)

fig.update_layout(
    template="plotly_dark",
    height=700,
    title="Energy Transition Quadrants"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info("""
Top Right = Strong Nuclear + Strong Renewables

Bottom Left = Low Clean Energy Adoption

Top Left = Renewable Dominant

Bottom Right = Nuclear Dominant
""")

st.divider()

# =====================================================
# TOP COUNTRIES
# =====================================================

left, right = st.columns(2)

with left:

    st.subheader(
        "🏆 Top Nuclear Producers"
    )

    nuclear_top = top_nuclear_countries(
        df,
        15
    )

    fig = top_country_chart(
        nuclear_top,
        "nuclear_electricity",
        "Top Nuclear Nations"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader(
        "🌱 Top Renewable Producers"
    )

    renewable_top = top_renewable_countries(
        df,
        15
    )

    fig = top_country_chart(
        renewable_top,
        "renewables_electricity",
        "Top Renewable Nations"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# COUNTRY RANKINGS
# =====================================================

st.subheader(
    "Country Energy Rankings"
)

ranking = latest_df[
    [
        col for col in [
            "country",
            "nuclear_electricity",
            "renewables_electricity",
            "decarbonisation_score",
            "co2_mtonne"
        ]
        if col in latest_df.columns
    ]
].copy()

ranking["clean_energy_total"] = (
    ranking["nuclear_electricity"]
    +
    ranking["renewables_electricity"]
)

ranking = ranking.sort_values(
    "clean_energy_total",
    ascending=False
)

st.dataframe(
    ranking.head(25),
    use_container_width=True
)

st.divider()

# =====================================================
# CORRELATION
# =====================================================

st.subheader(
    "Clean Energy Correlation"
)

corr_cols = [
    col for col in [
        "nuclear_electricity",
        "renewables_electricity",
        "co2_mtonne",
        "population",
        "gdp_per_capita_usd",
        "decarbonisation_score"
    ]
    if col in latest_df.columns
]

corr = latest_df[
    corr_cols
].corr()

fig = px.imshow(
    corr,
    text_auto=".2f",
    aspect="auto",
    title="Correlation Matrix"
)

fig.update_layout(
    template="plotly_dark",
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# NUCLEAR MAP
# =====================================================

if "iso_code" in latest_df.columns:

    st.subheader(
        "🌍 Nuclear Energy Map"
    )

    fig = world_map(
        latest_df,
        "iso_code",
        "nuclear_electricity",
        "country",
        "Global Nuclear Production"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# RENEWABLE MAP
# =====================================================

if "iso_code" in latest_df.columns:

    st.subheader(
        "🌎 Renewable Energy Map"
    )

    fig = world_map(
        latest_df,
        "iso_code",
        "renewables_electricity",
        "country",
        "Global Renewable Production"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# AI INSIGHTS
# =====================================================

st.subheader(
    "🤖 AI Insights"
)

top_nuclear = nuclear_top.iloc[0]
top_renewable = renewable_top.iloc[0]

insights = [

    f"⚛️ {top_nuclear['country']} is the world's leading nuclear electricity producer.",

    f"🌱 {top_renewable['country']} is the world's leading renewable electricity producer.",

    f"🌍 Global renewable generation currently totals {global_renewables:,.0f}.",

    f"⚡ Global nuclear generation currently totals {global_nuclear:,.0f}.",

    "📈 Countries balancing nuclear and renewables generally achieve stronger decarbonisation performance."

]

for item in insights:

    st.success(item)

st.divider()

# =====================================================
# DOWNLOAD
# =====================================================

csv = ranking.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download Energy Comparison Data",
    csv,
    "nuclear_vs_renewables.csv",
    "text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Global Nuclear Energy Intelligence Platform | Nuclear vs Renewables"
)
