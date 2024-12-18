
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BLS Dashboard", layout="wide")

# Load data
#@st.cache_data
total_nonfarm_employment = pd.read_csv('bls_data_files/Total_Nonfarm_Employment.csv')
unemployment_rate = pd.read_csv('bls_data_files/Unemployment_Rate.csv')
imports = pd.read_csv('bls_data_files/Imports.csv')
exports = pd.read_csv('bls_data_files/Exports.csv')

# Convert 'Year' and 'Period' to datetime
total_nonfarm_employment['Date'] = pd.to_datetime(total_nonfarm_employment['Year'].astype(str) + total_nonfarm_employment['Period'].str[1:], format='%Y%m')
unemployment_rate['Date'] = pd.to_datetime(unemployment_rate['Year'].astype(str) + unemployment_rate['Period'].str[1:], format='%Y%m')
imports['Date'] = pd.to_datetime(imports['Year'].astype(str) + imports['Period'].str[1:], format='%Y%m')
exports['Date'] = pd.to_datetime(exports['Year'].astype(str) + exports['Period'].str[1:], format='%Y%m')

# Add title and overview
st.title("BLS Dashboard")
st.markdown(
    """
    This dashboard provides insights visually based on data published monthly from the Bureau of Labor Statistics (BLS):
    
    - **Total Nonfarm Employment**: Trends in employment levels across various sectors.
    - **Unemployment Rate**: Historical unemployment rates over time.
    - **Trade Analysis**: Comparison of imports and exports.
    """
)

# Add sidebar filters
st.sidebar.header("Filter Data")
all_years = sorted(total_nonfarm_employment['Date'].dt.year.unique())
start_year = st.sidebar.selectbox("Start Year", options=all_years, index=0)
end_year = st.sidebar.selectbox("End Year", options=all_years, index=len(all_years) - 1)

# Filter data based on year range
filtered_total_nonfarm_employment = total_nonfarm_employment[(total_nonfarm_employment['Date'].dt.year >= start_year) & (total_nonfarm_employment['Date'].dt.year <= end_year)]
filtered_unemployment_rate = unemployment_rate[(unemployment_rate['Date'].dt.year >= start_year) & (unemployment_rate['Date'].dt.year <= end_year)]
filtered_imports = imports[(imports['Date'].dt.year >= start_year) & (imports['Date'].dt.year <= end_year)]
filtered_exports = exports[(exports['Date'].dt.year >= start_year) & (exports['Date'].dt.year <= end_year)]

# Color palette
color_palette = px.colors.qualitative.Dark24

# Vis 1: Total Nonfarm Employment over Time
fig1 = px.line(
    filtered_total_nonfarm_employment, 
    x='Date', y='Value', 
    title='Total Nonfarm Employment over Time',
    labels={"Value": "Employment (in thousands)", "Date": "Date"},
    color_discrete_sequence=[color_palette[0]]
)

# Vis 2: Unemployment Rate over Time
fig2 = px.line(
    filtered_unemployment_rate, 
    x='Date', y='Value', 
    title='Unemployment Rate over Time',
    labels={"Value": "Unemployment Rate (%)", "Date": "Date"},
    color_discrete_sequence=[color_palette[1]]
)

# Vis 3: Comparison of Imports and Exports over Time
filtered_imports['Type'] = 'Imports'
filtered_exports['Type'] = 'Exports'
filtered_trade_data = pd.concat([filtered_imports, filtered_exports])
fig3 = px.line(
    filtered_trade_data, 
    x='Date', y='Value', color='Type', 
    title='Comparison of Imports and Exports over Time',
    labels={"Value": "Value (in millions)", "Date": "Date", "Type": "Trade Type"},
    color_discrete_sequence=[color_palette[2], color_palette[3]]
)

# Display visualizations horizontally
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    st.plotly_chart(fig3, use_container_width=True)


# Add custom theme styles
st.markdown(
    """
    <style>
    .css-18e3th9 {
        background-color: #121212;
        color: #ffffff;
    }
    .css-1d391kg {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 5px;
        padding: 10px;
        color: #ffffff;
    }
    h1 {
        color: #bb86fc;
    }
    .stPlotlyChart div {
        background-color: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
