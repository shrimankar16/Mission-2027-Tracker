# Career Command Center - Mission 2027

A production-grade, dark-themed career management web application built for final-year engineering students preparing for **Campus Placement**, **SSC CGL 2027**, and **MPSC Group B/C** exams.

## 🎯 Overview

This application serves as your single daily command center that:
- Tells you exactly what to study today
- Tracks completion with persistent data (never loses progress)
- Shows real-time progress across all three career goals
- Implements spaced repetition (D3, D7, D10) for mastery
- Provides unified checklist with zero duplication

**Ultimate Goal:** Assistant Section Officer (ASO) at Ministry of External Affairs through SSC CGL 2027

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 3. First-Time Setup

On first launch:
1. Enter your name
2. Confirm start date (default: June 26, 2026)
3. Click "Start Journey" - the app will seed the entire roadmap database

## 📂 Project Structure

```
career_command_center/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── career_data.db             # SQLite database (created on first run)
│
├── database/
│   ├── models.py              # SQLAlchemy ORM models
│   ├── database.py            # Database connection & initialization
│   └── seed.py                # Roadmap seed data
│
├── engines/
│   ├── phase_engine.py        # Phase detection & switching
│   ├── checklist_engine.py    # Daily checklist generation
│   ├── revision_engine.py     # Spaced repetition scheduler
│   └── analytics_engine.py    # Progress & readiness calculations
│
├── pages/
│   ├── dashboard.py           # Dashboard view
│   ├── checklist.py           # Unified checklist
│   ├── roadmap.py             # Phase timeline
│   ├── progress.py            # Analytics & charts
│   ├── notes.py               # Note-taking system
│   └── mock_tests.py          # Mock test tracking
│
├── styles/
│   └── main.css               # Custom dark theme CSS
│
└── backups/                   # Auto-generated database backups
```

## 🔥 Key Features

### ✅ Unified Checklist
- **Zero Duplication:** Same topic appears once with multiple "Counts For" tags
- **Max 5 items/day:** Never overwhelms you
- **Automatic Overdue Tracking:** Missed tasks are flagged
- **Sequence Enforcement:** Practice only after Learn is complete

### 📊 Real-Time Analytics
- **Readiness Scores:** Placement, SSC CGL, MPSC (calculated from DB)
- **Study Streak:** Consecutive days with ≥1 task completed
- **Progress Tracking:** Week-by-week and subject-wise analysis

### 🔄 Spaced Repetition
- **Automatic Revision Scheduling:** D3, D7, D10 after learning
- **Never Miss a Revision:** Auto-inserts overdue revisions into today's list
- **Mastery Tracking:** Topics marked "Mastered" only after all 5 stages complete

### 🗓️ 5-Phase Roadmap
1. **Phase 1** (Jun-Sep 2026): DSA + Aptitude + Reasoning + English + Group C GS
2. **Phase 2** (Oct 2026-Feb 2027): Placement focus + Group C Mains (if cleared)
3. **Phase 3** (Mar-Jun 2027): SSC CGL intensive (80%) + MPSC Group B (20%)
4. **Phase 4** (Jul-Sep 2027): PYQs + Mocks
5. **Phase 5** (Oct-Dec 2027): Peak readiness - Full mocks only

### 💾 Data Safety
- **SQLite + WAL mode:** Concurrent read/write support
- **Write-once timestamps:** Audit trail preserved
- **Midnight auto-backup:** Daily database snapshots
- **Never deletes:** All data is permanent (archive only)

## 🎨 Design Philosophy

- **Dark theme only** - Professional military-planner aesthetic
- **No neon colors** - Muted, premium palette ($200 planner vibe)
- **8px spacing grid** - Consistent visual hierarchy
- **Fonts:** Space Grotesk (headings), Inter (body), JetBrains Mono (code/counters)

## 📖 Usage Guide

### Daily Workflow

1. **Open Dashboard**
   - See today's 4-5 tasks
   - Check current phase progress
   - View readiness scores

2. **Complete Tasks (Checklist)**
   - Check off items as you complete them
   - Log time spent (for analytics)
   - Overdue items auto-appear at top

3. **Track Progress**
   - Weekly completion charts
   - Subject-wise mastery
   - Mock test score trends

4. **Take Notes**
   - Link notes to subjects/topics
   - Tag for easy search
   - Pin important notes

5. **Log Mock Tests**
   - Record scores, accuracy, time
   - Track improvement over time
   - Analyze weak areas

### Status Updates

Use dashboard buttons to update your progress:
- ✅ **Mark Placement Secured** → Switches to Phase 3 (SSC focus)
- ✅ **Group C Prelim Cleared** → Adjusts Phase 2 focus split
- ❌ **Placement Failed** → Continues to Phase 3 (no impact on SSC prep)

## 🔧 Technical Details

### Database Schema

- **UserProfile:** Name, current phase, placement/Group C status
- **Subject:** Name, applies to which exams, active phase
- **Topic:** Part of subject, subtopics list, scheduled date
- **ChecklistItem:** Learn/Practice/Revise items, completion tracking
- **RevisionSchedule:** D3/D7/D10 dates per topic
- **TopicMastery:** 6-stage mastery tracking (Learn → Practice → 3 Revisions)
- **Note:** Markdown notes with tags
- **MockTest:** Test scores, subject breakdown, analysis
- **DailyLog:** Study minutes, tasks completed, streak tracking

### Background Jobs (APScheduler)

- **Midnight Revision Check:** Scans completed LEARN items, schedules D3/D7/D10
- **Midnight Backup:** Creates daily database snapshot

## 🛠️ Customization

### Extending the Seed Data

The `database/seed.py` file contains Phase 1 topics as a framework. To add more:

1. Add topics to `create_dsa_topics()`, `create_aptitude_topics()`, etc.
2. For Phase 3+ topics (Ancient History, World Geography, etc.), extend `create_gs_topics()` or create new functions
3. The seed only runs once on empty database

### Adding More Subjects

```python
new_subject = Subject(
    name="Your Subject",
    counts_for=["placement", "ssc"],  # Applies to which exams
    phase_introduced=1,
    is_active=True
)
session.add(new_subject)
```

## 🐛 Troubleshooting

### Database Issues

If database gets corrupted:
1. Restore from `backups/career_db_YYYYMMDD.sqlite`
2. Copy to root as `career_data.db`

### Revision Not Auto-Scheduling

- Run `revision_engine.run_catch_up()` manually
- Check if `LEARN` items are marked complete (revision needs this)

### Performance on Large Data

- Database uses WAL mode for better concurrency
- Consider adding indexes if query time > 1 second

## 📝 Development Status

**Current Version:** 1.0 (Foundation Build)

### ✅ Implemented
- Core database models & seed framework
- Phase detection & auto-switching
- Checklist engine with deduplication
- Spaced repetition scheduler
- Dashboard with readiness scores
- Notes system
- Mock test tracking
- Dark theme styling

### 🚧 Future Enhancements
- Complete Phase 1-5 seed data (currently framework only)
- Subject heatmap visualization
- PDF/Excel export for notes & progress
- Calendar view for roadmap
- Mobile-responsive design
- Multi-user support (currently single-user)

## 📜 License

Personal use only. Built for Mission 2027.

## 🎓 Credits

Designed and developed for final-year engineering students balancing campus placement prep with government exam preparation (SSC CGL, MPSC).

**Built with:** Python, Streamlit, SQLite, SQLAlchemy, Plotly, APScheduler

---

**Mission 2027:** Campus Placement ✓ → SSC CGL ASO at MEA 🎯 → Financial Security 💪
