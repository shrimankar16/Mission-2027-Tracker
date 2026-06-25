"""
Roadmap Page - Visual roadmap timeline and phase view
"""
import streamlit as st
from datetime import date
from engines.phase_engine import PhaseEngine


def show():
    """Render roadmap page"""
    st.title("🗺️ Roadmap")
    
    st.markdown("### Mission 2027 Timeline")
    
    phase_engine = PhaseEngine()
    
    # Phase overview
    for phase_num in range(1, 6):
        phase_info = phase_engine.get_phase_info(phase_num)
        
        status = phase_info.get('status', 'Upcoming')
        start = phase_info.get('start_date')
        end = phase_info.get('end_date')
        days_total = phase_info.get('total_days', 0)
        completion = phase_info.get('completion_pct', 0)
        
        # Status color
        if status == "Active":
            border_color = "#C9A84C"
        elif status == "Completed":
            border_color = "#6B8F71"
        else:
            border_color = "#2A3040"
        
        st.markdown(f"""
        <div style="border-left: 4px solid {border_color}; padding: 20px; margin-bottom: 16px; background-color: #161A20;">
            <h3>Phase {phase_num} - {status}</h3>
            <p style="color: #8A93A8;">{start.strftime('%b %d, %Y')} → {end.strftime('%b %d, %Y')} ({days_total} days)</p>
            <p><strong>Completion:</strong> {completion:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"Phase {phase_num} Details"):
            if phase_num == 1:
                st.markdown("""
                **Focus:**
                - DSA: 40%
                - Aptitude + Reasoning + English: 25%
                - MPSC Group C GS: 25%
                - Current Affairs: 10%
                
                **Goal:** Build foundation for placement + Group C prelim
                """)
            elif phase_num == 2:
                st.markdown("""
                **Focus:**
                - Placement: 70-100% (depending on Group C status)
                - Group C Mains: 30% (if prelim cleared)
                
                **Goal:** Secure campus placement + prepare for Group C Mains
                """)
            elif phase_num == 3:
                st.markdown("""
                **Focus:**
                - SSC CGL: 80%
                - MPSC Group B: 20%
                
                **Goal:** Intensive SSC CGL preparation (Target: ASO at MEA)
                """)
            elif phase_num == 4:
                st.markdown("""
                **Focus:**
                - SSC CGL: 70%
                - MPSC Group B: 30%
                
                **Goal:** PYQ practice + Mocks
                """)
            else:  # Phase 5
                st.markdown("""
                **Focus:**
                - Full-length mocks (alternating SSC/MPSC)
                - Error analysis
                - Formula revision
                
                **Goal:** Peak readiness for exams
                """)
    
    phase_engine.close()
