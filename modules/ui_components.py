import streamlit as st
import plotly.express as px

def render_weather_card(weather):
    st.subheader("🌦️ Cuaca Saat Ini")
    st.metric("Kota", weather["city"])
    st.metric("Suhu", f"{weather['temperature']} °C")
    st.metric("Kelembapan", f"{weather['humidity']}%")
    st.metric("Kondisi", weather["description"].capitalize())
    st.metric("Kecepatan Angin", f"{weather['wind_speed']} m/s")


def render_flood_chart(summary_df):
    st.subheader("📊 Statistik Status Banjir")
    fig = px.bar(summary_df, x="Status", y="Jumlah Lokasi", color="Status",
                 color_discrete_map={"Normal": "green", "Waspada": "orange", "Siaga": "red"})
    st.plotly_chart(fig, use_container_width=True)
