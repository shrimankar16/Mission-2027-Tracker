"""
Phase Engine - Detects and manages phase transitions
Handles auto-switching based on dates and status changes
"""
from datetime import date, datetime
from database.models import UserProfile, ChecklistItem, DailyLog, TopicMastery, Topic, Subject
from database.database import get_session


class PhaseEngine:
    """Manages phase detection and transitions"""
    
    PHASE_DATES = {
        1: (date(2026, 6, 26), date(2026, 9, 27)),    # Phase 1: 95 days
        2: (date(2026, 10, 1), date(2027, 2, 28)),    # Phase 2: ~150 days
        3: (date(2027, 3, 1), date(2027, 6, 30)),     # Phase 3: ~120 days
        4: (date(2027, 7, 1), date(2027, 9, 30)),     # Phase 4: ~90 days
        5: (date(2027, 10, 1), date(2027, 12, 31)),   # Phase 5: ~90 days
    }
    
    def __init__(self):
        self.session = get_session()
    
    def get_current_phase(self) -> int:
        """Determine current phase based on date and status"""
        user = self.session.query(UserProfile).first()
        if not user:
            return 1
        
        today = date.today()
        
        # Override: If placement secured, force Phase 3
        if user.placement_status == "secured":
            return 3
        
        # Date-based phase detection
        for phase, (start, end) in self.PHASE_DATES.items():
            if start <= today <= end:
                return phase
        
        # If past all phases
        if today > self.PHASE_DATES[5][1]:
            return 5
        
        return user.current_phase
    
    def check_and_switch_phase(self) -> tuple[bool, int, int]:
        """
        Check if phase should switch and execute switch
        Returns: (switched, old_phase, new_phase)
        """
        user = self.session.query(UserProfile).first()
        if not user:
            return False, 1, 1
        
        old_phase = user.current_phase
        new_phase = self.get_current_phase()
        
        if old_phase != new_phase:
            self._execute_phase_switch(user, old_phase, new_phase)
            return True, old_phase, new_phase
        
        return False, old_phase, new_phase
    
    def _execute_phase_switch(self, user: UserProfile, old_phase: int, new_phase: int):
        """Execute phase transition logic"""
        try:
            user.current_phase = new_phase
            user.last_updated = datetime.now()
            
            # Phase 3 specific: Auto-complete already studied topics
            if new_phase == 3 and old_phase < 3:
                self._auto_complete_phase3_topics()
            
            # Log the phase switch
            self._log_phase_switch(old_phase, new_phase)
            
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            raise e
    
    def _auto_complete_phase3_topics(self):
        """
        Auto-mark topics as complete when Phase 3 starts
        Topics done in Phase 1/2 for placement are already complete for SSC
        """
        # Get subjects that were already covered
        covered_subjects = ["Quantitative Aptitude", "Logical Reasoning", "English", "General Studies"]
        
        for subject_name in covered_subjects:
            subject = self.session.query(Subject).filter_by(name=subject_name).first()
            if not subject:
                continue
            
            # Get all topics from Phase 1
            topics = self.session.query(Topic).filter_by(
                subject_id=subject.id,
                phase=1
            ).all()
            
            for topic in topics:
                # Check if learn was completed
                learn_item = self.session.query(ChecklistItem).filter_by(
                    topic_id=topic.id,
                    item_type="learn",
                    completed=True
                ).first()
                
                if learn_item:
                    # Mark mastery as complete for SSC (auto-carry forward)
                    mastery = self.session.query(TopicMastery).filter_by(
                        topic_id=topic.id
                    ).first()
                    if mastery:
                        mastery.learn_done = True
                        # Note: Practice and revisions may still be pending
    
    def _log_phase_switch(self, old_phase: int, new_phase: int):
        """Log phase switch event"""
        today = date.today()
        daily_log = self.session.query(DailyLog).filter_by(log_date=today).first()
        
        if not daily_log:
            daily_log = DailyLog(
                log_date=today,
                total_study_minutes=0,
                tasks_completed=0,
                tasks_total=0,
                phase=new_phase,
                streak_day=0
            )
            self.session.add(daily_log)
        else:
            daily_log.phase = new_phase
    
    def get_phase_info(self, phase: int) -> dict:
        """Get information about a specific phase"""
        if phase not in self.PHASE_DATES:
            return {}
        
        start, end = self.PHASE_DATES[phase]
        today = date.today()
        
        total_days = (end - start).days + 1
        days_elapsed = max(0, (today - start).days)
        days_remaining = max(0, (end - today).days)
        
        # Calculate completion percentage
        completion_pct = min(100, (days_elapsed / total_days) * 100) if total_days > 0 else 0
        
        status = "Upcoming" if today < start else ("Active" if today <= end else "Completed")
        
        return {
            "phase": phase,
            "start_date": start,
            "end_date": end,
            "total_days": total_days,
            "days_elapsed": days_elapsed,
            "days_remaining": days_remaining,
            "completion_pct": completion_pct,
            "status": status
        }
    
    def close(self):
        """Close database session"""
        self.session.close()
