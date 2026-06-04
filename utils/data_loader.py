"""
data_loader.py

Utility functions for loading and validating
Global Nuclear Energy Intelligence Dataset
"""

import pandas as pd
import streamlit as st
from pathlib import Path

# ---------------------------------------------------
# DATA PATH
# ---------------------------------------------------

DATA_PATH = Path(
    "data/global_nuclear_energy_intelligence_1965_2025.csv"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data(show_spinner=False)
def load_data():
    """
    Load CSV dataset

    Returns
    -------
    pandas.DataFrame
    """

    try:

        if not DATA_PATH.exists():

            st.error(
                f"Dataset not found:\n{DATA_PATH}"
            )

            st.stop()

        df = pd.read_csv(DATA_PATH)

        # Clean column names
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        return df

    except Exception as e:

        st.error(
            f"Error loading dataset:\n{e}"
        )

        st.stop()


# ---------------------------------------------------
# GET COLUMN LIST
# ---------------------------------------------------

def get_columns(df):
    """
    Return column names
    """

    return list(df.columns)


# ---------------------------------------------------
# NUMERIC COLUMNS
# ---------------------------------------------------

def get_numeric_columns(df):
    """
    Return numeric columns
    """

    return df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()


# ---------------------------------------------------
# CATEGORICAL COLUMNS
# ---------------------------------------------------

def get_categorical_columns(df):
    """
    Return categorical columns
    """

    return df.select_dtypes(
        include=["object"]
    ).columns.tolist()


# ---------------------------------------------------
# COUNTRY LIST
# ---------------------------------------------------

def get_country_list(df):

    if "country" not in df.columns:
        return []

    return sorted(
        df["country"]
        .dropna()
        .unique()
        .tolist()
    )


# ---------------------------------------------------
# LATEST YEAR
# ---------------------------------------------------

def get_latest_year(df):

    if "year" not in df.columns:
        return None

    return int(
        df["year"].max()
    )


# ---------------------------------------------------
# FILTER COUNTRY
# ---------------------------------------------------

def filter_country(df, country):

    if "country" not in df.columns:
        return df

    return df[
        df["country"] == country
    ]


# ---------------------------------------------------
# FILTER YEAR
# ---------------------------------------------------

def filter_year(df, year):

    if "year" not in df.columns:
        return df

    return df[
        df["year"] == year
    ]


# ---------------------------------------------------
# DATA SUMMARY
# ---------------------------------------------------

def get_dataset_summary(df):

    summary = {

        "rows":
            len(df),

        "columns":
            len(df.columns),

        "countries":
            df["country"].nunique()
            if "country" in df.columns
            else 0,

        "start_year":
            int(df["year"].min())
            if "year" in df.columns
            else None,

        "end_year":
            int(df["year"].max())
            if "year" in df.columns
            else None,

        "missing_values":
            int(df.isna().sum().sum())
    }

    return summary


# ---------------------------------------------------
# VALIDATE REQUIRED COLUMNS
# ---------------------------------------------------

def validate_columns(
    df,
    required_columns
):
    """
    Check required columns exist

    Returns:
    missing_columns
    """

    missing = [

        col

        for col in required_columns

        if col not in df.columns

    ]

    return missing


# ---------------------------------------------------
# LATEST DATA
# ---------------------------------------------------

def get_latest_data(df):

    if "year" not in df.columns:
        return df

    latest_year = df["year"].max()

    return df[
        df["year"] == latest_year
    ]


# ---------------------------------------------------
# COUNTRY DATA
# ---------------------------------------------------

def get_country_data(
    df,
    country
):

    if "country" not in df.columns:
        return pd.DataFrame()

    return df[
        df["country"] == country
    ].sort_values("year")


# ---------------------------------------------------
# TOP COUNTRIES
# ---------------------------------------------------

def get_top_countries(
    df,
    metric,
    top_n=10
):

    latest_df = get_latest_data(df)

    if metric not in latest_df.columns:
        return pd.DataFrame()

    return (
        latest_df
        .sort_values(
            metric,
            ascending=False
        )
        .head(top_n)
    )


# ---------------------------------------------------
# EXPORT DATA
# ---------------------------------------------------

def dataframe_to_csv(df):

    return df.to_csv(
        index=False
    ).encode("utf-8")


# ---------------------------------------------------
# TEST
# ---------------------------------------------------

if __name__ == "__main__":

    df = load_data()

    print(
        get_dataset_summary(df)
    )
