"""
Notes Page - Note-taking with markdown, tagging, and search
"""
import streamlit as st
from datetime import datetime
from database.database import get_session
from database.models import Note, Subject, Topic


def show():
    """Render notes page"""
    st.title("📝 Notes")
    
    session = get_session()
    
    # Create note section
    with st.expander("➕ Create New Note"):
        subjects = session.query(Subject).all()
        subject_names = [s.name for s in subjects]
        
        selected_subject = st.selectbox("Subject:", subject_names)
        
        subject_obj = session.query(Subject).filter_by(name=selected_subject).first()
        topics = session.query(Topic).filter_by(subject_id=subject_obj.id).all() if subject_obj else []
        topic_names = ["(General note)"] + [t.name for t in topics]
        
        selected_topic = st.selectbox("Topic (optional):", topic_names)
        
        title = st.text_input("Note Title:")
        content = st.text_area("Content (Markdown supported):", height=200)
        
        tags_input = st.text_input("Tags (comma-separated):", placeholder="formula, mnemonic, PYQ-insight")
        
        pinned = st.checkbox("Pin this note")
        
        if st.button("💾 Save Note"):
            if title.strip() and content.strip():
                topic_id = None
                if selected_topic != "(General note)":
                    topic_obj = session.query(Topic).filter_by(
                        subject_id=subject_obj.id,
                        name=selected_topic
                    ).first()
                    if topic_obj:
                        topic_id = topic_obj.id
                
                tags_list = [t.strip() for t in tags_input.split(",")] if tags_input else []
                
                note = Note(
                    subject_id=subject_obj.id,
                    topic_id=topic_id,
                    title=title.strip(),
                    content=content.strip(),
                    tags=tags_list,
                    pinned=pinned,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                session.add(note)
                session.commit()
                st.success("✅ Note saved!")
                st.rerun()
            else:
                st.error("Please fill in title and content")
    
    st.markdown("---")
    
    # Display notes
    st.markdown("### 📚 Your Notes")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_pinned_only = st.checkbox("Pinned only")
    
    with col2:
        subjects = session.query(Subject).all()
        filter_subject = st.selectbox("Filter by subject:", ["All"] + [s.name for s in subjects])
    
    with col3:
        search_query = st.text_input("Search notes:", placeholder="Keywords...")
    
    # Query notes
    notes_query = session.query(Note).filter_by(archived=False)
    
    if show_pinned_only:
        notes_query = notes_query.filter_by(pinned=True)
    
    if filter_subject != "All":
        subject_obj = session.query(Subject).filter_by(name=filter_subject).first()
        if subject_obj:
            notes_query = notes_query.filter_by(subject_id=subject_obj.id)
    
    notes = notes_query.order_by(Note.pinned.desc(), Note.updated_at.desc()).all()
    
    if search_query:
        notes = [n for n in notes if search_query.lower() in n.title.lower() or search_query.lower() in n.content.lower()]
    
    if not notes:
        st.info("No notes found. Create your first note above!")
    else:
        for note in notes:
            subject = session.query(Subject).filter_by(id=note.subject_id).first()
            topic = session.query(Topic).filter_by(id=note.topic_id).first() if note.topic_id else None
            
            pin_icon = "📌 " if note.pinned else ""
            
            with st.expander(f"{pin_icon}{note.title} - {subject.name if subject else 'Unknown'}"):
                if topic:
                    st.caption(f"📘 Topic: {topic.name}")
                
                st.markdown(note.content)
                
                if note.tags:
                    st.markdown("**Tags:** " + " ".join([f"`{tag}`" for tag in note.tags]))
                
                st.caption(f"Last updated: {note.updated_at.strftime('%b %d, %Y %I:%M %p')}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Archive", key=f"archive_{note.id}"):
                        note.archived = True
                        session.commit()
                        st.rerun()
                
                with col2:
                    if st.button("📌 Toggle Pin", key=f"pin_{note.id}"):
                        note.pinned = not note.pinned
                        session.commit()
                        st.rerun()
    
    session.close()
