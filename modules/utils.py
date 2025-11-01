import streamlit as st

def handle_error(source, error):
    st.warning(f"⚠️ {source} data unavailable: {error}")
