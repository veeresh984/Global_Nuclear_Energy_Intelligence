"""
charts.py

Visualization Engine
Global Nuclear Energy Intelligence Platform
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# =====================================================
# DEFAULT LAYOUT
# =====================================================

def apply_layout(fig, title):

    fig.update_layout(
        title=title,
        template="plotly_dark",
        height=550,
        title_x=0.5,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    return fig


# =====================================================
# LINE CHART
# =====================================================

def line_chart(
    df,
    x,
    y,
    title
):

    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True
    )

    return apply_layout(fig, title)


# =====================================================
# MULTI LINE CHART
# =====================================================

def multi_line_chart(
    df,
    x,
    y_columns,
    title
):

    fig = px.line(
        df,
        x=x,
        y=y_columns
    )

    return apply_layout(fig, title)


# =====================================================
# AREA CHART
# =====================================================

def area_chart(
    df,
    x,
    y,
    title
):

    fig = px.area(
        df,
        x=x,
        y=y
    )

    return apply_layout(fig, title)


# =====================================================
# BAR CHART
# =====================================================

def bar_chart(
    df,
    x,
    y,
    title
):

    fig = px.bar(
        df,
        x=x,
        y=y,
        text_auto=".2s"
    )

    return apply_layout(fig, title)


# =====================================================
# HORIZONTAL BAR
# =====================================================

def horizontal_bar_chart(
    df,
    x,
    y,
    title
):

    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation="h"
    )

    return apply_layout(fig, title)


# =====================================================
# PIE CHART
# =====================================================

def pie_chart(
    df,
    names,
    values,
    title
):

    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.4
    )

    return apply_layout(fig, title)


# =====================================================
# DONUT CHART
# =====================================================

def donut_chart(
    df,
    names,
    values,
    title
):

    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.6
    )

    return apply_layout(fig, title)


# =====================================================
# SCATTER PLOT
# =====================================================

def scatter_chart(
    df,
    x,
    y,
    color,
    size,
    hover_name,
    title
):

    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        size=size,
        hover_name=hover_name
    )

    return apply_layout(fig, title)


# =====================================================
# BUBBLE CHART
# =====================================================

def bubble_chart(
    df,
    x,
    y,
    size,
    color,
    hover_name,
    title
):

    fig = px.scatter(
        df,
        x=x,
        y=y,
        size=size,
        color=color,
        hover_name=hover_name,
        size_max=60
    )

    return apply_layout(fig, title)


# =====================================================
# HISTOGRAM
# =====================================================

def histogram_chart(
    df,
    column,
    title
):

    fig = px.histogram(
        df,
        x=column,
        nbins=30
    )

    return apply_layout(fig, title)


# =====================================================
# BOX PLOT
# =====================================================

def box_plot(
    df,
    x,
    y,
    title
):

    fig = px.box(
        df,
        x=x,
        y=y
    )

    return apply_layout(fig, title)


# =====================================================
# TREEMAP
# =====================================================

def treemap_chart(
    df,
    path,
    values,
    color,
    title
):

    fig = px.treemap(
        df,
        path=path,
        values=values,
        color=color
    )

    return apply_layout(fig, title)


# =====================================================
# SUNBURST
# =====================================================

def sunburst_chart(
    df,
    path,
    values,
    title
):

    fig = px.sunburst(
        df,
        path=path,
        values=values
    )

    return apply_layout(fig, title)


# =====================================================
# CHOROPLETH MAP
# =====================================================

def world_map(
    df,
    location_col,
    color_col,
    hover_name,
    title
):

    fig = px.choropleth(
        df,
        locations=location_col,
        color=color_col,
        hover_name=hover_name,
        projection="natural earth"
    )

    return apply_layout(fig, title)


# =====================================================
# HEATMAP
# =====================================================

def correlation_heatmap(corr_matrix):

    fig = px.imshow(
        corr_matrix,
        text_auto=".2f",
        aspect="auto"
    )

    return apply_layout(
        fig,
        "Correlation Heatmap"
    )


# =====================================================
# ENERGY MIX CHART
# =====================================================

def energy_mix_chart(
    energy_df
):

    fig = px.pie(
        energy_df,
        names="Source",
        values="Generation",
        hole=0.5
    )

    return apply_layout(
        fig,
        "Global Energy Mix"
    )


# =====================================================
# TOP COUNTRIES CHART
# =====================================================

def top_country_chart(
    df,
    metric,
    title
):

    fig = px.bar(
        df,
        x="country",
        y=metric,
        color=metric,
        text_auto=".2s"
    )

    fig.update_xaxes(
        tickangle=-45
    )

    return apply_layout(fig, title)


# =====================================================
# FORECAST CHART
# =====================================================

def forecast_chart(
    historical_df,
    forecast_df,
    x,
    y,
    forecast_y,
    title
):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=historical_df[x],
            y=historical_df[y],
            mode="lines+markers",
            name="Historical"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_df[x],
            y=forecast_df[forecast_y],
            mode="lines",
            name="Forecast"
        )
    )

    return apply_layout(fig, title)


# =====================================================
# COUNTRY COMPARISON
# =====================================================

def country_comparison_chart(
    df,
    countries,
    metric,
    title
):

    filtered = df[
        df["country"].isin(countries)
    ]

    fig = px.line(
        filtered,
        x="year",
        y=metric,
        color="country"
    )

    return apply_layout(fig, title)


# =====================================================
# KPI CARD HELPER
# =====================================================

def format_number(value):

    try:

        if value >= 1_000_000_000:
            return f"{value/1_000_000_000:.2f}B"

        if value >= 1_000_000:
            return f"{value/1_000_000:.2f}M"

        if value >= 1_000:
            return f"{value/1_000:.2f}K"

        return f"{value:.2f}"

    except:
        return value


# =====================================================
# DECARBONISATION LEADERS
# =====================================================

def decarbonisation_chart(
    df,
    title="Top Decarbonisation Countries"
):

    fig = px.bar(
        df,
        x="country",
        y="decarbonisation_score",
        color="decarbonisation_score",
        text_auto=".2f"
    )

    fig.update_xaxes(
        tickangle=-45
    )

    return apply_layout(fig, title)


# =====================================================
# CO2 ANALYTICS
# =====================================================

def co2_emissions_chart(
    df,
    title
):

    fig = px.area(
        df,
        x="year",
        y="co2_mtonne"
    )

    return apply_layout(fig, title)


# =====================================================
# NUCLEAR VS RENEWABLES
# =====================================================

def nuclear_vs_renewables_chart(
    df
):

    fig = px.scatter(
        df,
        x="renewables_electricity",
        y="nuclear_electricity",
        size="population",
        color="decarbonisation_score",
        hover_name="country"
    )

    return apply_layout(
        fig,
        "Nuclear vs Renewables"
    )
