"""
Home page - shows when data is loaded in main app
This file can remain simple or redirect to main app
"""

import streamlit as st
from styles import apply_global_styles

st.set_page_config(page_title="Home", layout="wide", page_icon="🏠")
apply_global_styles()

st.title("🏠 Home")
st.info("👈 Go back to the main app page to load data first!")
