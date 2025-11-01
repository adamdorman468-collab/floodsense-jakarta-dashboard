# app.py
import streamlit as st
from modules.data_fetcher import fetch_weather_openweathermap, fetch_flood_data
from modules.data_processor import process_flood_data, summarize_flood_stats
from modules.ui_components import render_weather_card, render_flood_chart
from modules.map_view import render_flood_map
from modules.utils import info_user

st.set_page_config(page_title="FloodSense", layout="wide", page_icon="🌊")

# --- Header / Intro ---
with st.container():
    col1, col2 = st.columns([6,1])
    with col1:
        st.title("🌊 FloodSense")
        st.markdown("**Real-Time Flood & Weather Dashboard — Jakarta**  \n"
                    "Data driven visualization to increase awareness and preparedness.")
    with col2:
        st.image("assets/logo.png" if (st.runtime.exists("assets/logo.png") if hasattr(st.runtime, 'exists') else False) else None, width=60)

st.sidebar.header("Navigasi")
page = st.sidebar.radio("Pilih Halaman:", ["Dashboard Utama", "Data Cuaca", "Statistik", "Tentang & Kredit"])

# Fetch data once and cache
@st.cache_data(ttl=300)
def _fetch_all():
    weather = fetch_weather_openweathermap("Jakarta")
    flood_df = fetch_flood_data()
    return weather, flood_df

weather_data, flood_df = _fetch_all()
flood_df = process_flood_data(flood_df)
summary_df = summarize_flood_stats(flood_df)

if page == "Dashboard Utama":
    st.header("Overview")
    col1, col2 = st.columns([3,2])
    with col1:
        render_flood_map(flood_df)
    with col2:
        st.markdown("### Ringkasan Cepat")
        if flood_df is None or flood_df.empty:
            st.info("Data banjir tidak tersedia saat ini.")
        else:
            st.write(f"Lokasi terdata: **{len(flood_df)}**")
            last_update = flood_df["updated_at"].max()
            st.write(f"Terakhir update (terbesar): **{last_update}**")
        render_weather_card(weather_data)

elif page == "Data Cuaca":
    st.header("Data Cuaca Jakarta")
    render_weather_card(weather_data)
    st.markdown("---")
    st.markdown("Sumber: OpenWeatherMap (konfigurasi API key via Streamlit Secrets).")

elif page == "Statistik":
    st.header("Statistik & Tren")
    render_flood_chart(summary_df)
    st.markdown("Tabel ringkasan:")
    st.dataframe(summary_df)

elif page == "Tentang & Kredit":
    st.header("Tentang FloodSense")
    st.markdown("""
    FloodSense dibangun oleh **Adam Dorman — Mahasiswa S1 Sistem Informasi UPNVJ (Angkatan 2024)**.
    Tujuan: menyediakan dasbor edukatif untuk meningkatkan kesadaran dan mitigasi risiko banjir di Jakarta.
    """)
    st.markdown("**Kredit & Teknologi**")
    st.markdown("- Backend/Frontend: Python + Streamlit\n- Visualisasi: Plotly, Folium\n- Data: Open public APIs / fallback sample\n- AI-assisted development: IBM Granite / GPT used during code generation")
    st.markdown("---")
    st.markdown("**Catatan Pengguna**")
    st.info("Untuk menampilkan data cuaca real-time, pastikan `OPENWEATHERMAP_API_KEY` diset di Streamlit Secrets. "
            "Jika kamu mempunyai endpoint banjir publik, letakkan URL sebagai `FLOOD_API_URL` di Secrets juga.")
    st.markdown("**Contact / Repo**: https://github.com/AdamDorman/floodsense-jakarta-dashboard")
    st.caption("© 2025 Adam Dorman — FloodSense. Built for UPNVJ Capstone.")
