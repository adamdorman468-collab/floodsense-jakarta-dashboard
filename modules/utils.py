# modules/utils.py
import streamlit as st
import logging

logger = logging.getLogger("floodsense")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def warn_user(msg: str):
    st.warning(msg)

def info_user(msg: str):
    st.info(msg)

def log_error(source: str, exc: Exception):
    logger.exception("Error in %s: %s", source, exc)
    warn_user(f"⚠️ {source} error: {exc}")
