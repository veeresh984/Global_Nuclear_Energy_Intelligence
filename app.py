import streamlit as st
import pandas as pd

from utils.data_loader import load_data

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Global Nuclear Energy Intelligence",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.metric-card {
    background-color: #1f2937;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
}

.big-font {
    font-size:28px !important;
    font-weight:bold;
}

.small-font {
    font-size:14px !important;
    color:gray;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def get_data():
    return load_data()

df = get_data()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.image(
        "assets/logo.png",
        use_container_width=True
    )

    st.title("⚛️ Nuclear Intelligence")

    st.markdown("---")

    st.markdown("""
### Dashboard Modules

🌍 Global Overview

🏭 Country Analysis

⚛️ Nuclear Analytics

🌱 Renewable Analytics

📉 Carbon Analytics

📊 Decarbonisation

🤖 AI Insights

Use the Pages menu above.
""")

    st.markdown("---")

    st.info(
        "Data Source: Global Nuclear Energy Intelligence Dataset"
    )

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("⚛️ Global Nuclear Energy Intelligence Platform")

st.markdown("""
Analyze global nuclear power generation, renewable energy growth,
carbon emissions, decarbonisation performance, and country-level
energy transition metrics from 1965–2025.
""")

st.divider()

# ---------------------------------------------------
# DATA VALIDATION
# ---------------------------------------------------

required_cols = [
    "country",
    "year"
]

missing_cols = [
    col for col in required_cols
    if col not in df.columns
]

if missing_cols:
    st.error(
        f"Missing required columns: {missing_cols}"
    )
    st.stop()

# ---------------------------------------------------
# LATEST YEAR DATA
# ---------------------------------------------------

latest_year = int(df["year"].max())

latest_df = df[
    df["year"] == latest_year
]

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

st.subheader("Executive Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Countries",
        f"{df['country'].nunique():,}"
    )

with col2:
    st.metric(
        "Latest Year",
        latest_year
    )

# Safe handling for optional columns

if "nuclear_electricity" in latest_df.columns:
    nuclear_total = latest_df[
        "nuclear_electricity"
    ].sum()
else:
    nuclear_total = 0

if "renewables_electricity" in latest_df.columns:
    renewable_total = latest_df[
        "renewables_electricity"
    ].sum()
else:
    renewable_total = 0

with col3:
    st.metric(
        "Global Nuclear Generation",
        f"{nuclear_total:,.0f}"
    )

with col4:
    st.metric(
        "Renewable Generation",
        f"{renewable_total:,.0f}"
    )

st.divider()

# ---------------------------------------------------
# DATA SUMMARY
# ---------------------------------------------------

left, right = st.columns([2, 1])

with left:

    st.subheader("Dataset Overview")

    st.write(
        f"""
        Total Records: **{len(df):,}**

        Total Features: **{len(df.columns)}**

        Year Range: **{df['year'].min()} - {df['year'].max()}**
        """
    )

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

with right:

    st.subheader("Dataset Statistics")

    stats_df = pd.DataFrame({
        "Metric": [
            "Rows",
            "Columns",
            "Countries",
            "Latest Year"
        ],
        "Value": [
            len(df),
            len(df.columns),
            df["country"].nunique(),
            latest_year
        ]
    })

    st.dataframe(
        stats_df,
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------
# AVAILABLE ANALYTICS
# ---------------------------------------------------

st.divider()

st.subheader("Available Analytics")

c1, c2, c3 = st.columns(3)

with c1:
    st.success("""
    🌍 Global Overview

    • Energy Trends

    • Nuclear Growth

    • Renewable Expansion

    • Historical Analysis
    """)

with c2:
    st.success("""
    📉 Carbon Analytics

    • CO₂ Trends

    • Carbon Intensity

    • Emission Benchmarking

    • Sustainability Scores
    """)

with c3:
    st.success("""
    🤖 AI Insights

    • Top Performers

    • Country Rankings

    • Decarbonisation Leaders

    • Automated Intelligence
    """)

# ---------------------------------------------------
# COLUMN INFORMATION
# ---------------------------------------------------

with st.expander("View Dataset Columns"):

    st.write(df.columns.tolist())

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "⚛️ Global Nuclear Energy Intelligence Dashboard | Streamlit + Plotly + Python"
)
