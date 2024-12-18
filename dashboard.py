
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

# Visualization 1: Total Nonfarm Employment over Time
#st.header('Total Nonfarm Employment over Time')
fig1 = px.line(total_nonfarm_employment, x='Date', y='Value', title='Total Nonfarm Employment over Time')
#st.plotly_chart(fig1)

# Visualization 2: Unemployment Rate over Time
#st.header('Unemployment Rate over Time')
fig2 = px.line(unemployment_rate, x='Date', y='Value', title='Unemployment Rate over Time')
#st.plotly_chart(fig2)

# Visualization 3: Comparison of Imports and Exports over Time
#st.header('Comparison of Imports and Exports over Time')
imports['Type'] = 'Imports'
exports['Type'] = 'Exports'
trade_data = pd.concat([imports, exports])
fig3 = px.line(trade_data, x='Date', y='Value', color='Type', title='Comparison of Imports and Exports over Time')
#st.plotly_chart(fig3)

# Display visualizations horizontally
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    st.plotly_chart(fig3, use_container_width=True)
