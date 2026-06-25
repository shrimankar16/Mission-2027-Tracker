"""
Career Command Center - Main Application
Production-grade career management system for Mission 2027
"""
import streamlit as st
from pathlib import Path
from datetime import date

# Database imports
from database.database import init_database, is_database_empty, get_session
from database.seed import seed_database
from database.models import UserProfile

# Engine imports
from engines.phase_engine import PhaseEngine
from engines.revision_engine import RevisionEngine

# Page imports
from pages import dashboard, checklist, roadmap, progress, notes, mock_tests

# Configuration
st.set_page_config(
    page_title="Career Command Center | Mission 2027",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_file = Path(__file__).parent / "styles" / "main.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize database
init_database()


def init_session_state():
    """Initialize session state variables"""
    if 'revision_engine' not in st.session_state:
        st.session_state.revision_engine = None
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False


def onboarding_screen():
    """First-time user onboarding"""
    st.markdown("<h1 style='text-align: center;'>🎯 Career Command Center</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #8A93A8;'>Mission 2027</h3>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("### Welcome!")
    st.markdown("This is your unified command center for:")
    st.markdown("- 🏢 **Campus Placement** (Feb 2027)")
    st.markdown("- 📚 **SSC CGL 2027** (Ultimate Goal: ASO at MEA)")
    st.markdown("- 🏛️ **MPSC Group B/C** (Financial Safety Net)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        name = st.text_input("Enter your name:", placeholder="Your Name")
        start_date = st.date_input(
            "Start date:",
            value=date(2026, 6, 26),
            min_value=date(2026, 1, 1),
            max_value=date(2027, 12, 31)
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Start Journey", width="stretch"):
            if name.strip():
                with st.spinner("Setting up your roadmap..."):
                    # Seed database
                    seed_database(name.strip(), start_date)
                    st.session_state.user_name = name.strip()
                    st.session_state.initialized = True
                    st.rerun()
            else:
                st.error("Please enter your name")


def main_app():
    """Main application with navigation"""
    # Get user profile
    session = get_session()
    user = session.query(UserProfile).first()
    session.close()
    
    if not user:
        onboarding_screen()
        return
    
    # Start revision engine on first load
    if not st.session_state.revision_engine:
        rev_engine = RevisionEngine()
        rev_engine.start_scheduler()
        rev_engine.run_catch_up()  # Catch up on any missed revisions
        st.session_state.revision_engine = rev_engine
    
    # Check for phase transitions
    phase_engine = PhaseEngine()
    switched, old_phase, new_phase = phase_engine.check_and_switch_phase()
    phase_engine.close()
    
    if switched:
        st.success(f"✨ Phase switched from {old_phase} to {new_phase}!")
    
    # Sidebar navigation
    st.sidebar.markdown(f"### 👤 {user.name}")
    st.sidebar.markdown(f"**Phase {user.current_phase}** | Day {(date.today() - user.start_date).days + 1}")
    
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigate",
        ["Dashboard", "Checklist", "Roadmap", "Progress", "Notes", "Mock Tests"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Quick stats in sidebar
    from engines.analytics_engine import AnalyticsEngine
    analytics = AnalyticsEngine()
    stats = analytics.get_dashboard_stats()
    analytics.close()
    
    st.sidebar.metric("Study Streak", f"{stats.get('streak', 0)} days")
    st.sidebar.metric("Overall Progress", f"{stats.get('overall_completion', 0)}%")
    
    st.sidebar.markdown("---")
    st.sidebar.caption("💾 Auto-backup enabled")
    st.sidebar.caption(f"Last updated: {date.today().strftime('%d %b %Y')}")
    
    # Route to pages
    if page == "Dashboard":
        dashboard.show()
    elif page == "Checklist":
        checklist.show()
    elif page == "Roadmap":
        roadmap.show()
    elif page == "Progress":
        progress.show()
    elif page == "Notes":
        notes.show()
    elif page == "Mock Tests":
        mock_tests.show()


if __name__ == "__main__":
    init_session_state()
    
    # Check if database is empty
    if is_database_empty() and not st.session_state.initialized:
        onboarding_screen()
    else:
        main_app()
