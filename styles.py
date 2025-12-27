"""
Global styling module for UMK Sleep Study Dashboard
Clean, readable light theme with dark sidebar
"""

import streamlit as st

def apply_global_styles():
    """Apply consistent styling across all pages"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* ========== GLOBAL FONT ========== */
        html, body, [class*="css"], * { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }
        
        /* ========== MAIN APP BACKGROUND ========== */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }
        
        /* ========== MAIN CONTENT CONTAINER (WHITE BACKGROUND) ========== */
        .main .block-container {
            background-color: #ffffff !important;
            border-radius: 20px !important;
            padding: 3rem 2rem !important;
            margin-top: 2rem !important;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3) !important;
            max-width: 1400px !important;
        }
        
        /* ========== FORCE DARK TEXT IN MAIN CONTENT ========== */
        .main {
            color: #1e293b !important;
        }
        
        .main p, .main span, .main div, .main li, .main label {
            color: #1e293b !important;
        }
        
        .main strong, .main b {
            color: #0f172a !important;
            font-weight: 700 !important;
        }
        
        /* ========== SIDEBAR (DARK THEME) ========== */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
        }
        
        section[data-testid="stSidebar"] > div {
            background-color: transparent !important;
            padding-top: 2rem !important;
        }
        
        /* Sidebar text - WHITE for visibility */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] li {
            color: #f1f5f9 !important;
        }
        
        section[data-testid="stSidebar"] h3 {
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            color: #ffffff !important;
            margin-bottom: 1.5rem !important;
            margin-top: 1.5rem !important;
            padding-bottom: 0.75rem !important;
            border-bottom: 2px solid #334155 !important;
        }
        
        /* ========== MULTISELECT FILTERS (DARK SIDEBAR) ========== */
        section[data-testid="stSidebar"] .stMultiSelect {
            margin-bottom: 1.5rem !important;
        }
        
        section[data-testid="stSidebar"] .stMultiSelect label {
            color: #cbd5e1 !important;
            font-size: 0.875rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important;
        }
        
        section[data-testid="stSidebar"] [data-baseweb="select"] {
            background-color: #0f172a !important;
            border: 1px solid #475569 !important;
            border-radius: 8px !important;
        }
        
        section[data-testid="stSidebar"] [data-baseweb="select"]:hover {
            border-color: #64748b !important;
        }
        
        section[data-testid="stSidebar"] input {
            color: #f1f5f9 !important;
            background-color: #0f172a !important;
        }
        
        /* Selected pills - BLUE */
        section[data-testid="stSidebar"] [data-baseweb="tag"] {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 0.35rem 0.85rem !important;
            margin: 0.25rem 0.25rem 0.25rem 0 !important;
            font-size: 0.813rem !important;
            font-weight: 500 !important;
        }
        
        section[data-testid="stSidebar"] [data-baseweb="tag"] span {
            color: #ffffff !important;
        }
        
        section[data-testid="stSidebar"] [data-baseweb="tag"] svg {
            fill: #ffffff !important;
        }
        
        /* Dropdown menu */
        [data-baseweb="popover"] {
            background-color: #1e293b !important;
        }
        
        [data-baseweb="menu"] {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
        }
        
        [role="option"] {
            background-color: #1e293b !important;
            color: #f1f5f9 !important;
            font-weight: 500 !important;
        }
        
        [role="option"]:hover,
        [aria-selected="true"] {
            background-color: #334155 !important;
        }
        
        /* ========== SIDEBAR BUTTONS ========== */
        section[data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 600 !important;
            width: 100% !important;
            transition: all 0.3s !important;
        }
        
        section[data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4) !important;
        }
        
        /* ========== SIDEBAR ALERTS ========== */
        section[data-testid="stSidebar"] .stAlert {
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%) !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 1.25rem !important;
        }
        
        section[data-testid="stSidebar"] .stAlert * {
            color: #dbeafe !important;
        }
        
        /* ========== SIDEBAR RADIO ========== */
        section[data-testid="stSidebar"] .stRadio > div {
            background-color: #1e293b !important;
            padding: 0.75rem !important;
            border-radius: 8px !important;
            border: 1px solid #334155 !important;
        }
        
        section[data-testid="stSidebar"] .stRadio label {
            color: #f1f5f9 !important;
        }
        
        /* ========== SIDEBAR EXPANDER ========== */
        section[data-testid="stSidebar"] .streamlit-expanderHeader {
            background-color: #1e293b !important;
            border-radius: 8px !important;
            color: #f1f5f9 !important;
        }
        
        section[data-testid="stSidebar"] .streamlit-expanderContent {
            background-color: #1e293b !important;
            border-color: #334155 !important;
        }
        
        /* ========== MAIN CONTENT HEADINGS (DARK TEXT) ========== */
        .main h1 {
            color: #1e293b !important;
            font-weight: 800 !important;
            font-size: 2.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        .main h2 {
            color: #1e293b !important;
            font-weight: 700 !important;
            font-size: 1.75rem !important;
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
        }
        
        .main h3 {
            color: #334155 !important;
            font-weight: 600 !important;
            font-size: 1.25rem !important;
        }
        
        .main h4 {
            color: #475569 !important;
            font-weight: 600 !important;
        }
        
        /* ========== METRICS ========== */
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
            padding: 1.5rem !important;
            border-radius: 12px !important;
            border: 2px solid #e2e8f0 !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
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
        
        /* ========== ALERTS IN MAIN (LIGHT THEME) ========== */
        .main .stSuccess {
            background-color: #d1fae5 !important;
            border-left: 4px solid #10b981 !important;
            color: #065f46 !important;
            border-radius: 8px !important;
        }
        
        .main .stInfo {
            background-color: #dbeafe !important;
            border-left: 4px solid #3b82f6 !important;
            color: #1e40af !important;
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
        
        /* ========== DIVIDERS ========== */
        .main hr {
            border: none !important;
            border-top: 2px solid #e5e7eb !important;
            margin: 2rem 0 !important;
        }
        
        /* ========== DATAFRAME ========== */
        .main [data-testid="stDataFrame"] {
            border-radius: 10px !important;
            overflow: hidden !important;
        }
        
        /* ========== EXPANDER IN MAIN ========== */
        .main .streamlit-expanderHeader {
            background-color: #f8fafc !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            color: #1e293b !important;
        }
        
        .main .streamlit-expanderHeader:hover {
            background-color: #f1f5f9 !important;
        }
        
        /* ========== CAPTIONS ========== */
        .main .caption, .main [data-testid="stCaptionContainer"] {
            color: #64748b !important;
        }
        
        /* ========== INSIGHT BOXES ========== */
        .insight-box {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%) !important;
            border-left: 4px solid #3b82f6 !important;
            border-radius: 10px !important;
            padding: 1.25rem 1.5rem !important;
            margin: 1.5rem 0 !important;
            box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1) !important;
        }
        
        .insight-box strong {
            color: #1e40af !important;
            font-weight: 600 !important;
        }
        
        .insight-box p {
            color: #1e293b !important;
            line-height: 1.6 !important;
            margin: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)
