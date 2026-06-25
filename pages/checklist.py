"""
Checklist Page - Unified checklist with deduplication
The most important section where users manage daily tasks
"""
import streamlit as st
from datetime import date, timedelta
from engines.checklist_engine import ChecklistEngine


def show():
    """Render checklist page"""
    st.title("📋 Unified Checklist")
    
    # View mode tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Today", "This Week", "Date Range", "Overdue"])
    
    checklist_engine = ChecklistEngine()
    
    with tab1:
        st.markdown("### Today's Tasks")
        render_checklist_items(checklist_engine.get_today_checklist(), checklist_engine)
    
    with tab2:
        st.markdown("### This Week")
        week_data = checklist_engine.get_week_checklist()
        
        for day, items in week_data.items():
            day_name = day.strftime("%A, %b %d")
            is_today = day == date.today()
            
            if is_today:
                st.markdown(f"#### 🎯 {day_name} (Today)")
            else:
                st.markdown(f"#### {day_name}")
            
            if not items:
                st.info("No tasks scheduled")
            else:
                render_checklist_items(items, checklist_engine, show_checkbox=False)
            
            st.markdown("---")
    
    with tab3:
        st.markdown("### Custom Date Range")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From:", value=date.today())
        with col2:
            end_date = st.date_input("To:", value=date.today() + timedelta(days=7))
        
        if st.button("Load Tasks"):
            current = start_date
            while current <= end_date:
                items = checklist_engine.get_checklist_for_date(current)
                st.markdown(f"#### {current.strftime('%A, %b %d, %Y')}")
                if items:
                    render_checklist_items(items, checklist_engine, show_checkbox=False)
                else:
                    st.info("No tasks")
                st.markdown("---")
                current += timedelta(days=1)
    
    with tab4:
        st.markdown("### ⚠️ Overdue Tasks")
        overdue_items = checklist_engine.get_overdue_items()
        
        if not overdue_items:
            st.success("✅ No overdue tasks! You're up to date.")
        else:
            st.warning(f"You have {len(overdue_items)} overdue tasks.")
            
            for item_data in overdue_items:
                item = item_data['item']
                topic = item_data['topic']
                subject = item_data['subject']
                days_overdue = item_data['days_overdue']
                
                with st.expander(f"[{days_overdue}d overdue] {subject.name} → {topic.name}"):
                    st.write(f"**Item Type:** {item.item_type.upper()}")
                    st.write(f"**Originally scheduled:** {item.scheduled_date.strftime('%b %d, %Y')}")
                    st.write(f"**Subtopics:** {', '.join(topic.subtopics)}")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("✅ Mark Complete", key=f"complete_{item.id}"):
                            checklist_engine.mark_complete(item.id)
                            st.success("Marked complete!")
                            st.rerun()
                    
                    with col2:
                        if st.button("📅 Move to Today", key=f"move_{item.id}"):
                            checklist_engine.move_to_today(item.id)
                            st.success("Moved to today!")
                            st.rerun()
                    
                    with col3:
                        skip_reason = st.selectbox(
                            "Skip reason:",
                            ["", "Sick", "Emergency", "Rest", "Other"],
                            key=f"skip_select_{item.id}"
                        )
                        if skip_reason and st.button("⏭️ Skip", key=f"skip_{item.id}"):
                            checklist_engine.mark_skipped(item.id, skip_reason)
                            st.info("Task skipped")
                            st.rerun()
    
    checklist_engine.close()


def render_checklist_items(items, engine, show_checkbox=True):
    """Render checklist items with interactive checkboxes"""
    if not items:
        st.info("No tasks scheduled")
        return
    
    for item_data in items:
        item = item_data['item']
        topic = item_data['topic']
        subject = item_data['subject']
        counts_for = item_data['counts_for']
        
        # Badge class
        badge_class = "badge-learn"
        if item.item_type == "practice":
            badge_class = "badge-practice"
        elif item.item_type.startswith("revise"):
            badge_class = "badge-revise"
        elif item.item_type == "current_affairs":
            badge_class = "badge-current-affairs"
        
        # Completion status
        completed_class = "completed" if item.completed else ""
        
        # Render item card
        st.markdown(f"""
        <div class="checklist-item {completed_class}">
            <span class="badge {badge_class}">{item.item_type.upper().replace('_', ' ')}</span>
            <strong style="color: var(--text-primary); font-size: 16px;">{subject.name}</strong> → {topic.name}
            <br>
            <small style="color: var(--text-secondary);">
                <strong>Subtopics:</strong> {', '.join(topic.subtopics)}
            </small>
            <br>
            <small>
                <strong>Counts for:</strong> 
                {"".join([f'<span class="tag">{c.replace("_", " ").title()}</span>' for c in counts_for])}
            </small>
        </div>
        """, unsafe_allow_html=True)
        
        if show_checkbox:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                checked = st.checkbox(
                    "Mark complete" if not item.completed else "Completed ✓",
                    value=item.completed,
                    key=f"check_{item.id}"
                )
                
                if checked != item.completed:
                    if checked:
                        engine.mark_complete(item.id)
                    else:
                        engine.mark_incomplete(item.id)
                    st.rerun()
            
            with col2:
                if checked and not item.time_spent_minutes:
                    with st.popover("⏱️ Log time"):
                        time_input = st.number_input(
                            "Minutes:",
                            min_value=1,
                            max_value=300,
                            value=45,
                            key=f"time_{item.id}"
                        )
                        if st.button("Save", key=f"save_time_{item.id}"):
                            engine.mark_complete(item.id, time_input)
                            st.rerun()
                elif item.time_spent_minutes:
                    st.caption(f"⏱️ {item.time_spent_minutes} min")
        
        st.markdown("<br>", unsafe_allow_html=True)
