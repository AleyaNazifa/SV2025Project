import streamlit as st

def apply_global_styles():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Purple gradient background */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* White content box */
        .main .block-container {
            background-color: white;
            border-radius: 20px;
            padding: 3rem 2rem;
            margin: 2rem auto;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        /* ALL TEXT IN MAIN IS DARK */
        .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
            color: #1a202c !important;
        }
        
        .main p, .main span, .main div, .main li, .main label {
            color: #2d3748 !important;
        }
        
        .main strong {
            color: #1a202c !important;
        }
        
        /* Dark sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        }
        
        /* All sidebar text is WHITE */
        section[data-testid="stSidebar"] * {
            color: white !important;
        }
        
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: white !important;
            border-bottom: 2px solid #334155;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }
        
        /* Multiselect in sidebar */
        section[data-testid="stSidebar"] [data-baseweb="select"] {
            background-color: #0f172a !important;
            border: 1px solid #475569 !important;
        }
        
        section[data-testid="stSidebar"] input {
            color: white !important;
            background-color: #0f172a !important;
        }
        
        /* Blue pills for selected items */
        section[data-testid="stSidebar"] [data-baseweb="tag"] {
            background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 0.3rem 0.8rem !important;
            margin: 0.2rem !important;
        }
        
        section[data-testid="stSidebar"] [data-baseweb="tag"] span {
            color: white !important;
        }
        
        section[data-testid="stSidebar"] [data-baseweb="tag"] svg {
            fill: white !important;
        }
        
        /* Dropdown menu */
        [data-baseweb="popover"],
        [data-baseweb="menu"] {
            background-color: #1e293b !important;
        }
        
        [role="option"] {
            background-color: #1e293b !important;
            color: white !important;
        }
        
        [role="option"]:hover {
            background-color: #334155 !important;
        }
        
        /* Sidebar buttons */
        section[data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            width: 100%;
        }
        
        section[data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            transform: translateY(-2px);
        }
        
        /* Sidebar alerts */
        section[data-testid="stSidebar"] .stAlert {
            background: linear-gradient(135deg, #1e3a8a, #1e40af) !important;
            color: white !important;
            border: none !important;
        }
        
        section[data-testid="stSidebar"] .stAlert * {
            color: white !important;
        }
        
        /* Sidebar radio */
        section[data-testid="stSidebar"] .stRadio > div {
            background-color: #1e293b;
            padding: 0.75rem;
            border-radius: 8px;
            border: 1px solid #334155;
        }
        
        /* Metrics */
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, #f8fafc, #f1f5f9);
            padding: 1.5rem;
            border-radius: 12px;
            border: 2px solid #e2e8f0;
        }
        
        [data-testid="stMetricValue"] {
            color: #667eea !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
        }
        
        [data-testid="stMetricLabel"] {
            color: #475569 !important;
            font-weight: 600 !important;
        }
        
        /* Info boxes in main */
        .stInfo {
            background-color: #dbeafe !important;
            border-left: 4px solid #3b82f6 !important;
            color: #1e40af !important;
        }
        
        .stSuccess {
            background-color: #d1fae5 !important;
            border-left: 4px solid #10b981 !important;
            color: #065f46 !important;
        }
        
        .stWarning {
            background-color: #fef3c7 !important;
            border-left: 4px solid #f59e0b !important;
            color: #92400e !important;
        }
        
        .stError {
            background-color: #fee2e2 !important;
            border-left: 4px solid #ef4444 !important;
            color: #991b1b !important;
        }
        
        /* Dividers */
        hr {
            border: none;
            border-top: 2px solid #e5e7eb;
            margin: 2rem 0;
        }
        
        /* Insight boxes */
        .insight-box {
            background: linear-gradient(135deg, #eff6ff, #dbeafe);
            border-left: 4px solid #3b82f6;
            border-radius: 10px;
            padding: 1.25rem 1.5rem;
            margin: 1.5rem 0;
        }
        
        .insight-box strong {
            color: #1e40af !important;
        }
        
        .insight-box p {
            color: #1e293b !important;
        }
    </style>
    """, unsafe_allow_html=True)
