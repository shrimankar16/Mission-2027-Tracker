"""
Revision Engine - Implements spaced repetition (D3, D7, D10)
Runs as APScheduler job at midnight to insert revision tasks
"""
from datetime import date, timedelta, datetime
from database.models import ChecklistItem, RevisionSchedule, Topic
from database.database import get_session
from apscheduler.schedulers.background import BackgroundScheduler


class RevisionEngine:
    """Manages spaced repetition scheduling"""
    
    def __init__(self):
        self.session = get_session()
        self.scheduler = BackgroundScheduler()
    
    def start_scheduler(self):
        """Start the APScheduler for midnight jobs"""
        # Run revision check at midnight every day
        self.scheduler.add_job(
            self.process_revisions,
            'cron',
            hour=0,
            minute=0,
            id='revision_check'
        )
        
        # Run backup at midnight
        from database.database import backup_database
        self.scheduler.add_job(
            backup_database,
            'cron',
            hour=0,
            minute=5,
            id='database_backup'
        )
        
        self.scheduler.start()
    
    def process_revisions(self):
        """
        Main revision processing - scans completed LEARN items
        and creates revision schedule + checklist items
        """
        try:
            # Get all completed LEARN items
            learn_items = self.session.query(ChecklistItem).filter_by(
                item_type="learn",
                completed=True,
                is_active=True
            ).all()
            
            for item in learn_items:
                self._create_revision_schedule(item)
            
            # Insert due revisions into today's checklist
            self._insert_due_revisions()
            
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            print(f"Revision processing error: {e}")
    
    def _create_revision_schedule(self, learn_item: ChecklistItem):
        """Create revision schedule for a completed LEARN item"""
        # Check if schedule already exists
        existing = self.session.query(RevisionSchedule).filter_by(
            topic_id=learn_item.topic_id
        ).first()
        
        if existing:
            return  # Already scheduled
        
        # Use completion date if available, else scheduled date
        base_date = learn_item.completed_at if learn_item.completed_at else learn_item.scheduled_date
        
        if isinstance(base_date, datetime):
            base_date = base_date.date()
        
        # Create schedule
        schedule = RevisionSchedule(
            topic_id=learn_item.topic_id,
            learn_completed_date=base_date,
            revision_d3_date=base_date + timedelta(days=3),
            revision_d7_date=base_date + timedelta(days=7),
            revision_d10_date=base_date + timedelta(days=10),
            revision_d3_done=False,
            revision_d7_done=False,
            revision_d10_done=False
        )
        
        self.session.add(schedule)
    
    def _insert_due_revisions(self):
        """Insert revision items that are due today"""
        today = date.today()
        
        # Find all schedules with due revisions
        schedules = self.session.query(RevisionSchedule).all()
        
        for schedule in schedules:
            # Check D3
            if schedule.revision_d3_date <= today and not schedule.revision_d3_done:
                self._create_revision_checklist_item(
                    schedule.topic_id,
                    "revise_d3",
                    schedule.revision_d3_date
                )
            
            # Check D7
            if schedule.revision_d7_date <= today and not schedule.revision_d7_done:
                self._create_revision_checklist_item(
                    schedule.topic_id,
                    "revise_d7",
                    schedule.revision_d7_date
                )
            
            # Check D10
            if schedule.revision_d10_date <= today and not schedule.revision_d10_done:
                self._create_revision_checklist_item(
                    schedule.topic_id,
                    "revise_d10",
                    schedule.revision_d10_date
                )
    
    def _create_revision_checklist_item(self, topic_id: int, revision_type: str, scheduled_date: date):
        """Create a revision checklist item if it doesn't exist"""
        # Check if already exists
        existing = self.session.query(ChecklistItem).filter_by(
            topic_id=topic_id,
            item_type=revision_type,
            scheduled_date=scheduled_date
        ).first()
        
        if existing:
            return
        
        topic = self.session.query(Topic).filter_by(id=topic_id).first()
        if not topic:
            return
        
        # Create checklist item
        item = ChecklistItem(
            topic_id=topic_id,
            item_type=revision_type,
            description=f"Revise: {topic.name} ({revision_type.upper()})",
            scheduled_date=scheduled_date,
            completed=False,
            is_active=True
        )
        
        self.session.add(item)
    
    def mark_revision_done(self, topic_id: int, revision_type: str):
        """Mark a revision as done in the schedule"""
        schedule = self.session.query(RevisionSchedule).filter_by(
            topic_id=topic_id
        ).first()
        
        if not schedule:
            return
        
        try:
            if revision_type == "revise_d3":
                schedule.revision_d3_done = True
            elif revision_type == "revise_d7":
                schedule.revision_d7_done = True
            elif revision_type == "revise_d10":
                schedule.revision_d10_done = True
            
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            print(f"Error marking revision done: {e}")
    
    def run_catch_up(self):
        """
        Run revision check immediately (for when app wasn't opened at midnight)
        """
        self.process_revisions()
    
    def close(self):
        """Close session and shutdown scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
        self.session.close()
