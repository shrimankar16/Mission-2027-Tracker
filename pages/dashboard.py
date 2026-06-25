"""
Dashboard - Main command center view
Shows today's tasks, phase info, quick stats, and readiness scores
"""
import streamlit as st
from datetime import date
from engines.analytics_engine import AnalyticsEngine
from engines.phase_engine import PhaseEngine
from engines.checklist_engine import ChecklistEngine
from database.models import UserProfile
from database.database import get_session
import plotly.graph_objects as go


def show():
    """Render dashboard page"""
    st.title("🎯 Dashboard")
    
    # Get analytics
    analytics = AnalyticsEngine()
    stats = analytics.get_dashboard_stats()
    
    # Get user profile
    session = get_session()
    user = session.query(UserProfile).first()
    session.close()
    
    # Top stat cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <h3>Today</h3>
            <div class="value mono">{}</div>
            <p style="color: var(--text-secondary); margin-top: 8px;">Day {} of 551</p>
        </div>
        """.format(
            date.today().strftime("%b %d"),
            stats.get('current_day', 1)
        ), unsafe_allow_html=True)
    
    with col2:
        phase_engine = PhaseEngine()
        phase_info = phase_engine.get_phase_info(stats.get('current_phase', 1))
        phase_engine.close()
        
        st.markdown("""
        <div class="stat-card">
            <h3>Current Phase</h3>
            <div class="value">Phase {}</div>
            <p style="color: var(--text-secondary); margin-top: 8px;">{} days remaining</p>
        </div>
        """.format(
            stats.get('current_phase', 1),
            phase_info.get('days_remaining', 0)
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <h3>Study Streak</h3>
            <div class="value">{}</div>
            <p style="color: var(--text-secondary); margin-top: 8px;">consecutive days</p>
        </div>
        """.format(stats.get('streak', 0)), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <h3>Overall Progress</h3>
            <div class="value">{}%</div>
            <p style="color: var(--text-secondary); margin-top: 8px;">roadmap completion</p>
        </div>
        """.format(stats.get('overall_completion', 0)), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main content columns
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### 📋 Today's Checklist")
        
        # Get today's checklist
        checklist_engine = ChecklistEngine()
        today_items = checklist_engine.get_today_checklist()
        
        if not today_items:
            st.info("🎉 No tasks scheduled for today. Rest day or catch up on overdue items!")
        else:
            for item_data in today_items:
                item = item_data['item']
                topic = item_data['topic']
                subject = item_data['subject']
                counts_for = item_data['counts_for']
                
                # Determine badge color
                badge_class = "badge-learn"
                if item.item_type == "practice":
                    badge_class = "badge-practice"
                elif item.item_type.startswith("revise"):
                    badge_class = "badge-revise"
                elif item.item_type == "current_affairs":
                    badge_class = "badge-current-affairs"
                
                # Completion status
                completed_class = "completed" if item.completed else ""
                
                st.markdown(f"""
                <div class="checklist-item {completed_class}">
                    <span class="badge {badge_class}">{item.item_type.upper()}</span>
                    <strong style="color: var(--text-primary);">{subject.name}</strong> → {topic.name}
                    <br>
                    <small style="color: var(--text-secondary);">Subtopics: {', '.join(topic.subtopics)}</small>
                    <br>
                    <small>
                    {"".join([f'<span class="tag">{c.replace("_", " ").title()}</span>' for c in counts_for])}
                    </small>
                </div>
                """, unsafe_allow_html=True)
                
                # Checkbox
                checked = st.checkbox(
                    f"Mark complete",
                    value=item.completed,
                    key=f"item_{item.id}"
                )
                
                if checked != item.completed:
                    if checked:
                        checklist_engine.mark_complete(item.id)
                    else:
                        checklist_engine.mark_incomplete(item.id)
                    st.rerun()
                
                if checked and not item.time_spent_minutes:
                    time_input = st.number_input(
                        "Time spent (minutes):",
                        min_value=1,
                        max_value=300,
                        value=45,
                        key=f"time_{item.id}"
                    )
                    if st.button("Save time", key=f"save_{item.id}"):
                        checklist_engine.mark_complete(item.id, time_input)
                        st.rerun()
        
        checklist_engine.close()
    
    with col_right:
        st.markdown("### 📊 Readiness Scores")
        
        # Gauge charts for readiness
        placement_score = analytics.calculate_placement_readiness()
        ssc_score = analytics.calculate_ssc_readiness()
        mpsc_score = analytics.calculate_mpsc_readiness()
        
        # Placement gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=placement_score,
            title={'text': "Placement"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#C9A84C"},
                'bgcolor': "#161A20",
                'borderwidth': 2,
                'bordercolor': "#2A3040"
            }
        ))
        fig.update_layout(
            height=200,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="#0D0F12",
            font=dict(color="#E8EAF0", family="Inter")
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # SSC gauge
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=ssc_score,
            title={'text': "SSC CGL"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#6B8F71"},
                'bgcolor': "#161A20",
                'borderwidth': 2,
                'bordercolor': "#2A3040"
            }
        ))
        fig2.update_layout(
            height=200,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="#0D0F12",
            font=dict(color="#E8EAF0", family="Inter")
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # MPSC gauge
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=mpsc_score,
            title={'text': "MPSC Group B/C"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#5B7FA6"},
                'bgcolor': "#161A20",
                'borderwidth': 2,
                'bordercolor': "#2A3040"
            }
        ))
        fig3.update_layout(
            height=200,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="#0D0F12",
            font=dict(color="#E8EAF0", family="Inter")
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    analytics.close()
    
    # Status update section
    st.markdown("---")
    st.markdown("### ⚙️ Status Updates")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("✅ Mark Placement Secured"):
            if st.session_state.get('confirm_placement'):
                session = get_session()
                user = session.query(UserProfile).first()
                user.placement_status = "secured"
                user.current_phase = 3
                session.commit()
                session.close()
                st.success("Placement marked as secured! Moving to Phase 3.")
                st.rerun()
            else:
                st.session_state.confirm_placement = True
                st.warning("Click again to confirm")
    
    with col2:
        if st.button("✅ Group C Prelim Cleared"):
            session = get_session()
            user = session.query(UserProfile).first()
            user.group_c_status = "prelim_cleared"
            session.commit()
            session.close()
            st.success("Group C Prelim marked as cleared!")
            st.rerun()
    
    with col3:
        if st.button("❌ Placement Failed (Feb 2027)"):
            session = get_session()
            user = session.query(UserProfile).first()
            user.placement_status = "failed_Feb2027"
            user.current_phase = 3
            session.commit()
            session.close()
            st.info("Status updated. Moving to Phase 3.")
            st.rerun()
    
    with col4:
        if st.button("🔄 Reset All Status"):
            st.warning("This will reset all status. Not recommended unless starting fresh.")
