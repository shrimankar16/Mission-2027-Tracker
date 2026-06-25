"""
Checklist Engine - Generates daily checklists with deduplication
Enforces max 5 items/day, topic sequence, and unified task display
"""
from datetime import date, timedelta
from database.models import ChecklistItem, Topic, Subject, TopicMastery, RevisionSchedule
from database.database import get_session
from sqlalchemy import and_


class ChecklistEngine:
    """Manages checklist generation and deduplication"""
    
    MAX_ITEMS_PER_DAY = 5
    
    def __init__(self):
        self.session = get_session()
    
    def get_today_checklist(self) -> list:
        """Get today's checklist items"""
        today = date.today()
        return self._get_checklist_for_date(today)
    
    def get_checklist_for_date(self, target_date: date) -> list:
        """Get checklist for specific date"""
        return self._get_checklist_for_date(target_date)
    
    def _get_checklist_for_date(self, target_date: date) -> list:
        """Internal method to fetch checklist"""
        items = self.session.query(ChecklistItem).filter(
            and_(
                ChecklistItem.scheduled_date == target_date,
                ChecklistItem.is_active == True
            )
        ).order_by(ChecklistItem.item_type).all()
        
        # Enrich with topic and subject info
        enriched_items = []
        for item in items:
            topic = self.session.query(Topic).filter_by(id=item.topic_id).first()
            if not topic:
                continue
            
            subject = self.session.query(Subject).filter_by(id=topic.subject_id).first()
            if not subject:
                continue
            
            enriched_items.append({
                "item": item,
                "topic": topic,
                "subject": subject,
                "counts_for": subject.counts_for
            })
        
        return enriched_items
    
    def get_overdue_items(self) -> list:
        """Get all overdue (uncompleted past) items"""
        today = date.today()
        
        items = self.session.query(ChecklistItem).filter(
            and_(
                ChecklistItem.scheduled_date < today,
                ChecklistItem.completed == False,
                ChecklistItem.is_active == True,
                ChecklistItem.skipped == False
            )
        ).order_by(ChecklistItem.scheduled_date).all()
        
        enriched_items = []
        for item in items:
            topic = self.session.query(Topic).filter_by(id=item.topic_id).first()
            if not topic:
                continue
            
            subject = self.session.query(Subject).filter_by(id=topic.subject_id).first()
            if not subject:
                continue
            
            enriched_items.append({
                "item": item,
                "topic": topic,
                "subject": subject,
                "counts_for": subject.counts_for,
                "days_overdue": (today - item.scheduled_date).days
            })
        
        return enriched_items
    
    def mark_complete(self, item_id: int, time_spent: int = None) -> bool:
        """Mark checklist item as complete"""
        try:
            item = self.session.query(ChecklistItem).filter_by(id=item_id).first()
            if not item:
                return False
            
            # Only set completed_at if not already set (write-once)
            if not item.completed_at:
                item.completed_at = date.today()
            
            item.completed = True
            
            if time_spent:
                item.time_spent_minutes = time_spent
            
            # Update topic mastery
            self._update_mastery(item)
            
            self.session.commit()
            return True
            
        except Exception as e:
            self.session.rollback()
            print(f"Error marking complete: {e}")
            return False
    
    def mark_incomplete(self, item_id: int) -> bool:
        """Uncheck a completed item (keeps completed_at for audit)"""
        try:
            item = self.session.query(ChecklistItem).filter_by(id=item_id).first()
            if not item:
                return False
            
            item.completed = False
            # DO NOT null out completed_at - keep for audit trail
            
            self.session.commit()
            return True
            
        except Exception as e:
            self.session.rollback()
            return False
    
    def mark_skipped(self, item_id: int, reason: str) -> bool:
        """Mark item as skipped"""
        try:
            item = self.session.query(ChecklistItem).filter_by(id=item_id).first()
            if not item:
                return False
            
            item.skipped = True
            item.skip_reason = reason
            
            self.session.commit()
            return True
            
        except Exception as e:
            self.session.rollback()
            return False
    
    def move_to_today(self, item_id: int) -> bool:
        """Move overdue item to today (catch-up)"""
        try:
            item = self.session.query(ChecklistItem).filter_by(id=item_id).first()
            if not item:
                return False
            
            today = date.today()
            item.scheduled_date = today
            
            self.session.commit()
            return True
            
        except Exception as e:
            self.session.rollback()
            return False
    
    def _update_mastery(self, item: ChecklistItem):
        """Update topic mastery when item completed"""
        mastery = self.session.query(TopicMastery).filter_by(
            topic_id=item.topic_id
        ).first()
        
        if not mastery:
            mastery = TopicMastery(topic_id=item.topic_id)
            self.session.add(mastery)
        
        # Update based on item type
        if item.item_type == "learn":
            mastery.learn_done = True
        elif item.item_type == "notes":
            mastery.notes_done = True
        elif item.item_type == "practice":
            mastery.practice_done = True
        elif item.item_type == "revise_d3":
            mastery.revise_d3_done = True
        elif item.item_type == "revise_d7":
            mastery.revise_d7_done = True
        elif item.item_type == "revise_d10":
            mastery.revise_d10_done = True
        
        # Check if fully mastered
        if all([
            mastery.learn_done,
            mastery.practice_done,
            mastery.revise_d3_done,
            mastery.revise_d7_done,
            mastery.revise_d10_done
        ]):
            mastery.mastered = True
    
    def get_week_checklist(self, start_date: date = None) -> dict:
        """Get checklist for entire week"""
        if not start_date:
            start_date = date.today()
        
        week_data = {}
        for i in range(7):
            day = start_date + timedelta(days=i)
            week_data[day] = self._get_checklist_for_date(day)
        
        return week_data
    
    def close(self):
        """Close database session"""
        self.session.close()
