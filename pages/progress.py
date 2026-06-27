"""
Progress/Analytics Page - Comprehensive visualizations and insights
Multiple charts tracking phase progress, subject mastery, daily activity, and trends
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from engines.analytics_engine import AnalyticsEngine
from engines.phase_engine import PhaseEngine
from datetime import date, timedelta
from database.database import get_session
from database.models import Subject, Topic, ChecklistItem, DailyLog, TopicMastery
import pandas as pd


def show():
    """Render comprehensive progress analytics page"""
    st.title("📊 Progress Tracker & Analytics")
    
    analytics = AnalyticsEngine()
    
    # Tab navigation for different analytics views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview", 
        "🎯 Phase Progress", 
        "📚 Subject Analysis",
        "📅 Daily Activity",
        "🔥 Performance Trends"
    ])
    
    with tab1:
        show_overview_analytics(analytics)
    
    with tab2:
        show_phase_progress(analytics)
    
    with tab3:
        show_subject_analysis(analytics)
    
    with tab4:
        show_daily_activity(analytics)
    
    with tab5:
        show_performance_trends(analytics)
    
    analytics.close()


def show_overview_analytics(analytics):
    """Tab 1: Overview - High-level summary"""
    st.markdown("### 🎯 Mission 2027 - Overall Progress")
    
    # Get key metrics
    stats = analytics.get_dashboard_stats()
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Completion", f"{stats.get('overall_completion', 0)}%")
    
    with col2:
        st.metric("Study Streak", f"{stats.get('streak', 0)} days", 
                 delta="Keep going!" if stats.get('streak', 0) > 0 else None)
    
    with col3:
        st.metric("Current Phase", f"Phase {stats.get('current_phase', 1)}")
    
    with col4:
        st.metric("Day", f"{stats.get('current_day', 1)} / 551")
    
    st.markdown("---")
    
    # Readiness Scores - Three Gauges
    st.markdown("### 🎯 Exam Readiness Scores")
    
    placement_score = analytics.calculate_placement_readiness()
    ssc_score = analytics.calculate_ssc_readiness()
    mpsc_score = analytics.calculate_mpsc_readiness()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig_placement = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=placement_score,
            title={'text': "🏢 Placement", 'font': {'size': 20}},
            delta={'reference': 80, 'increasing': {'color': "#6B8F71"}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': "#C9A84C"},
                'bgcolor': "#161A20",
                'borderwidth': 2,
                'bordercolor': "#2A3040",
                'steps': [
                    {'range': [0, 40], 'color': '#1E2430'},
                    {'range': [40, 70], 'color': '#252D3D'},
                    {'range': [70, 100], 'color': '#2A3648'}
                ],
                'threshold': {
                    'line': {'color': "#6B8F71", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        fig_placement.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor="#0D0F12",
            font=dict(color="#E8EAF0", family="Inter")
        )
        st.plotly_chart(fig_placement, width="stretch")
    
    with col2:
        fig_ssc = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=ssc_score,
            title={'text': "📚 SSC CGL", 'font': {'size': 20}},
            delta={'reference': 80, 'increasing': {'color': "#6B8F71"}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': "#6B8F71"},
                'bgcolor': "#161A20",
                'borderwidth': 2,
                'bordercolor': "#2A3040",
                'steps': [
                    {'range': [0, 40], 'color': '#1E2430'},
                    {'range': [40, 70], 'color': '#252D3D'},
                    {'range': [70, 100], 'color': '#2A3648'}
                ],
                'threshold': {
                    'line': {'color': "#C9A84C", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        fig_ssc.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor="#0D0F12",
            font=dict(color="#E8EAF0", family="Inter")
        )
        st.plotly_chart(fig_ssc, width="stretch")
    
    with col3:
        fig_mpsc = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=mpsc_score,
            title={'text': "🏛️ MPSC", 'font': {'size': 20}},
            delta={'reference': 80, 'increasing': {'color': "#6B8F71"}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': "#5B7FA6"},
                'bgcolor': "#161A20",
                'borderwidth': 2,
                'bordercolor': "#2A3040",
                'steps': [
                    {'range': [0, 40], 'color': '#1E2430'},
                    {'range': [40, 70], 'color': '#252D3D'},
                    {'range': [70, 100], 'color': '#2A3648'}
                ],
                'threshold': {
                    'line': {'color': "#C9A84C", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        fig_mpsc.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor="#0D0F12",
            font=dict(color="#E8EAF0", family="Inter")
        )
        st.plotly_chart(fig_mpsc, width="stretch")
    
    st.markdown("---")
    
    # Week Progress Bar Chart
    st.markdown("### 📅 This Week's Progress")
    
    week_data = analytics.get_week_progress()
    
    days = list(week_data.keys())
    completed = [week_data[day]['completed'] for day in days]
    total = [week_data[day]['total'] for day in days]
    pending = [t - c for t, c in zip(total, completed)]
    
    fig_week = go.Figure()
    fig_week.add_trace(go.Bar(
        name='Completed',
        x=days,
        y=completed,
        marker_color='#6B8F71',
        text=completed,
        textposition='inside'
    ))
    fig_week.add_trace(go.Bar(
        name='Pending',
        x=days,
        y=pending,
        marker_color='#2A3040',
        text=pending,
        textposition='inside'
    ))
    
    fig_week.update_layout(
        barmode='stack',
        title="Tasks Completed vs Pending (This Week)",
        xaxis_title="Day",
        yaxis_title="Number of Tasks",
        paper_bgcolor='#0D0F12',
        plot_bgcolor='#161A20',
        font=dict(color='#E8EAF0', family='Inter'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#2A3040'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400
    )
    
    st.plotly_chart(fig_week, width="stretch")



def show_phase_progress(analytics):
    """Tab 2: Phase-wise progress breakdown"""
    st.markdown("### 🎯 Phase-Wise Progress Analysis")
    
    phase_engine = PhaseEngine()
    session = get_session()
    
    # Get current phase info
    from database.models import UserProfile
    user = session.query(UserProfile).first()
    current_phase = user.current_phase if user else 1
    
    # Phase timeline visualization
    phase_data = []
    for phase_num in range(1, 6):
        info = phase_engine.get_phase_info(phase_num)
        phase_data.append({
            'Phase': f'Phase {phase_num}',
            'Completion': info.get('completion_pct', 0),
            'Status': info.get('status', 'Upcoming'),
            'Days Remaining': info.get('days_remaining', 0),
            'Total Days': info.get('total_days', 0)
        })
    
    # Horizontal bar chart for phase completion
    df_phases = pd.DataFrame(phase_data)
    
    colors = ['#C9A84C' if row['Status'] == 'Active' else 
              '#6B8F71' if row['Status'] == 'Completed' else 
              '#2A3040' for _, row in df_phases.iterrows()]
    
    fig_phases = go.Figure(go.Bar(
        x=df_phases['Completion'],
        y=df_phases['Phase'],
        orientation='h',
        marker=dict(color=colors),
        text=df_phases['Completion'].apply(lambda x: f'{x:.1f}%'),
        textposition='inside',
        hovertemplate='<b>%{y}</b><br>Completion: %{x:.1f}%<br><extra></extra>'
    ))
    
    fig_phases.update_layout(
        title="Phase Completion Status",
        xaxis_title="Completion %",
        yaxis_title="",
        paper_bgcolor='#0D0F12',
        plot_bgcolor='#161A20',
        font=dict(color='#E8EAF0', family='Inter'),
        xaxis=dict(showgrid=True, gridcolor='#2A3040', range=[0, 100]),
        yaxis=dict(showgrid=False),
        height=400
    )
    
    st.plotly_chart(fig_phases, width="stretch")
    
    st.markdown("---")
    
    # Detailed phase breakdown
    st.markdown("### 📋 Detailed Phase Information")
    
    for phase_num in range(1, 6):
        info = phase_engine.get_phase_info(phase_num)
        status = info.get('status', 'Upcoming')
        
        # Status badge color
        if status == 'Active':
            badge_color = '#C9A84C'
            icon = '🎯'
        elif status == 'Completed':
            badge_color = '#6B8F71'
            icon = '✅'
        else:
            badge_color = '#5B7FA6'
            icon = '📅'
        
        with st.expander(f"{icon} Phase {phase_num} - {status}", expanded=(phase_num == current_phase)):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Duration", f"{info.get('total_days', 0)} days")
            
            with col2:
                st.metric("Days Elapsed", f"{info.get('days_elapsed', 0)}")
            
            with col3:
                st.metric("Days Remaining", f"{info.get('days_remaining', 0)}")
            
            # Progress bar
            st.progress(info.get('completion_pct', 0) / 100)
            st.caption(f"{info.get('completion_pct', 0):.1f}% Complete")
            
            # Date range
            start = info.get('start_date')
            end = info.get('end_date')
            if start and end:
                st.info(f"📅 {start.strftime('%b %d, %Y')} → {end.strftime('%b %d, %Y')}")
    
    phase_engine.close()
    session.close()


def show_subject_analysis(analytics):
    """Tab 3: Subject-wise mastery and progress"""
    st.markdown("### 📚 Subject-Wise Analysis")
    
    session = get_session()
    
    # Get all subjects and their mastery
    subjects = session.query(Subject).all()
    
    subject_data = []
    for subject in subjects:
        topics = session.query(Topic).filter_by(subject_id=subject.id).all()
        total_topics = len(topics)
        
        if total_topics == 0:
            continue
        
        mastered = 0
        for topic in topics:
            mastery = session.query(TopicMastery).filter_by(topic_id=topic.id).first()
            if mastery and mastery.mastered:
                mastered += 1
        
        completion_pct = (mastered / total_topics * 100) if total_topics > 0 else 0
        
        subject_data.append({
            'Subject': subject.name,
            'Topics Mastered': mastered,
            'Total Topics': total_topics,
            'Completion %': completion_pct,
            'Counts For': ', '.join([c.replace('_', ' ').title() for c in subject.counts_for])
        })
    
    df_subjects = pd.DataFrame(subject_data)
    
    # Sunburst chart for subject hierarchy
    st.markdown("#### 🎯 Subject Mastery Overview")
    
    fig_sunburst = go.Figure(go.Sunburst(
        labels=df_subjects['Subject'].tolist() + ['All Subjects'],
        parents=['All Subjects'] * len(df_subjects) + [''],
        values=df_subjects['Total Topics'].tolist() + [df_subjects['Total Topics'].sum()],
        marker=dict(colors=['#C9A84C', '#6B8F71', '#5B7FA6', '#8B7355', '#A0522D', '#4A5568', '#E8EAF0']),
        hovertemplate='<b>%{label}</b><br>Topics: %{value}<br><extra></extra>'
    ))
    
    fig_sunburst.update_layout(
        paper_bgcolor='#0D0F12',
        font=dict(color='#E8EAF0', family='Inter'),
        height=500
    )
    
    st.plotly_chart(fig_sunburst, width="stretch")
    
    st.markdown("---")
    
    # Subject completion radar chart
    st.markdown("#### 📊 Subject Completion Radar")
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=df_subjects['Completion %'].tolist(),
        theta=df_subjects['Subject'].tolist(),
        fill='toself',
        fillcolor='rgba(107, 143, 113, 0.3)',
        line=dict(color='#6B8F71', width=2),
        marker=dict(size=8, color='#C9A84C'),
        name='Mastery %'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            bgcolor='#161A20',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='#2A3040',
                tickfont=dict(color='#8A93A8')
            ),
            angularaxis=dict(
                gridcolor='#2A3040',
                tickfont=dict(color='#E8EAF0')
            )
        ),
        paper_bgcolor='#0D0F12',
        font=dict(color='#E8EAF0', family='Inter'),
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig_radar, width="stretch")
    
    st.markdown("---")
    
    # Detailed subject table
    st.markdown("#### 📋 Subject Details")
    
    # Sort by completion percentage
    df_subjects_sorted = df_subjects.sort_values('Completion %', ascending=False)
    
    for _, row in df_subjects_sorted.iterrows():
        col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
        
        with col1:
            st.markdown(f"**{row['Subject']}**")
        
        with col2:
            st.metric("Topics", f"{row['Topics Mastered']}/{row['Total Topics']}", label_visibility="collapsed")
        
        with col3:
            completion = row['Completion %']
            color = '#6B8F71' if completion >= 70 else '#C9A84C' if completion >= 40 else '#A0522D'
            st.markdown(f"<h4 style='color:{color};'>{completion:.0f}%</h4>", unsafe_allow_html=True)
        
        with col4:
            st.caption(f"📌 {row['Counts For']}")
        
        st.progress(row['Completion %'] / 100)
        st.markdown("<br>", unsafe_allow_html=True)
    
    session.close()


def show_daily_activity(analytics):
    """Tab 4: Daily study activity and patterns"""
    st.markdown("### 📅 Daily Activity Analysis")
    
    session = get_session()
    
    # Get last 30 days of activity
    end_date = date.today()
    start_date = end_date - timedelta(days=29)
    
    daily_logs = session.query(DailyLog).filter(
        DailyLog.log_date >= start_date,
        DailyLog.log_date <= end_date
    ).order_by(DailyLog.log_date).all()
    
    # Prepare data
    dates = []
    study_hours = []
    tasks_completed_list = []
    tasks_total_list = []
    completion_rate = []
    
    current = start_date
    while current <= end_date:
        log = next((l for l in daily_logs if l.log_date == current), None)
        
        dates.append(current)
        
        if log:
            hours = log.total_study_minutes / 60
            study_hours.append(hours)
            tasks_completed_list.append(log.tasks_completed)
            tasks_total_list.append(log.tasks_total)
            rate = (log.tasks_completed / log.tasks_total * 100) if log.tasks_total > 0 else 0
            completion_rate.append(rate)
        else:
            study_hours.append(0)
            tasks_completed_list.append(0)
            tasks_total_list.append(0)
            completion_rate.append(0)
        
        current += timedelta(days=1)
    
    # Study hours heatmap (calendar style)
    st.markdown("#### 🔥 Study Hours Heatmap (Last 30 Days)")
    
    df_heatmap = pd.DataFrame({
        'Date': dates,
        'Hours': study_hours,
        'Day': [d.strftime('%a') for d in dates],
        'Week': [(d - start_date).days // 7 for d in dates]
    })
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        x=df_heatmap['Week'],
        y=df_heatmap['Day'],
        z=df_heatmap['Hours'],
        colorscale=[
            [0, '#1E2430'],
            [0.25, '#2A3648'],
            [0.5, '#5B7FA6'],
            [0.75, '#6B8F71'],
            [1, '#C9A84C']
        ],
        hovertemplate='Week %{x}<br>%{y}<br>%{z:.1f} hours<extra></extra>',
        colorbar=dict(title="Hours", tickfont=dict(color='#E8EAF0'))
    ))
    
    fig_heatmap.update_layout(
        xaxis_title="Week",
        yaxis_title="",
        paper_bgcolor='#0D0F12',
        plot_bgcolor='#161A20',
        font=dict(color='#E8EAF0', family='Inter'),
        height=300
    )
    
    st.plotly_chart(fig_heatmap, width="stretch")
    
    st.markdown("---")
    
    # Daily completion rate line chart
    st.markdown("#### 📈 Daily Task Completion Rate")

    
    fig_completion = go.Figure()
    
    fig_completion.add_trace(go.Scatter(
        x=dates,
        y=completion_rate,
        mode='lines+markers',
        name='Completion Rate',
        line=dict(color='#6B8F71', width=3),
        marker=dict(size=6, color='#C9A84C'),
        fill='tozeroy',
        fillcolor='rgba(107, 143, 113, 0.2)',
        hovertemplate='%{x|%b %d}<br>%{y:.0f}% completed<extra></extra>'
    ))
    
    # Add reference line at 100%
    fig_completion.add_hline(y=100, line_dash="dash", line_color="#C9A84C", 
                            annotation_text="100% Target", annotation_position="right")
    
    fig_completion.update_layout(
        xaxis_title="Date",
        yaxis_title="Completion Rate (%)",
        paper_bgcolor='#0D0F12',
        plot_bgcolor='#161A20',
        font=dict(color='#E8EAF0', family='Inter'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#2A3040', range=[0, 110]),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_completion, width="stretch")
    
    st.markdown("---")
    
    # Study hours bar chart
    st.markdown("#### ⏱️ Daily Study Hours")
    
    fig_hours = go.Figure()
    
    colors_hours = ['#6B8F71' if h >= 5 else '#C9A84C' if h >= 3 else '#A0522D' for h in study_hours]
    
    fig_hours.add_trace(go.Bar(
        x=dates,
        y=study_hours,
        marker=dict(color=colors_hours),
        text=[f'{h:.1f}h' if h > 0 else '' for h in study_hours],
        textposition='outside',
        hovertemplate='%{x|%b %d}<br>%{y:.1f} hours<extra></extra>'
    ))
    
    # Add target line at 6 hours
    fig_hours.add_hline(y=6, line_dash="dash", line_color="#5B7FA6", 
                       annotation_text="6h Target", annotation_position="right")
    
    fig_hours.update_layout(
        xaxis_title="Date",
        yaxis_title="Hours",
        paper_bgcolor='#0D0F12',
        plot_bgcolor='#161A20',
        font=dict(color='#E8EAF0', family='Inter'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#2A3040'),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_hours, width="stretch")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_hours = sum(study_hours) / len(study_hours)
        st.metric("Avg Daily Hours", f"{avg_hours:.1f}h")
    
    with col2:
        total_hours = sum(study_hours)
        st.metric("Total Hours (30d)", f"{total_hours:.0f}h")
    
    with col3:
        avg_completion = sum(completion_rate) / len(completion_rate)
        st.metric("Avg Completion", f"{avg_completion:.0f}%")
    
    with col4:
        days_100 = sum(1 for rate in completion_rate if rate >= 100)
        st.metric("Perfect Days", f"{days_100}")
    
    session.close()


def show_performance_trends(analytics):
    """Tab 5: Long-term trends and projections"""
    st.markdown("### 🔥 Performance Trends & Projections")
    
    session = get_session()
    
    # Get all daily logs for trend analysis
    all_logs = session.query(DailyLog).order_by(DailyLog.log_date).all()
    
    if len(all_logs) < 2:
        st.info("📊 Not enough data yet. Come back after a few days of tracking!")
        session.close()
        return
    
    # Prepare cumulative data
    dates = [log.log_date for log in all_logs]
    cumulative_hours = []
    cumulative_tasks = []
    total_hours = 0
    total_tasks = 0
    
    for log in all_logs:
        total_hours += log.total_study_minutes / 60
        total_tasks += log.tasks_completed
        cumulative_hours.append(total_hours)
        cumulative_tasks.append(total_tasks)
    
    # Cumulative progress chart
    st.markdown("#### 📈 Cumulative Progress Over Time")
    
    fig_cumulative = go.Figure()
    
    fig_cumulative.add_trace(go.Scatter(
        x=dates,
        y=cumulative_tasks,
        mode='lines+markers',
        name='Tasks Completed',
        line=dict(color='#C9A84C', width=3),
        marker=dict(size=6),
        yaxis='y1',
        hovertemplate='%{x|%b %d}<br>%{y} tasks total<extra></extra>'
    ))
    
    fig_cumulative.add_trace(go.Scatter(
        x=dates,
        y=cumulative_hours,
        mode='lines+markers',
        name='Study Hours',
        line=dict(color='#6B8F71', width=3),
        marker=dict(size=6),
        yaxis='y2',
        hovertemplate='%{x|%b %d}<br>%{y:.0f} hours total<extra></extra>'
    ))
    
    fig_cumulative.update_layout(
        xaxis_title="Date",
        yaxis=dict(
            title="Total Tasks",
            titlefont=dict(color='#C9A84C'),
            tickfont=dict(color='#C9A84C'),
            showgrid=True,
            gridcolor='#2A3040'
        ),
        yaxis2=dict(
            title="Total Hours",
            titlefont=dict(color='#6B8F71'),
            tickfont=dict(color='#6B8F71'),
            overlaying='y',
            side='right',
            showgrid=False
        ),
        paper_bgcolor='#0D0F12',
        plot_bgcolor='#161A20',
        font=dict(color='#E8EAF0', family='Inter'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400
    )
    
    st.plotly_chart(fig_cumulative, width="stretch")
    
    st.markdown("---")
    
    # Streak analysis
    st.markdown("#### 🔥 Study Streak Analysis")
    
    streak_data = []
    current_streak = 0
    max_streak = 0
    
    for i, log in enumerate(all_logs):
        if log.tasks_completed > 0:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
        
        streak_data.append(current_streak)
    
    fig_streak = go.Figure()
    
    fig_streak.add_trace(go.Scatter(
        x=dates,
        y=streak_data,
        mode='lines',
        fill='tozeroy',
        fillcolor='rgba(201, 168, 76, 0.3)',
        line=dict(color='#C9A84C', width=2),
        hovertemplate='%{x|%b %d}<br>Streak: %{y} days<extra></extra>'
    ))
    
    fig_streak.update_layout(
        title=f"Study Streak History (Max: {max_streak} days)",
        xaxis_title="Date",
        yaxis_title="Streak (days)",
        paper_bgcolor='#0D0F12',
        plot_bgcolor='#161A20',
        font=dict(color='#E8EAF0', family='Inter'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#2A3040'),
        height=350,
        showlegend=False
    )
    
    st.plotly_chart(fig_streak, width="stretch")
    
    st.markdown("---")
    
    # Weekly performance comparison
    st.markdown("#### 📊 Weekly Performance Comparison")
    
    # Group by week
    weekly_data = {}
    for log in all_logs:
        week_num = (log.log_date - all_logs[0].log_date).days // 7
        week_key = f"Week {week_num + 1}"
        
        if week_key not in weekly_data:
            weekly_data[week_key] = {'hours': 0, 'tasks': 0, 'days': 0}
        
        weekly_data[week_key]['hours'] += log.total_study_minutes / 60
        weekly_data[week_key]['tasks'] += log.tasks_completed
        weekly_data[week_key]['days'] += 1
    
    weeks = list(weekly_data.keys())
    week_hours = [weekly_data[w]['hours'] for w in weeks]
    week_tasks = [weekly_data[w]['tasks'] for w in weeks]
    
    fig_weekly = go.Figure()
    
    fig_weekly.add_trace(go.Bar(
        x=weeks,
        y=week_hours,
        name='Study Hours',
        marker_color='#6B8F71',
        yaxis='y1',
        text=[f'{h:.0f}h' for h in week_hours],
        textposition='outside'
    ))
    
    fig_weekly.add_trace(go.Scatter(
        x=weeks,
        y=week_tasks,
        name='Tasks Completed',
        mode='lines+markers',
        line=dict(color='#C9A84C', width=3),
        marker=dict(size=10),
        yaxis='y2'
    ))
    
    fig_weekly.update_layout(
        xaxis_title="Week",
        yaxis=dict(
            title="Study Hours",
            titlefont=dict(color='#6B8F71'),
            tickfont=dict(color='#6B8F71'),
            showgrid=True,
            gridcolor='#2A3040'
        ),
        yaxis2=dict(
            title="Tasks Completed",
            titlefont=dict(color='#C9A84C'),
            tickfont=dict(color='#C9A84C'),
            overlaying='y',
            side='right',
            showgrid=False
        ),
        paper_bgcolor='#0D0F12',
        plot_bgcolor='#161A20',
        font=dict(color='#E8EAF0', family='Inter'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400
    )
    
    st.plotly_chart(fig_weekly, width="stretch")
    
    # Performance insights
    st.markdown("---")
    st.markdown("#### 💡 Performance Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Key Statistics:**")
        st.metric("Total Days Tracked", len(all_logs))
        st.metric("Total Study Hours", f"{total_hours:.0f}h")
        st.metric("Total Tasks Completed", f"{total_tasks}")
        st.metric("Max Streak", f"{max_streak} days")
    
    with col2:
        st.markdown("**🎯 Averages:**")
        avg_daily_hours = total_hours / len(all_logs)
        avg_daily_tasks = total_tasks / len(all_logs)
        st.metric("Avg Hours/Day", f"{avg_daily_hours:.1f}h")
        st.metric("Avg Tasks/Day", f"{avg_daily_tasks:.1f}")
        
        # Calculate trend
        if len(all_logs) >= 14:
            recent_avg = sum([l.total_study_minutes / 60 for l in all_logs[-7:]]) / 7
            older_avg = sum([l.total_study_minutes / 60 for l in all_logs[-14:-7]]) / 7
            trend = recent_avg - older_avg
            
            if trend > 0:
                st.success(f"📈 Improving! +{trend:.1f}h/day vs last week")
            elif trend < 0:
                st.warning(f"📉 Declining: {trend:.1f}h/day vs last week")
            else:
                st.info("➡️ Steady pace maintained")
    
    session.close()
