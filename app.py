import streamlit as st

st.set_page_config(
    page_title="UMK Insomnia Dashboard",
    page_icon="😴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Optional styling (safe)
st.markdown(
    """
<style>
[data-testid="stSidebar"] {background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%);}
[data-testid="stSidebar"] * {color: white !important;}
h1 {font-weight: 800;}
</style>
""",
    unsafe_allow_html=True,
)

home = st.Page("home.py", title="Overview", icon="🏠", default=True)
aleya_aelyana = st.Page("page_aleya_aelyana.py", title="Sleep Patterns", icon="😴")
aleya_nazifa = st.Page("page_aleya_nazifa.py", title="Academic Impact", icon="📚")
nash = st.Page("page_nash.py", title="Lifestyle Factors", icon="🏃")

pg = st.navigation({"📊 Dashboard": [home, aleya_aelyana, aleya_nazifa, nash]})
pg.run()
