"""
Progress/Analytics Page - Charts, heatmaps, subject-wise analysis
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from engines.analytics_engine import AnalyticsEngine
from datetime import date, timedelta


def show():
    """Render progress analytics page"""
    st.title("📊 Progress Tracker")
    
    analytics = AnalyticsEngine()
    
    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["Overview", "Subject Analysis", "Phase Progress"])
    
    with tab1:
        st.markdown("### Overview Analytics")
        
        # This week's progress
        week_data = analytics.get_week_progress()
        
        days = list(week_data.keys())
        completed = [week_data[day]['completed'] for day in days]
        total = [week_data[day]['total'] for day in days]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=days,
            y=completed,
            name='Completed',
            marker_color='#6B8F71'
        ))
        fig.add_trace(go.Bar(
            x=days,
            y=[t - c for t, c in zip(total, completed)],
            name='Pending',
            marker_color='#2A3040'
        ))
        
        fig.update_layout(
            title="This Week's Progress",
            barmode='stack',
            paper_bgcolor='#0D0F12',
            plot_bgcolor='#161A20',
            font=dict(color='#E8EAF0', family='Inter'),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#2A3040')
        )
        
        st.plotly_chart(fig, width="stretch")
        
        # Readiness scores summary
        st.markdown("### Readiness Scores")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            placement_score = analytics.calculate_placement_readiness()
            st.metric("Placement", f"{placement_score}%")
        
        with col2:
            ssc_score = analytics.calculate_ssc_readiness()
            st.metric("SSC CGL", f"{ssc_score}%")
        
        with col3:
            mpsc_score = analytics.calculate_mpsc_readiness()
            st.metric("MPSC", f"{mpsc_score}%")
    
    with tab2:
        st.markdown("### Subject-Level Analysis")
        st.info("Subject heatmap and detailed breakdown will be displayed here.")
        
        # Placeholder for subject analysis
        st.markdown("**Feature coming soon:**")
        st.markdown("- Subject-wise completion percentage")
        st.markdown("- Study hours heatmap (GitHub-style)")
        st.markdown("- Weak vs Strong subject identification")
    
    with tab3:
        st.markdown("### Phase Progress")
        
        from engines.phase_engine import PhaseEngine
        phase_engine = PhaseEngine()
        
        for phase in range(1, 6):
            info = phase_engine.get_phase_info(phase)
            st.markdown(f"**Phase {phase}:** {info.get('completion_pct', 0):.1f}% complete")
            st.progress(info.get('completion_pct', 0) / 100)
        
        phase_engine.close()
    
    analytics.close()
