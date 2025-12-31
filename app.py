import streamlit as st

st.set_page_config(
    page_title="UMK Sleep & Academic Performance Dashboard",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define pages with modern icons
home = st.Page("home.py", title="Overview", icon="🏠", default=True)
aleya_aelyana = st.Page("page_aleya_aelyana.py", title="Sleep & Insomnia Patterns", icon="🛌")
aleya_nazifa = st.Page("page_aleya_nazifa.py", title="Academic Impact Analysis", icon="📚")
nash = st.Page("page_nash.py", title="Lifestyle & Stress Factors", icon="⚙️")

# Navigation
pg = st.navigation({
    "Dashboard": [home, aleya_aelyana, aleya_nazifa, nash]
})

pg.run()
