import streamlit as st
from modules.data_fetcher import fetch_weather, fetch_flood_data
from modules.data_processor import process_flood_data, summarize_flood_stats
from modules.ui_components import render_weather_card, render_flood_chart
from modules.map_view import render_flood_map

st.set_page_config(page_title="FloodSense", layout="wide", page_icon="🌊")

# --- Header ---
st.title("🌊 FloodSense")
st.caption("Real-Time Flood and Weather Dashboard for Jakarta")

# --- Sidebar ---
st.sidebar.header("Navigasi")
page = st.sidebar.radio("Pilih Halaman:", ["Dashboard Utama", "Data Cuaca", "Statistik"])

# --- Fetch Data ---
weather_data = fetch_weather("Jakarta")
flood_df = fetch_flood_data()
flood_df = process_flood_data(flood_df)
summary_df = summarize_flood_stats(flood_df)

# --- Routing ---
if page == "Dashboard Utama":
    st.header("🗺️ Peta Banjir Jakarta")
    render_flood_map(flood_df)
    st.info(f"Terakhir diperbarui: {flood_df['updated_at'].iloc[0].strftime('%Y-%m-%d %H:%M:%S')}")
elif page == "Data Cuaca":
    render_weather_card(weather_data)
elif page == "Statistik":
    render_flood_chart(summary_df)
    st.dataframe(summary_df)
