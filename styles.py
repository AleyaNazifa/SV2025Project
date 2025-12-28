"""Global styling for UMK Sleep Study Dashboard"""
import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', -apple-system, sans-serif !important;
        }
        
        /* Purple gradient background */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* White content container */
        .main .block-container {
            background-color: #ffffff;
            border-radius: 20px;
            padding: 3rem 2rem;
            margin: 2rem auto;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 1400px;
        }
        
        /* MAIN CONTENT - Dark text on white */
        .main h1, .main h2, .main h3, .main h4 {
            color: #1a202c !important;
        }
        
        .main p, .main span, .main div, .main li, .main label {
            color: #2d3748 !important;
        }
        
        .main strong {
            color: #1a202c !important;
        }
        
        /* SIDEBAR - Dark background with white text */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        }
        
        section[data-testid="stSidebar"] * {
            color: #f1f5f9 !important;
        }
        
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #ffffff !important;
            border-bottom: 2px solid #334155;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }
        
        /* Multiselect filters */
        section[data-testid="stSidebar"] [data-baseweb="select"] {
            background-color: #0f172a !important;
            border: 1px solid #475569 !important;
            border-radius: 8px !important;
        }
        
        section[data-testid="stSidebar"] input {
            color: #ffffff !important;
            background-color: #0f172a !important;
        }
        
        /* Blue gradient pills for selected filters */
        section[data-testid="stSidebar"] [data-baseweb="tag"] {
            background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 0.35rem 0.85rem !important;
            margin: 0.25rem !important;
            font-weight: 500 !important;
        }
        
        section[data-testid="stSidebar"] [data-baseweb="tag"] span,
        section[data-testid="stSidebar"] [data-baseweb="tag"] svg {
            color: #ffffff !important;
            fill: #ffffff !important;
        }
        
        /* Dropdown menus */
        [data-baseweb="popover"],
        [data-baseweb="menu"] {
            background-color: #1e293b !important;
        }
        
        [role="option"] {
            background-color: #1e293b !important;
            color: #f1f5f9 !important;
        }
        
        [role="option"]:hover {
            background-color: #334155 !important;
        }
        
        /* Sidebar buttons */
        section[data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            color: #ffffff;
            border: none;
            border-radius: 10px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s;
        }
        
        section[data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        }
        
        /* Sidebar alerts */
        section[data-testid="stSidebar"] .stAlert {
            background: linear-gradient(135deg, #1e3a8a, #1e40af) !important;
            border: none !important;
            border-radius: 10px !important;
        }
        
        section[data-testid="stSidebar"] .stAlert * {
            color: #dbeafe !important;
        }
        
        /* Sidebar radio buttons */
        section[data-testid="stSidebar"] .stRadio > div {
            background-color: #1e293b;
            padding: 0.75rem;
            border-radius: 8px;
            border: 1px solid #334155;
        }
        
        /* Metrics cards */
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, #f8fafc, #f1f5f9);
            padding: 1.5rem;
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        [data-testid="stMetricValue"] {
            color: #667eea !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
        }
        
        [data-testid="stMetricLabel"] {
            color: #475569 !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
        }
        
        /* Alert boxes in main content */
        .main .stInfo {
            background-color: #dbeafe !important;
            border-left: 4px solid #3b82f6 !important;
            color: #1e40af !important;
            border-radius: 8px !important;
        }
        
        .main .stSuccess {
            background-color: #d1fae5 !important;
            border-left: 4px solid #10b981 !important;
            color: #065f46 !important;
            border-radius: 8px !important;
        }
        
        .main .stWarning {
            background-color: #fef3c7 !important;
            border-left: 4px solid #f59e0b !important;
            color: #92400e !important;
            border-radius: 8px !important;
        }
        
        .main .stError {
            background-color: #fee2e2 !important;
            border-left: 4px solid #ef4444 !important;
            color: #991b1b !important;
            border-radius: 8px !important;
        }
        
        /* Dividers */
        .main hr {
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
            box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1);
        }
        
        .insight-box strong {
            color: #1e40af !important;
            font-weight: 600 !important;
        }
        
        .insight-box p {
            color: #1e293b !important;
            margin: 0;
        }
        
        /* Expanders */
        .main .streamlit-expanderHeader {
            background-color: #f8fafc;
            border-radius: 8px;
            font-weight: 600;
            color: #1e293b;
        }
        
        .main .streamlit-expanderHeader:hover {
            background-color: #f1f5f9;
        }
        
        /* Captions */
        .main [data-testid="stCaptionContainer"] {
            color: #64748b !important;
        }
    </style>
    """, unsafe_allow_html=True)
