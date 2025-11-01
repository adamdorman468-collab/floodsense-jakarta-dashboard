import os
import streamlit as st
from modules.data_fetcher import fetch_weather_openweathermap, fetch_flood_data
from modules.data_processor import process_flood_data, summarize_flood_stats
from modules.ui_components import render_weather_card, render_flood_chart
from modules.map_view import render_flood_map
from modules.utils import info_user

# ==============================
# Streamlit App Config
# ==============================
st.set_page_config(
    page_title="FloodSense — Jakarta Dashboard",
    page_icon="🌊",
    layout="wide"
)

# ==============================
# Header / Hero Section
# ==============================
with st.container():
    st.markdown(
        """
        <div style="
            background: linear-gradient(90deg, #0b6fa6 0%, #3aaed8 100%);
            border-radius: 12px;
            padding: 25px 30px;
            color: white;
        ">
            <h1 style="margin-bottom:0;">🌊 FloodSense</h1>
            <h4 style="margin-top:5px;">Real-Time Flood & Weather Dashboard — Jakarta</h4>
            <p style="margin-top:10px; font-size:15px;">
                Data-driven visualization to increase awareness, preparedness, and urban resilience.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==============================
# Sidebar Navigation
# ==============================
st.sidebar.header("📍 Navigasi")
page = st.sidebar.radio(
    "Pilih Halaman:",
    ["Dashboard Utama", "Data Cuaca", "Statistik", "Tentang & Kredit"]
)

# ==============================
# Data Fetching (with caching)
# ==============================
@st.cache_data(ttl=300)
def _fetch_all():
    weather = fetch_weather_openweathermap("Jakarta")
    flood_df = fetch_flood_data()
    return weather, flood_df

weather_data, flood_df = _fetch_all()
flood_df = process_flood_data(flood_df)
summary_df = summarize_flood_stats(flood_df)

# ==============================
# ROUTING
# ==============================
if page == "Dashboard Utama":
    st.subheader("📊 Ringkasan Utama")
    col1, col2 = st.columns([3, 2])

    with col1:
        render_flood_map(flood_df)

    with col2:
        st.markdown("### Kondisi Umum")
        if flood_df is None or flood_df.empty:
            st.info("Belum ada data banjir tersedia saat ini.")
        else:
            total = len(flood_df)
            last_update = flood_df["updated_at"].max()
            st.metric("Jumlah Lokasi Terdata", f"{total}")
            st.metric("Terakhir Diperbarui", str(last_update)[:19])
        st.markdown("---")
        render_weather_card(weather_data)

elif page == "Data Cuaca":
    st.subheader("🌦️ Kondisi Cuaca Jakarta")
    render_weather_card(weather_data)
    st.markdown("---")
    st.markdown(
        """
        **Sumber Data:** [OpenWeatherMap](https://openweathermap.org/api)  
        Konfigurasikan API key melalui **Streamlit Secrets** (`OPENWEATHERMAP_API_KEY`).
        """
    )

elif page == "Statistik":
    st.subheader("📈 Statistik & Tren")
    render_flood_chart(summary_df)
    st.markdown("#### Tabel Ringkasan Status Banjir")
    st.dataframe(summary_df, use_container_width=True)

elif page == "Tentang & Kredit":
    st.subheader("ℹ️ Tentang FloodSense")
    st.markdown(
        """
        **FloodSense** adalah aplikasi berbasis *data visualization* yang dikembangkan oleh  
        **Adam Dorman — Mahasiswa S1 Sistem Informasi UPNVJ (Angkatan 2024)**.  
        Tujuan aplikasi ini adalah menyediakan akses terbuka terhadap informasi banjir dan cuaca di Jakarta secara real-time, 
        untuk meningkatkan kesadaran masyarakat terhadap mitigasi bencana.

        ---
        **Teknologi yang Digunakan**
        - 🐍 Python + Streamlit (Frontend & Backend)
        - 📊 Plotly & Folium (Visualisasi Data)
        - 🌤️ OpenWeatherMap API
        - 💧 Jakarta SmartCity API / fallback data

        ---
        **AI Support**
        Proses pengembangan aplikasi ini dibantu dengan AI (IBM Granite & GPT-5)  
        untuk mempercepat code generation, dokumentasi, dan optimisasi.

        ---
        **Kontak & Repository**
        - GitHub: [FloodSense Repository](https://github.com/AdamDorman/floodsense-jakarta-dashboard)
        - Created © 2025 by Adam Dorman — UPN Veteran Jakarta.
        """
    )

# ==============================
# Footer
# ==============================
st.markdown(
    """
    <hr style="margin-top:40px;margin-bottom:10px;">
    <div style="text-align:center; font-size:13px; color:gray;">
        Built with ❤️ using Streamlit — FloodSense by Adam Dorman (UPNVJ 2024)
    </div>
    """,
    unsafe_allow_html=True
)
