"""
Analytics Engine - Calculates all metrics, readiness scores, and progress data
All values computed from database at runtime, never cached
"""
from datetime import date, timedelta
from database.models import (
    ChecklistItem, TopicMastery, MockTest, DailyLog, 
    Subject, Topic, UserProfile
)
from database.database import get_session
from sqlalchemy import func, and_


class AnalyticsEngine:
    """Computes all analytics and readiness scores"""
    
    def __init__(self):
        self.session = get_session()
    
    def get_dashboard_stats(self) -> dict:
        """Get key stats for dashboard"""
        user = self.session.query(UserProfile).first()
        if not user:
            return {}
        
        today = date.today()
        days_since_start = (today - user.start_date).days + 1
        
        return {
            "current_day": days_since_start,
            "current_phase": user.current_phase,
            "streak": self._calculate_streak(),
            "overall_completion": self._calculate_overall_completion(),
            "study_hours_today": self._get_study_hours_today(),
            "tasks_completed_today": self._get_tasks_completed_today(),
            "tasks_total_today": self._get_tasks_total_today()
        }
    
    def _calculate_streak(self) -> int:
        """Calculate current study streak"""
        today = date.today()
        streak = 0
        
        current_date = today
        while True:
            log = self.session.query(DailyLog).filter_by(log_date=current_date).first()
            if not log or log.tasks_completed == 0:
                break
            streak += 1
            current_date -= timedelta(days=1)
        
        return streak
    
    def _calculate_overall_completion(self) -> float:
        """Calculate overall roadmap completion %"""
        total_items = self.session.query(ChecklistItem).filter_by(
            is_active=True
        ).count()
        
        completed_items = self.session.query(ChecklistItem).filter_by(
            is_active=True,
            completed=True
        ).count()
        
        if total_items == 0:
            return 0.0
        
        return round((completed_items / total_items) * 100, 1)
    
    def _get_study_hours_today(self) -> float:
        """Get total study hours logged today"""
        today = date.today()
        
        result = self.session.query(
            func.sum(ChecklistItem.time_spent_minutes)
        ).filter(
            and_(
                ChecklistItem.scheduled_date == today,
                ChecklistItem.completed == True
            )
        ).scalar()
        
        minutes = result if result else 0
        return round(minutes / 60, 1)
    
    def _get_tasks_completed_today(self) -> int:
        """Count completed tasks today"""
        today = date.today()
        
        return self.session.query(ChecklistItem).filter(
            and_(
                ChecklistItem.scheduled_date == today,
                ChecklistItem.completed == True
            )
        ).count()
    
    def _get_tasks_total_today(self) -> int:
        """Count total tasks scheduled today"""
        today = date.today()
        
        return self.session.query(ChecklistItem).filter(
            and_(
                ChecklistItem.scheduled_date == today,
                ChecklistItem.is_active == True
            )
        ).count()
    
    def calculate_placement_readiness(self) -> float:
        """
        Calculate placement readiness score
        DSA: 40%, Aptitude+Reasoning+English: 60%
        """
        # DSA mastery
        dsa_subject = self.session.query(Subject).filter_by(
            name="Data Structures & Algorithms"
        ).first()
        
        dsa_score = 0
        if dsa_subject:
            dsa_score = self._get_subject_mastery_score(dsa_subject.id)
        
        # Aptitude/Reasoning/English mastery
        apt_reasoning_english = ["Quantitative Aptitude", "Logical Reasoning", "English"]
        are_score = 0
        
        for subject_name in apt_reasoning_english:
            subject = self.session.query(Subject).filter_by(name=subject_name).first()
            if subject:
                are_score += self._get_subject_mastery_score(subject.id)
        
        are_score = are_score / 3  # Average of three subjects
        
        # Weighted score
        placement_score = (dsa_score * 0.4) + (are_score * 0.6)
        
        return round(placement_score, 1)
    
    def calculate_ssc_readiness(self) -> float:
        """
        Calculate SSC CGL readiness
        Based on all relevant subjects mastery
        """
        ssc_subjects = ["Quantitative Aptitude", "Logical Reasoning", "English", "General Studies"]
        total_score = 0
        
        for subject_name in ssc_subjects:
            subject = self.session.query(Subject).filter_by(name=subject_name).first()
            if subject:
                total_score += self._get_subject_mastery_score(subject.id)
        
        return round(total_score / len(ssc_subjects), 1)
    
    def calculate_mpsc_readiness(self) -> float:
        """
        Calculate MPSC readiness
        Similar to SSC with GS emphasis
        """
        return self.calculate_ssc_readiness()
    
    def _get_subject_mastery_score(self, subject_id: int) -> float:
        """Get mastery % for a subject"""
        topics = self.session.query(Topic).filter_by(subject_id=subject_id).all()
        if not topics:
            return 0.0
        
        total_topics = len(topics)
        mastered_topics = 0
        
        for topic in topics:
            mastery = self.session.query(TopicMastery).filter_by(
                topic_id=topic.id
            ).first()
            
            if mastery and mastery.mastered:
                mastered_topics += 1
        
        return (mastered_topics / total_topics) * 100 if total_topics > 0 else 0.0
    
    def get_week_progress(self) -> dict:
        """Get this week's progress data"""
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        
        week_data = {}
        for i in range(7):
            day = week_start + timedelta(days=i)
            
            completed = self.session.query(ChecklistItem).filter(
                and_(
                    ChecklistItem.scheduled_date == day,
                    ChecklistItem.completed == True
                )
            ).count()
            
            total = self.session.query(ChecklistItem).filter(
                and_(
                    ChecklistItem.scheduled_date == day,
                    ChecklistItem.is_active == True
                )
            ).count()
            
            week_data[day.strftime("%A")] = {
                "completed": completed,
                "total": total,
                "percentage": round((completed / total * 100), 1) if total > 0 else 0
            }
        
        return week_data
    
    def get_subject_heatmap_data(self) -> dict:
        """Get subject-wise study hours for heatmap"""
        # Last 30 days
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        subjects = self.session.query(Subject).all()
        heatmap_data = {}
        
        for subject in subjects:
            daily_hours = []
            current_date = start_date
            
            while current_date <= end_date:
                # Get total time spent on this subject on this date
                topics = self.session.query(Topic).filter_by(
                    subject_id=subject.id
                ).all()
                
                topic_ids = [t.id for t in topics]
                
                minutes = self.session.query(
                    func.sum(ChecklistItem.time_spent_minutes)
                ).filter(
                    and_(
                        ChecklistItem.topic_id.in_(topic_ids),
                        ChecklistItem.scheduled_date == current_date,
                        ChecklistItem.completed == True
                    )
                ).scalar()
                
                daily_hours.append({
                    "date": current_date,
                    "hours": round((minutes / 60), 1) if minutes else 0
                })
                
                current_date += timedelta(days=1)
            
            heatmap_data[subject.name] = daily_hours
        
        return heatmap_data
    
    def close(self):
        """Close database session"""
        self.session.close()
