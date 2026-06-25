"""
Mock Tests Page - Log and analyze practice tests
"""
import streamlit as st
from datetime import date
from database.database import get_session
from database.models import MockTest
import plotly.graph_objects as go


def show():
    """Render mock tests page"""
    st.title("🎯 Mock Tests")
    
    session = get_session()
    
    # Add new mock test
    with st.expander("➕ Log New Mock Test"):
        exam_type = st.selectbox(
            "Exam Type:",
            ["placement_aptitude", "placement_dsa", "ssc_tier1", "ssc_tier2", 
             "mpsc_group_c", "mpsc_group_b", "custom"]
        )
        
        test_name = st.text_input("Test Name/Source:", placeholder="e.g., Infosys Mock 1")
        
        col1, col2 = st.columns(2)
        with col1:
            taken_on = st.date_input("Date Taken:", value=date.today())
        with col2:
            time_taken = st.number_input("Time Taken (minutes):", min_value=1, value=60)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            total_q = st.number_input("Total Questions:", min_value=1, value=100)
        with col2:
            correct = st.number_input("Correct:", min_value=0, value=0, max_value=total_q)
        with col3:
            wrong = st.number_input("Wrong:", min_value=0, value=0)
        
        attempted = correct + wrong
        
        col1, col2 = st.columns(2)
        with col1:
            score = st.number_input("Your Score:", min_value=0.0, value=0.0)
        with col2:
            max_score = st.number_input("Max Score:", min_value=0.0, value=100.0)
        
        notes = st.text_area("Notes/Observations:", placeholder="What went wrong, areas to improve...")
        
        if st.button("💾 Save Mock Test"):
            if test_name.strip():
                mock = MockTest(
                    exam_type=exam_type,
                    test_name=test_name.strip(),
                    taken_on=taken_on,
                    total_questions=total_q,
                    attempted=attempted,
                    correct=correct,
                    wrong=wrong,
                    score=score,
                    max_score=max_score,
                    time_taken_minutes=time_taken,
                    subject_breakdown={},  # Can be extended
                    notes=notes.strip() if notes else None
                )
                
                session.add(mock)
                session.commit()
                st.success("✅ Mock test logged!")
                st.rerun()
            else:
                st.error("Please enter test name")
    
    st.markdown("---")
    
    # Display mock tests
    st.markdown("### 📊 Mock Test History")
    
    mocks = session.query(MockTest).order_by(MockTest.taken_on.desc()).all()
    
    if not mocks:
        st.info("No mock tests logged yet. Add your first test above!")
    else:
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Mocks", len(mocks))
        
        with col2:
            avg_score = sum(m.score for m in mocks) / len(mocks) if mocks else 0
            st.metric("Avg Score", f"{avg_score:.1f}")
        
        with col3:
            best_score = max(m.score for m in mocks) if mocks else 0
            st.metric("Best Score", f"{best_score:.1f}")
        
        with col4:
            if len(mocks) >= 2:
                last_score = mocks[0].score
                prev_score = mocks[1].score
                improvement = last_score - prev_score
                st.metric("Last vs Prev", f"{improvement:+.1f}")
            else:
                st.metric("Last vs Prev", "N/A")
        
        # Score trend chart
        if len(mocks) >= 2:
            dates = [m.taken_on.strftime('%b %d') for m in reversed(mocks)]
            scores = [m.score for m in reversed(mocks)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=scores,
                mode='lines+markers',
                line=dict(color='#C9A84C', width=2),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title="Score Trend",
                xaxis_title="Test Date",
                yaxis_title="Score",
                paper_bgcolor='#0D0F12',
                plot_bgcolor='#161A20',
                font=dict(color='#E8EAF0', family='Inter'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#2A3040')
            )
            
            st.plotly_chart(fig, width="stretch")
        
        # Mock test list
        st.markdown("### 📝 Test Details")
        
        for mock in mocks:
            accuracy = (mock.correct / mock.attempted * 100) if mock.attempted > 0 else 0
            percentage = (mock.score / mock.max_score * 100) if mock.max_score > 0 else 0
            
            with st.expander(f"{mock.test_name} - {mock.taken_on.strftime('%b %d, %Y')} ({percentage:.1f}%)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Exam Type:** {mock.exam_type.replace('_', ' ').title()}")
                    st.write(f"**Score:** {mock.score}/{mock.max_score} ({percentage:.1f}%)")
                    st.write(f"**Time Taken:** {mock.time_taken_minutes} minutes")
                
                with col2:
                    st.write(f"**Total Questions:** {mock.total_questions}")
                    st.write(f"**Attempted:** {mock.attempted}")
                    st.write(f"**Correct:** {mock.correct} | **Wrong:** {mock.wrong}")
                    st.write(f"**Accuracy:** {accuracy:.1f}%")
                
                if mock.notes:
                    st.markdown("**Notes:**")
                    st.info(mock.notes)
    
    session.close()
