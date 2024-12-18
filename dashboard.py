# -*- coding: utf-8 -*-
"""Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1p9fy8wlPk4ydxMuY4dBKKpWnBZJNsZOw
"""

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


# Sidebar widgets for filtering
start_year = st.sidebar.slider('Start Year', min_value=total_nonfarm_employment['Date'].dt.year.min(), max_value=total_nonfarm_employment['Date'].dt.year.max(), value=total_nonfarm_employment['Date'].dt.year.min())
end_year = st.sidebar.slider('End Year', min_value=total_nonfarm_employment['Date'].dt.year.min(), max_value=total_nonfarm_employment['Date'].dt.year.max(), value=total_nonfarm_employment['Date'].dt.year.max())

# Filter data based on selected years
total_nonfarm_employment = total_nonfarm_employment[(total_nonfarm_employment['Date'].dt.year >= start_year) & (total_nonfarm_employment['Date'].dt.year <= end_year)]
unemployment_rate = unemployment_rate[(unemployment_rate['Date'].dt.year >= start_year) & (unemployment_rate['Date'].dt.year <= end_year)]
imports = imports[(imports['Date'].dt.year >= start_year) & (imports['Date'].dt.year <= end_year)]
exports = exports[(exports['Date'].dt.year >= start_year) & (exports['Date'].dt.year <= end_year)]

#Aggregate unemployment data by quarter & calculate change
unemployment_rate['Quarter'] = unemployment_rate['Date'].dt.to_period('Q')
quarterly_unemployment = unemployment_rate.groupby('Quarter').mean().reset_index()
quarterly_unemployment['QoQ Change'] = quarterly_unemployment['Value'].pct_change() * 100

current_unemployment = quarterly_unemployment.iloc[-1]['Value']
recent_qoq_change = quarterly_unemployment.iloc[-1]['QoQ Change']


# Side-by-side visualizations
col1, col2 = st.columns(2)

#Viz 1: Unemployment Rate Quarter-over-Quarter Change
st.header(f'Current Unemployment Rate: {current_unemployment:.2f}%')
st.subheader(f'Quarter-over-Quarter Change: {recent_qoq_change:.2f}%')
fig = px.bar(quarterly_unemployment, x='Quarter', y='QoQ Change', title='Quarter-over-Quarter Change in Unemployment Rate')
st.plotly_chart(fig)

# Viz 3: Unemployment Rate over Time
st.header('Unemployment Rate over Time')
fig2 = px.line(unemployment_rate, x='Date', y='Value', title='Unemployment Rate over Time')
st.plotly_chart(fig2)

# Viz 2: Total Nonfarm Employment over Time
st.header('Total Nonfarm Employment over Time')
fig1 = px.line(total_nonfarm_employment, x='Date', y='Value', title='Total Nonfarm Employment over Time')
st.plotly_chart(fig1)

# Viz 4: Comparison of Imports and Exports over Time
st.header('Comparison of Imports and Exports over Time')
imports['Type'] = 'Imports'
exports['Type'] = 'Exports'
trade_data = pd.concat([imports, exports])
fig3 = px.line(trade_data, x='Date', y='Value', color='Type', title='Comparison of Imports and Exports over Time')
st.plotly_chart(fig3)