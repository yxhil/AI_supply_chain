import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")
st.title("📊 AI-Driven Supply Chain Dashboard")

# API base
API_BASE = "http://192.168.97.17:8000"

# --- Helper functions to fetch data ---
@st.cache_data
def get_forecast():
    try:
        response = requests.get(f"{API_BASE}/forecast")
        return pd.DataFrame(response.json())
    except:
        return pd.DataFrame()

@st.cache_data
def get_warehouse():
    try:
        response = requests.get(f"{API_BASE}/warehouse")
        return pd.DataFrame(response.json())
    except:
        return pd.DataFrame()

@st.cache_data
def get_emissions():
    try:
        response = requests.get(f"{API_BASE}/emissions")
        return pd.DataFrame(response.json())
    except:
        return pd.DataFrame()


# --- Forecast vs Actual ---
st.subheader("🔮 Demand Forecast vs Actual")
forecast_df = get_forecast()

if not forecast_df.empty:
    forecast_df["date"] = pd.to_datetime(forecast_df["date"])
    forecast_df = forecast_df.set_index("date")
    st.line_chart(forecast_df[["actual", "forecast"]])
else:
    st.error("⚠️ Could not fetch forecast data")


# --- Warehouse Stock Levels ---
st.subheader("🏭 Warehouse Stock Levels")
wh_df = get_warehouse()

if not wh_df.empty:
    st.bar_chart(wh_df.set_index("warehouse")["stock"])
    st.dataframe(wh_df)  # Show stock + stockouts
else:
    st.error("⚠️ Could not fetch warehouse data")


# --- CO₂ Emissions ---
st.subheader("🌱 CO₂ Emissions Over Time")
em_df = get_emissions()

if not em_df.empty:
    em_df["date"] = pd.to_datetime(em_df["date"])
    em_df = em_df.set_index("date")
    st.line_chart(em_df["emissions"])
else:
    st.error("⚠️ Could not fetch emissions data")
