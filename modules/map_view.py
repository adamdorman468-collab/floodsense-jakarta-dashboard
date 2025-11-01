# modules/map_view.py
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import streamlit as st

def render_flood_map(df, center=[-6.2, 106.816666], zoom_start=11):
    st.subheader("🗺️ Peta Banjir Jakarta")
    m = folium.Map(location=center, zoom_start=zoom_start)
    cluster = MarkerCluster().add_to(m)
    if df is None or df.empty:
        st.info("Data titik banjir tidak tersedia. Menampilkan peta dasar.")
        st_folium(m, width="100%", height=550)
        return

    added = 0
    for _, row in df.iterrows():
        lat = row.get("lat")
        lon = row.get("lon")
        if lat is None or lon is None or pd.isna(lat) or pd.isna(lon):
            continue
        popup_text = f"<b>{row.get('location')}</b><br>Status: {row.get('status')}<br>Terakhir: {row.get('updated_at')}"
        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            color=row.get("status_color", "blue"),
            fill=True,
            fill_opacity=0.7,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(cluster)
        added += 1

    if added == 0:
        st.info("Tidak ditemukan koordinat valid pada data banjir. Menampilkan peta dasar.")
    st_folium(m, width="100%", height=550)

