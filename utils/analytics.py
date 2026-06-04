"""
analytics.py

Business Analytics Engine
Global Nuclear Energy Intelligence Platform
"""

import pandas as pd
import numpy as np


# =====================================================
# BASIC DATA METRICS
# =====================================================

def total_countries(df):

    if "country" not in df.columns:
        return 0

    return df["country"].nunique()


def latest_year(df):

    if "year" not in df.columns:
        return None

    return int(df["year"].max())


def total_records(df):

    return len(df)


def total_columns(df):

    return len(df.columns)


# =====================================================
# LATEST DATA
# =====================================================

def get_latest_data(df):

    year = latest_year(df)

    return df[df["year"] == year]


# =====================================================
# KPI FUNCTIONS
# =====================================================

def global_nuclear_generation(df):

    latest = get_latest_data(df)

    if "nuclear_electricity" not in latest.columns:
        return 0

    return latest["nuclear_electricity"].sum()


def global_renewable_generation(df):

    latest = get_latest_data(df)

    if "renewables_electricity" not in latest.columns:
        return 0

    return latest["renewables_electricity"].sum()


def global_co2_emissions(df):

    latest = get_latest_data(df)

    if "co2_mtonne" not in latest.columns:
        return 0

    return latest["co2_mtonne"].sum()


def global_population(df):

    latest = get_latest_data(df)

    if "population" not in latest.columns:
        return 0

    return latest["population"].sum()


# =====================================================
# COUNTRY FILTERS
# =====================================================

def get_country_data(df, country):

    if "country" not in df.columns:
        return pd.DataFrame()

    return (
        df[df["country"] == country]
        .sort_values("year")
    )


# =====================================================
# TOP COUNTRIES
# =====================================================

def top_nuclear_countries(df, top_n=10):

    latest = get_latest_data(df)

    if "nuclear_electricity" not in latest.columns:
        return pd.DataFrame()

    return (
        latest
        .sort_values(
            "nuclear_electricity",
            ascending=False
        )
        .head(top_n)
    )


def top_renewable_countries(df, top_n=10):

    latest = get_latest_data(df)

    if "renewables_electricity" not in latest.columns:
        return pd.DataFrame()

    return (
        latest
        .sort_values(
            "renewables_electricity",
            ascending=False
        )
        .head(top_n)
    )


def top_emission_countries(df, top_n=10):

    latest = get_latest_data(df)

    if "co2_mtonne" not in latest.columns:
        return pd.DataFrame()

    return (
        latest
        .sort_values(
            "co2_mtonne",
            ascending=False
        )
        .head(top_n)
    )


def top_decarbonisation_countries(df, top_n=10):

    latest = get_latest_data(df)

    if "decarbonisation_score" not in latest.columns:
        return pd.DataFrame()

    return (
        latest
        .sort_values(
            "decarbonisation_score",
            ascending=False
        )
        .head(top_n)
    )


# =====================================================
# COUNTRY RANKING
# =====================================================

def country_rank(df, metric):

    latest = get_latest_data(df)

    if metric not in latest.columns:
        return pd.DataFrame()

    ranking = (
        latest
        .sort_values(metric, ascending=False)
        [["country", metric]]
        .reset_index(drop=True)
    )

    ranking.index += 1

    return ranking


# =====================================================
# GROWTH ANALYSIS
# =====================================================

def calculate_growth_rate(series):

    if len(series) < 2:
        return 0

    start = series.iloc[0]
    end = series.iloc[-1]

    if start == 0:
        return 0

    return ((end - start) / start) * 100


def country_nuclear_growth(df, country):

    country_df = get_country_data(df, country)

    if "nuclear_electricity" not in country_df.columns:
        return 0

    return round(
        calculate_growth_rate(
            country_df["nuclear_electricity"]
        ),
        2
    )


def renewable_growth(df, country):

    country_df = get_country_data(df, country)

    if "renewables_electricity" not in country_df.columns:
        return 0

    return round(
        calculate_growth_rate(
            country_df["renewables_electricity"]
        ),
        2
    )


# =====================================================
# DECARBONISATION ANALYTICS
# =====================================================

def average_decarbonisation_score(df):

    latest = get_latest_data(df)

    if "decarbonisation_score" not in latest.columns:
        return 0

    return round(
        latest["decarbonisation_score"].mean(),
        2
    )


def best_decarbonisation_country(df):

    latest = get_latest_data(df)

    if "decarbonisation_score" not in latest.columns:
        return None

    row = latest.loc[
        latest["decarbonisation_score"].idxmax()
    ]

    return row["country"]


# =====================================================
# CARBON INTELLIGENCE
# =====================================================

def average_carbon_intensity(df):

    latest = get_latest_data(df)

    if "co2_per_capita_t" not in latest.columns:
        return 0

    return round(
        latest["co2_per_capita_t"].mean(),
        2
    )


def high_carbon_risk(df):

    latest = get_latest_data(df)

    if "co2_mtonne" not in latest.columns:
        return pd.DataFrame()

    return (
        latest
        .sort_values(
            "co2_mtonne",
            ascending=False
        )
        .head(15)
    )


# =====================================================
# CORRELATION ANALYSIS
# =====================================================

def correlation_matrix(df):

    numeric_df = df.select_dtypes(
        include=np.number
    )

    return numeric_df.corr()


# =====================================================
# ENERGY MIX
# =====================================================

def energy_mix_summary(df):

    latest = get_latest_data(df)

    cols = [
        "nuclear_electricity",
        "renewables_electricity",
        "coal_electricity",
        "gas_electricity",
        "oil_electricity"
    ]

    available = [
        c for c in cols
        if c in latest.columns
    ]

    if len(available) == 0:
        return pd.DataFrame()

    totals = latest[available].sum()

    return pd.DataFrame({
        "Source": totals.index,
        "Generation": totals.values
    })


# =====================================================
# AI INSIGHT ENGINE
# =====================================================

def generate_ai_insights(df):

    insights = []

    try:

        nuclear_leader = (
            top_nuclear_countries(df, 1)
            .iloc[0]["country"]
        )

        insights.append(
            f"🏆 {nuclear_leader} is the largest nuclear energy producer."
        )

    except:
        pass

    try:

        decarb_leader = (
            top_decarbonisation_countries(df, 1)
            .iloc[0]["country"]
        )

        insights.append(
            f"🌱 {decarb_leader} leads global decarbonisation performance."
        )

    except:
        pass

    try:

        carbon_risk = (
            top_emission_countries(df, 1)
            .iloc[0]["country"]
        )

        insights.append(
            f"⚠️ {carbon_risk} currently produces the highest CO₂ emissions."
        )

    except:
        pass

    if len(insights) == 0:

        insights.append(
            "No AI insights available."
        )

    return insights


# =====================================================
# SCORECARD
# =====================================================

def executive_scorecard(df):

    return {
        "countries": total_countries(df),
        "latest_year": latest_year(df),
        "nuclear_generation":
            round(global_nuclear_generation(df), 2),
        "renewable_generation":
            round(global_renewable_generation(df), 2),
        "co2_emissions":
            round(global_co2_emissions(df), 2),
        "population":
            round(global_population(df), 2),
        "avg_decarbonisation":
            average_decarbonisation_score(df)
    }
