import folium
from streamlit_folium import st_folium

def render_flood_map(df):
    """Render interactive flood map using Folium."""
    st_map = folium.Map(location=[-6.2, 106.816666], zoom_start=11)
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=8,
            color=row["status_color"],
            fill=True,
            fill_opacity=0.7,
            popup=f"{row['location']} - {row['status']}"
        ).add_to(st_map)
    st_folium(st_map, width=700, height=450)
