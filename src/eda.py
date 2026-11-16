"""
Exploratory Data Analysis (EDA) Module
DS2004: Fundamentals of Data Science
Project: Tourist Demand Pattern Analysis Across Indian Destinations

Provides:
1. Static publication-quality plots (Matplotlib/Seaborn saved to outputs/figures/)
2. Dynamic interactive Plotly figures for Streamlit dashboard
3. Statistical summaries and correlation analysis
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

FIGURES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs", "figures")

# Styling configurations
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8


# ==========================================================
# 1. STATIC VISUALIZATION GENERATORS (Outputs to figures/)
# ==========================================================

def generate_static_eda_figures():
    """Generates and saves all required static EDA charts."""
    os.makedirs(FIGURES_DIR, exist_ok=True)
    
    from src.cleaner import clean_all_and_save
    from src.feature_engineering import engineer_all_and_save
    
    processed = clean_all_and_save()
    df_dest = engineer_all_and_save()
    df_state = processed["statewise"]
    df_qtr = processed["quarterly"]
    df_fta = processed["fta"]
    
    # 1. Yearly Tourism Trends (1981-2020)
    plt.figure(figsize=(10, 5))
    valid_fta = df_fta.dropna(subset=['FTAs_Million'])
    plt.plot(valid_fta['Year'], valid_fta['FTAs_Million'], marker='o', color='#1f77b4', linewidth=2.5, label='FTAs (Millions)')
    plt.fill_between(valid_fta['Year'], valid_fta['FTAs_Million'], color='#1f77b4', alpha=0.15)
    plt.title('Longitudinal Foreign Tourist Arrivals in India (1981–2020)', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Year', fontsize=11)
    plt.ylabel('FTAs (Million Visitors)', fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.annotate('COVID-19 Pandemic Drop (2020)', xy=(2020, valid_fta[valid_fta['Year']==2020]['FTAs_Million'].values[0]),
                 xytext=(2010, 8), arrowprops=dict(facecolor='red', shrink=0.05, width=1.5, headwidth=8),
                 fontweight='bold', color='#b22222')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "yearly_tourism_trends.png"), dpi=300)
    plt.close()
    
    # 2. Seasonal Quarterly Trends
    plt.figure(figsize=(10, 5))
    qtr_pivot = df_qtr.pivot(index='Year', columns='Quarter', values='Arrival_Share_Pct')
    palette = ['#2ca02c', '#d62728', '#1f77b4', '#ff7f0e']
    for i, col in enumerate(['Q1', 'Q2', 'Q3', 'Q4']):
        labels = {'Q1': 'Q1 (Jan-Mar: Winter)', 'Q2': 'Q2 (Apr-Jun: Summer)', 'Q3': 'Q3 (Jul-Sep: Monsoon)', 'Q4': 'Q4 (Oct-Dec: Post-Monsoon)'}
        plt.plot(qtr_pivot.index, qtr_pivot[col], marker='s', label=labels[col], linewidth=2, color=palette[i])
    plt.title('Quarterly Seasonal Demand Share Over 19 Years (2001–2019)', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Year', fontsize=11)
    plt.ylabel('Percentage Share (%)', fontsize=11)
    plt.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "seasonal_quarterly_trends.png"), dpi=300)
    plt.close()
    
    # 3. State-wise Tourism Demand (Top 10 States)
    plt.figure(figsize=(11, 6))
    top10_states = df_state.sort_values(by='Total_Visits_2019', ascending=False).head(10)
    y_pos = np.arange(len(top10_states))
    plt.barh(y_pos, top10_states['Domestic_2019'] / 1e6, label='Domestic (Million)', color='#3b82f6', height=0.6)
    plt.barh(y_pos, top10_states['Foreign_2019'] / 1e6, left=top10_states['Domestic_2019'] / 1e6, label='Foreign (Million)', color='#f59e0b', height=0.6)
    plt.yticks(y_pos, top10_states['State'], fontsize=10)
    plt.gca().invert_yaxis()
    plt.xlabel('Tourist Visits (in Millions)', fontsize=11)
    plt.title('Top 10 Indian States by Tourism Demand Volume (2019 Baseline)', fontsize=13, fontweight='bold', pad=12)
    plt.legend(frameon=True, loc='lower right')
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "statewise_tourism_demand.png"), dpi=300)
    plt.close()
    
    # 4. Top 15 Destinations / Monuments
    plt.figure(figsize=(11, 7))
    top15_dest = df_dest.sort_values(by='Total_Tourist_Visits', ascending=False).head(15)
    sns.barplot(data=top15_dest, y='Monument_Name', x='Total_Tourist_Visits', hue='Is_UNESCO_Site',
                palette={1: '#10b981', 0: '#6366f1'}, dodge=False)
    plt.title('Top 15 Most Visited Indian Destinations (ASI Centrally Protected)', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Total Annual Footfall (Visitors)', fontsize=11)
    plt.ylabel('')
    plt.legend(title='UNESCO Status', labels=['UNESCO Site', 'Non-UNESCO'], loc='lower right')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "top_destinations_footfall.png"), dpi=300)
    plt.close()
    
    # 5. Outliers Before & After Treatment (Boxplots)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.boxplot(y=df_dest['Total_Tourist_Visits'] / 1e3, ax=axes[0], color='#ef4444')
    axes[0].set_title('Raw Visits Distribution (Severe Right Skew & Outliers)', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('Visits (in Thousands)')
    
    sns.boxplot(y=df_dest['Log_Total_Visits'], ax=axes[1], color='#3b82f6')
    axes[1].set_title('Treated: Log-Transformed Visits [ln(1 + Visits)]', fontsize=11, fontweight='bold')
    axes[1].set_ylabel('Log(Visits)')
    plt.suptitle('Outlier Detection & Logarithmic Treatment Comparison', fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "outliers_boxplot_before_after.png"), dpi=300)
    plt.close()
    
    # 6. Temperature vs Tourist Demand
    plt.figure(figsize=(9, 5.5))
    sns.regplot(data=df_dest, x='Annual_Avg_Temp_C', y='Log_Total_Visits',
                scatter_kws={'alpha': 0.65, 'color': '#0284c7', 's': 55},
                line_kws={'color': '#dc2626', 'linewidth': 2})
    plt.axvline(22.0, color='#16a34a', linestyle='--', linewidth=1.5, label='Optimal Thermal Comfort (~22°C)')
    plt.title('Relationship Between Destination Average Temperature and Tourist Demand', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Annual Average Temperature (°C)', fontsize=11)
    plt.ylabel('Log Tourist Visits', fontsize=11)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "weather_temperature_vs_visits.png"), dpi=300)
    plt.close()
    
    # 7. Rainfall vs Tourist Demand
    plt.figure(figsize=(9, 5.5))
    sns.regplot(data=df_dest, x='Annual_Total_Rainfall_mm', y='Log_Total_Visits',
                scatter_kws={'alpha': 0.65, 'color': '#0d9488', 's': 55},
                line_kws={'color': '#f97316', 'linewidth': 2})
    plt.title('Relationship Between Annual Precipitation and Destination Tourist Demand', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Annual Total Rainfall (mm)', fontsize=11)
    plt.ylabel('Log Tourist Visits', fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "weather_rainfall_vs_visits.png"), dpi=300)
    plt.close()
    
    # 8. Correlation Heatmap
    plt.figure(figsize=(10, 8))
    corr_cols = [
        'Total_Tourist_Visits', 'Log_Total_Visits', 'Domestic_Tourist_Share', 'Foreign_Tourist_Share',
        'Tourist_Growth_Rate_Domestic', 'Annual_Avg_Temp_C', 'Annual_Total_Rainfall_mm',
        'Temp_Ideal_Deviation', 'Monsoon_Rainfall_mm', 'Is_UNESCO_Site'
    ]
    corr_df = df_dest[corr_cols].corr()
    mask = np.triu(np.ones_like(corr_df, dtype=bool))
    sns.heatmap(corr_df, mask=mask, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1,
                linewidths=0.5, cbar_kws={'shrink': 0.8})
    plt.title('Correlation Matrix: Tourism Demand, Tourist Mix & Weather Metrics', fontsize=13, fontweight='bold', pad=14)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "correlation_heatmap.png"), dpi=300)
    plt.close()
    
    # 9. Destination Typology Demand
    plt.figure(figsize=(10, 5.5))
    order = df_dest.groupby('Destination_Type')['Total_Tourist_Visits'].median().sort_values(ascending=False).index
    sns.boxplot(data=df_dest, x='Destination_Type', y='Log_Total_Visits', order=order, palette='Set2')
    plt.title('Tourist Demand Across Destination Typologies', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Structural & Cultural Typology', fontsize=11)
    plt.ylabel('Log Tourist Visits', fontsize=11)
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "destination_typology_demand.png"), dpi=300)
    plt.close()
    
    logger.info(f"All static publication-grade EDA figures saved to: {FIGURES_DIR}")


# ==========================================================
# 2. INTERACTIVE PLOTLY VISUALIZATIONS (For Streamlit UI)
# ==========================================================
# 2. INTERACTIVE PLOTLY VISUALIZATIONS (For Streamlit UI)
# ==========================================================

def apply_dark_theme(fig):
    """
    Apply a consistent dark theme to Plotly figures.
    Does not modify the underlying data.
    """
    if fig is None:
        return fig

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Plus Jakarta Sans, Inter, Arial, sans-serif",
            color="#E5E7EB"
        ),
        title_font=dict(
            family="Outfit, sans-serif",
            size=18,
            color="#FFFFFF"
        ),
        legend=dict(
            bgcolor="rgba(15, 23, 42, 0.65)",
            bordercolor="rgba(255, 255, 255, 0.1)",
            font=dict(color="#E5E7EB")
        ),
        margin=dict(
            l=30,
            r=30,
            t=60,
            b=30
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False
    )

    return fig


def get_yearly_trends_plot(df_fta: pd.DataFrame) -> go.Figure:
    """Returns interactive Plotly figure for longitudinal FTA trends."""
    fig = go.Figure()
    valid = df_fta.dropna(subset=['FTAs_Million'])
    fig.add_trace(go.Scatter(
        x=valid['Year'], y=valid['FTAs_Million'],
        mode='lines+markers', name='Foreign Tourist Arrivals (M)',
        line=dict(color='#38bdf8', width=3),
        marker=dict(size=7, color='#0284c7'),
        hovertemplate='<b>Year:</b> %{x}<br><b>FTAs:</b> %{y:.2f} Million<extra></extra>'
    ))
    fig.update_layout(
        title='<b>Longitudinal Foreign Tourist Arrivals in India (1981–2020)</b>',
        xaxis_title='Year', yaxis_title='Arrivals (Millions)',
        hovermode='x unified'
    )
    return apply_dark_theme(fig)


def get_seasonal_trends_plot(df_qtr: pd.DataFrame) -> go.Figure:
    """Returns interactive Plotly figure for quarterly seasonal demand distribution."""
    fig = px.line(
        df_qtr, x='Year', y='Arrival_Share_Pct', color='Season',
        color_discrete_map={'Winter': '#10b981', 'Summer': '#f43f5e', 'Monsoon': '#38bdf8', 'Post-Monsoon': '#fbbf24'},
        markers=True,
        title='<b>19-Year Seasonal Demand Distribution (% Share by Season)</b>'
    )
    fig.update_layout(
        xaxis_title='Year', yaxis_title='Seasonal Share (%)',
        hovermode='x unified'
    )
    return apply_dark_theme(fig)


def get_statewise_demand_plot(df_state: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """Returns interactive stacked horizontal bar chart of top states by tourist arrivals."""
    top_df = df_state.sort_values(by='Total_Visits_2019', ascending=False).head(top_n)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top_df['State'], x=top_df['Domestic_2019'] / 1e6,
        name='Domestic (M)', orientation='h', marker_color='#3b82f6',
        hovertemplate='%{y}: %{x:.2f}M Domestic<extra></extra>'
    ))
    fig.add_trace(go.Bar(
        y=top_df['State'], x=top_df['Foreign_2019'] / 1e6,
        name='Foreign (M)', orientation='h', marker_color='#f59e0b',
        hovertemplate='%{y}: %{x:.2f}M Foreign<extra></extra>'
    ))
    fig.update_layout(
        barmode='stack',
        title=f'<b>Top {top_n} Indian States by Tourist Volume (2019 Baseline)</b>',
        xaxis_title='Tourist Visits (Millions)', yaxis=dict(autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return apply_dark_theme(fig)


def get_top_destinations_plot(df_dest: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """Returns interactive horizontal bar chart for top destinations."""
    top_df = df_dest.sort_values(by='Total_Tourist_Visits', ascending=False).head(top_n)
    fig = px.bar(
        top_df, y='Monument_Name', x='Total_Tourist_Visits',
        color='Foreign_Tourist_Share',
        color_continuous_scale='Turbo',
        labels={'Total_Tourist_Visits': 'Annual Footfall', 'Foreign_Tourist_Share': 'Foreign Share (%)', 'Monument_Name': 'Destination'},
        title=f'<b>Top {top_n} Indian Heritage Destinations by Annual Footfall</b>',
        hover_data=['Circle', 'State', 'Annual_Avg_Temp_C', 'Is_UNESCO_Site']
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    return apply_dark_theme(fig)


def get_domestic_vs_foreign_plot(df_dest: pd.DataFrame) -> go.Figure:
    """Returns scatter plot comparing domestic vs foreign tourist footfalls."""
    fig = px.scatter(
        df_dest, x='Domestic_2019_20', y='Foreign_2019_20',
        size='Total_Tourist_Visits', color='Is_UNESCO_Site',
        color_discrete_map={1: '#10b981', 0: '#818cf8'},
        hover_name='Monument_Name',
        hover_data=['Circle', 'State', 'Foreign_Tourist_Share', 'Annual_Avg_Temp_C'],
        log_x=True, log_y=True,
        title='<b>Domestic vs Foreign Tourist Visits (Log Scale)</b>',
        labels={'Domestic_2019_20': 'Domestic Visits (Log)', 'Foreign_2019_20': 'Foreign Visits (Log)', 'Is_UNESCO_Site': 'UNESCO Site'}
    )
    return apply_dark_theme(fig)


def get_weather_temp_scatter(df_dest: pd.DataFrame) -> go.Figure:
    """Returns interactive scatter plot of Temperature vs Tourist Demand."""
    fig = px.scatter(
        df_dest, x='Annual_Avg_Temp_C', y='Total_Tourist_Visits',
        color='Thermal_Comfort_Category',
        size='Foreign_Tourist_Share',
        hover_name='Monument_Name',
        hover_data=['Circle', 'State', 'Annual_Total_Rainfall_mm'],
        log_y=True,
        title='<b>Destination Average Temperature vs Tourist Footfall (Log Scale)</b>',
        labels={'Annual_Avg_Temp_C': 'Annual Avg Temperature (°C)', 'Total_Tourist_Visits': 'Total Tourist Visits (Log)'}
    )
    fig.add_vline(x=22.0, line_dash='dash', line_color='#10b981', annotation_text='Ideal Comfort (22°C)')
    return apply_dark_theme(fig)


def get_weather_rain_scatter(df_dest: pd.DataFrame) -> go.Figure:
    """Returns interactive scatter plot of Rainfall vs Tourist Demand."""
    fig = px.scatter(
        df_dest, x='Annual_Total_Rainfall_mm', y='Total_Tourist_Visits',
        color='Rainfall_Severity_Category',
        hover_name='Monument_Name',
        hover_data=['Circle', 'State', 'Monsoon_Rainfall_mm'],
        log_y=True,
        title='<b>Annual Precipitation vs Destination Tourist Footfall</b>',
        labels={'Annual_Total_Rainfall_mm': 'Annual Rainfall (mm)', 'Total_Tourist_Visits': 'Total Tourist Visits (Log)'}
    )
    return apply_dark_theme(fig)


def get_correlation_heatmap_plot(df_dest: pd.DataFrame) -> go.Figure:
    """Returns Plotly heatmap of feature correlations."""
    cols = [
        'Total_Tourist_Visits', 'Log_Total_Visits', 'Domestic_Tourist_Share', 'Foreign_Tourist_Share',
        'Tourist_Growth_Rate_Domestic', 'Annual_Avg_Temp_C', 'Annual_Total_Rainfall_mm',
        'Temp_Ideal_Deviation', 'Is_UNESCO_Site'
    ]
    corr = df_dest[cols].corr().round(2)
    fig = px.imshow(
        corr, text_auto=True, aspect="auto",
        color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
        title='<b>Correlation Heatmap: Tourism & Meteorological Variables</b>'
    )
    return apply_dark_theme(fig)


if __name__ == "__main__":
    generate_static_eda_figures()
