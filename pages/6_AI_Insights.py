import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data

from utils.analytics import (
    get_latest_data,
    top_nuclear_countries,
    top_renewable_countries,
    top_emission_countries,
    top_decarbonisation_countries,
    generate_ai_insights
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Insights",
    page_icon="🤖",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

latest_df = get_latest_data(df)

# =====================================================
# HEADER
# =====================================================

st.title("🤖 AI Energy Intelligence Center")

st.markdown("""
AI-generated intelligence layer for identifying:

- Sustainability Leaders
- Carbon Risks
- Nuclear Opportunities
- Renewable Growth Markets
- Energy Transition Champions
""")

st.divider()

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.header("📋 Executive AI Summary")

ai_summary = generate_ai_insights(df)

for insight in ai_summary:
    st.success(insight)

st.divider()

# =====================================================
# GLOBAL LEADERS
# =====================================================

st.header("🏆 Global Leaders")

col1, col2 = st.columns(2)

# Nuclear Leader
with col1:

    nuclear_leader = (
        top_nuclear_countries(df, 1)
        .iloc[0]
    )

    st.metric(
        "Top Nuclear Producer",
        nuclear_leader["country"]
    )

    st.info(
        f"""
        Nuclear Generation:
        {nuclear_leader['nuclear_electricity']:,.2f}
        """
    )

# Renewable Leader
with col2:

    renewable_leader = (
        top_renewable_countries(df, 1)
        .iloc[0]
    )

    st.metric(
        "Top Renewable Producer",
        renewable_leader["country"]
    )

    st.info(
        f"""
        Renewable Generation:
        {renewable_leader['renewables_electricity']:,.2f}
        """
    )

st.divider()

# =====================================================
# SUSTAINABILITY LEADERS
# =====================================================

st.header("🌱 Sustainability Champions")

leaders = top_decarbonisation_countries(
    df,
    10
)

st.dataframe(
    leaders[
        [
            col for col in [
                "country",
                "decarbonisation_score",
                "nuclear_electricity",
                "renewables_electricity"
            ]
            if col in leaders.columns
        ]
    ],
    use_container_width=True
)

fig = px.bar(
    leaders,
    x="country",
    y="decarbonisation_score",
    color="decarbonisation_score",
    title="Top Sustainability Countries"
)

fig.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# CARBON RISKS
# =====================================================

st.header("⚠️ Carbon Risk Intelligence")

risk_df = top_emission_countries(
    df,
    15
)

st.dataframe(
    risk_df[
        [
            col for col in [
                "country",
                "co2_mtonne",
                "co2_per_capita_t"
            ]
            if col in risk_df.columns
        ]
    ],
    use_container_width=True
)

fig = px.bar(
    risk_df,
    x="country",
    y="co2_mtonne",
    color="co2_mtonne",
    title="High Carbon Risk Countries"
)

fig.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# NUCLEAR OPPORTUNITIES
# =====================================================

st.header("⚛️ Nuclear Growth Opportunities")

if (
    "nuclear_electricity" in latest_df.columns
    and
    "decarbonisation_score" in latest_df.columns
):

    opportunities = latest_df.copy()

    opportunities = opportunities[
        opportunities["decarbonisation_score"]
        < opportunities["decarbonisation_score"].median()
    ]

    opportunities = opportunities.sort_values(
        "co2_mtonne",
        ascending=False
    )

    st.dataframe(
        opportunities.head(15),
        use_container_width=True
    )

    fig = px.scatter(
        opportunities,
        x="co2_mtonne",
        y="decarbonisation_score",
        size="population"
        if "population" in opportunities.columns
        else None,
        color="co2_mtonne",
        hover_name="country",
        title="Potential Nuclear Expansion Markets"
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
# RENEWABLE OPPORTUNITIES
# =====================================================

st.header("🌍 Renewable Growth Opportunities")

if (
    "renewables_electricity" in latest_df.columns
):

    renewable_gap = latest_df.copy()

    renewable_gap = renewable_gap.sort_values(
        "renewables_electricity",
        ascending=True
    )

    st.dataframe(
        renewable_gap.head(15),
        use_container_width=True
    )

st.divider()

# =====================================================
# AI SCORING MODEL
# =====================================================

st.header("🧠 AI Sustainability Ranking")

score_cols = [
    col for col in [
        "decarbonisation_score",
        "renewables_electricity",
        "nuclear_electricity"
    ]
    if col in latest_df.columns
]

ai_rank = latest_df.copy()

ai_rank["ai_score"] = 0

for col in score_cols:

    ai_rank["ai_score"] += (
        ai_rank[col].rank(
            pct=True
        ) * 100
    )

ai_rank = ai_rank.sort_values(
    "ai_score",
    ascending=False
)

st.dataframe(
    ai_rank[
        [
            "country",
            "ai_score"
        ]
    ].head(20),
    use_container_width=True
)

fig = px.bar(
    ai_rank.head(20),
    x="country",
    y="ai_score",
    color="ai_score",
    title="AI Sustainability Rankings"
)

fig.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# RECOMMENDATIONS
# =====================================================

st.header("🎯 AI Recommendations")

recommendations = [

    "Increase nuclear generation in high-emission economies.",

    "Accelerate renewable deployment in carbon-intensive regions.",

    "Improve grid flexibility and storage infrastructure.",

    "Reduce fossil-fuel dependency through energy diversification.",

    "Focus investments on countries with high emissions and low decarbonisation scores.",

    "Promote clean energy adoption through long-term sustainability policies."
]

for rec in recommendations:

    st.success(rec)

st.divider()

# =====================================================
# AUTOMATED REPORT
# =====================================================

st.header("📄 AI Executive Report")

report = f"""
GLOBAL AI ENERGY INTELLIGENCE REPORT

Top Nuclear Producer:
{nuclear_leader['country']}

Top Renewable Producer:
{renewable_leader['country']}

Highest Carbon Risk:
{risk_df.iloc[0]['country']}

Top Sustainability Leader:
{leaders.iloc[0]['country']}

Recommendation:
Accelerate clean energy investments and
reduce carbon intensity through balanced
nuclear and renewable energy expansion.
"""

st.text_area(
    "Generated Report",
    report,
    height=300
)

st.download_button(
    label="📥 Download AI Report",
    data=report,
    file_name="AI_Energy_Report.txt",
    mime="text/plain"
)

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Global Nuclear Energy Intelligence Platform | AI Insights Engine"
)
