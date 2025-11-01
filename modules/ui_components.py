# modules/ui_components.py
import streamlit as st
import plotly.express as px
import pandas as pd

def render_weather_card(weather):
    st.subheader("🌦️ Cuaca Saat Ini")
    if not weather:
        st.info("Cuaca tidak tersedia — periksa konfigurasi API key di Streamlit Secrets.")
        return
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Kota", weather.get("city", "—"))
    col2.metric("Suhu", f"{weather.get('temperature', '—')} °C")
    col3.metric("Kelembapan", f"{weather.get('humidity', '—')}%")
    col4.metric("Angin", f"{weather.get('wind_speed', '—')} m/s")
    st.caption(f"Terakhir diperbarui: {weather.get('timestamp')}")

def render_flood_chart(summary_df: pd.DataFrame):
    st.subheader("📊 Statistik Status Banjir")
    if summary_df is None or summary_df.empty:
        st.info("Tidak ada data statistik banjir.")
        return
    fig = px.bar(summary_df, x="Status", y="Jumlah Lokasi", color="Status",
                 color_discrete_map={"Normal": "green", "Waspada": "orange", "Siaga": "red"})
    st.plotly_chart(fig, use_container_width=True)
