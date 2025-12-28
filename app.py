import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="UMK Insomnia & Education Survey",
    page_icon="😴",
    layout="wide"
)

# Google Sheets CSV URL
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSf4umx6QNDel99If8P2otizAHj7jEDxFIsqandbD0zYVzfDheZo2YVkK1_zknpDKjHnBuYWCINgcCe/pub?output=csv"

# Load data with caching
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load the data
df = load_data()

if df is not None:
    # Sidebar
    st.sidebar.title("📊 Dashboard Navigation")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Select Team Member's Analysis",
        ["🏠 Overview", "👤 Member 1 Analysis", "👤 Member 2 Analysis", "👤 Member 3 Analysis"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.sidebar.info(f"📝 Total Responses: {len(df)}")
    
    # Add refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    # OVERVIEW PAGE
    if page == "🏠 Overview":
        st.title("😴 Insomnia and Educational Outcomes Survey")
        st.subheader("UMK Students Research Dashboard")
        st.markdown("---")
        
        # Display basic statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Responses", len(df))
        with col2:
            st.metric("Total Questions", len(df.columns))
        with col3:
            st.metric("Data Fields", len(df.columns))
        with col4:
            st.metric("Status", "✅ Live")
        
        st.markdown("---")
        
        # Show column names
        st.subheader("📋 Survey Structure")
        st.write("**Available Data Columns:**")
        st.write(df.columns.tolist())
        
        # Data preview
        st.subheader("👀 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Download option
        st.download_button(
            label="⬇️ Download Full Dataset",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=f"umk_insomnia_survey_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    # MEMBER 1 ANALYSIS
    elif page == "👤 Member 1 Analysis":
        st.title("👤 Member 1: Demographic & Sleep Pattern Analysis")
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Visualization 1: Gender Distribution
            st.subheader("📊 Visualization 1: Gender Distribution")
            gender_counts = df['What is your gender?'].value_counts()
            fig1 = px.pie(values=gender_counts.values, names=gender_counts.index,
                         title="Survey Respondents by Gender",
                         color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Visualization 2: Age Group Distribution
            st.subheader("📊 Visualization 2: Age Group Distribution")
            fig2 = px.histogram(df, x='What is your age group?',
                               title="Distribution by Age Group",
                               color_discrete_sequence=['#1f77b4'])
            fig2.update_layout(xaxis_title="Age Group", yaxis_title="Count")
            st.plotly_chart(fig2, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            # Visualization 3: Sleep Hours Distribution
            st.subheader("📊 Visualization 3: Daily Sleep Hours")
            sleep_counts = df['On average, how many hours of sleep do you get on a typical day? '].value_counts()
            fig3 = px.bar(x=sleep_counts.index, y=sleep_counts.values,
                         title="Average Sleep Duration Distribution",
                         color_discrete_sequence=['#2ca02c'],
                         labels={'x': 'Sleep Hours', 'y': 'Number of Students'})
            st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            # Visualization 4: Difficulty Falling Asleep
            st.subheader("📊 Visualization 4: Insomnia Frequency")
            insomnia_counts = df['How often do you have difficulty falling asleep at night? '].value_counts()
            fig4 = px.pie(values=insomnia_counts.values, names=insomnia_counts.index,
                         title="Difficulty Falling Asleep Frequency",
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig4, use_container_width=True)
        
        # Visualization 5: Sleep Quality Rating
        st.subheader("📊 Visualization 5: Sleep Quality Rating Distribution")
        fig5 = px.histogram(df, x='How would you rate the overall quality of your sleep? ',
                           title="Overall Sleep Quality Ratings Among UMK Students",
                           color_discrete_sequence=['#ff7f0e'],
                           labels={'How would you rate the overall quality of your sleep? ': 'Sleep Quality Rating'})
        fig5.update_layout(xaxis_title="Sleep Quality Rating (1-5)", yaxis_title="Number of Students")
        st.plotly_chart(fig5, use_container_width=True)
    
    # MEMBER 2 ANALYSIS
    elif page == "👤 Member 2 Analysis":
        st.title("👤 Member 2: Academic Performance & Study Impact")
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Visualization 1: Faculty Distribution
            st.subheader("📊 Visualization 1: Faculty Distribution")
            faculty_counts = df['Which faculty are you currently enrolled in?'].value_counts()
            fig1 = px.bar(x=faculty_counts.index, y=faculty_counts.values,
                         title="Students by Faculty",
                         color_discrete_sequence=['#d62728'])
            fig1.update_layout(xaxis_title="Faculty", yaxis_title="Number of Students", xaxis_tickangle=-45)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Visualization 2: GPA Range Distribution
            st.subheader("📊 Visualization 2: GPA Range Distribution")
            gpa_counts = df['What is your GPA range for the most recent semester?'].value_counts()
            fig2 = px.pie(values=gpa_counts.values, names=gpa_counts.index,
                         title="GPA Distribution",
                         color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig2, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            # Visualization 3: Concentration Difficulty
            st.subheader("📊 Visualization 3: Concentration During Study")
            conc_counts = df['How often do you experience difficulty concentrating during lectures or studying due to lack of sleep? '].value_counts()
            fig3 = px.bar(x=conc_counts.index, y=conc_counts.values,
                         title="Difficulty Concentrating Due to Lack of Sleep",
                         color_discrete_sequence=['#9467bd'])
            fig3.update_layout(xaxis_title="Frequency", yaxis_title="Number of Students")
            st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            # Visualization 4: Daytime Fatigue
            st.subheader("📊 Visualization 4: Daytime Fatigue")
            fatigue_counts = df['How often do you feel fatigued during the day, affecting your ability to study or attend classes? '].value_counts()
            fig4 = px.pie(values=fatigue_counts.values, names=fatigue_counts.index,
                         title="Daily Fatigue Impact on Studies",
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig4, use_container_width=True)
        
        # Visualization 5: Sleep Impact on Assignments
        st.subheader("📊 Visualization 5: Impact on Assignment Completion")
        impact_counts = df['How would you describe the impact of insufficient sleep on your ability to complete assignments and meet deadlines? '].value_counts()
        fig5 = px.bar(x=impact_counts.index, y=impact_counts.values,
                     title="Sleep's Impact on Meeting Deadlines",
                     color_discrete_sequence=['#e377c2'])
        fig5.update_layout(xaxis_title="Impact Level", yaxis_title="Number of Students")
        st.plotly_chart(fig5, use_container_width=True)
    
    # MEMBER 3 ANALYSIS
    elif page == "👤 Member 3 Analysis":
        st.title("👤 Member 3: Lifestyle Factors & Sleep Habits")
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Visualization 1: Electronic Device Usage Before Sleep
            st.subheader("📊 Visualization 1: Device Usage Before Sleep")
            device_counts = df['How often do you use electronic devices (e.g., phone, computer) before going to sleep? '].value_counts()
            fig1 = px.pie(values=device_counts.values, names=device_counts.index,
                         title="Electronic Device Usage Before Bedtime",
                         color_discrete_sequence=px.colors.qualitative.Set1)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Visualization 2: Caffeine Consumption
            st.subheader("📊 Visualization 2: Caffeine Consumption")
            caffeine_counts = df['How often do you consume caffeine (coffee, energy drinks) to stay awake or alert? '].value_counts()
            fig2 = px.bar(x=caffeine_counts.index, y=caffeine_counts.values,
                         title="Caffeine Consumption Frequency",
                         color_discrete_sequence=['#17becf'])
            fig2.update_layout(xaxis_title="Frequency", yaxis_title="Number of Students")
            st.plotly_chart(fig2, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            # Visualization 3: Physical Activity
            st.subheader("📊 Visualization 3: Physical Activity Level")
            exercise_counts = df['How often do you engage in physical activity or exercise? '].value_counts()
            fig3 = px.bar(x=exercise_counts.index, y=exercise_counts.values,
                         title="Exercise Frequency Among Students",
                         color_discrete_sequence=['#2ca02c'])
            fig3.update_layout(xaxis_title="Frequency", yaxis_title="Number of Students")
            st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            # Visualization 4: Stress Levels
            st.subheader("📊 Visualization 4: Academic Stress Levels")
            stress_counts = df['How would you describe your stress levels related to academic workload? '].value_counts()
            fig4 = px.pie(values=stress_counts.values, names=stress_counts.index,
                         title="Stress Levels Related to Academic Workload",
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig4, use_container_width=True)
        
        # Visualization 5: Sleep Methods Used
        st.subheader("📊 Visualization 5: Sleep Aid Methods")
        methods_counts = df['Do you use any methods to help you sleep?'].value_counts()
        fig5 = px.bar(x=methods_counts.index, y=methods_counts.values,
                     title="Methods Used to Help Sleep",
                     color_discrete_sequence=['#ff7f0e'])
        fig5.update_layout(xaxis_title="Method", yaxis_title="Number of Students", xaxis_tickangle=-45)
        st.plotly_chart(fig5, use_container_width=True)

else:
    st.error("Unable to load data. Please check your Google Sheets link and ensure it's published correctly.")
    st.info("""
    **To publish your Google Sheet correctly:**
    1. Go to File → Share → Publish to web
    2. Choose 'Entire Document' and 'Comma-separated values (.csv)'
    3. Click 'Publish'
    4. Copy the link and update the CSV_URL in this code
    """)
