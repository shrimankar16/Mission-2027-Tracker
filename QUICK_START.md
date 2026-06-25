# Quick Start Guide - Career Command Center

## 🚀 Get Started in 3 Steps

### Step 1: Install Python
Make sure you have Python 3.11+ installed. Check with:
```bash
python --version
```

### Step 2: Install Dependencies
Open Command Prompt in this folder and run:
```bash
pip install -r requirements.txt
```

**OR** simply double-click `run.bat` (Windows) - it will create a virtual environment and install everything automatically.

### Step 3: Launch the App
```bash
streamlit run app.py
```

**OR** double-click `run.bat`

The app will open in your browser at `http://localhost:8501`

---

## ✅ First-Time Setup

When you open the app for the first time:

1. **Enter Your Name** - This will be displayed throughout the app
2. **Confirm Start Date** - Default is June 26, 2026 (Mission 2027 start)
3. **Click "Start Journey"** - This will:
   - Create the database
   - Seed all subjects and topics
   - Generate your complete roadmap
   - Set up the checklist system

**⚠️ This process takes 10-15 seconds. Don't close the app!**

---

## 📱 Daily Usage

### Every Morning:
1. Open the app (double-click `run.bat` or run `streamlit run app.py`)
2. Go to **Dashboard** to see today's 4-5 tasks
3. Check **Readiness Scores** to track your preparation level

### Throughout the Day:
1. Go to **Checklist** section
2. Check off tasks as you complete them
3. Log time spent for accurate analytics

### End of Day:
1. Review **Progress** charts
2. Add any **Notes** from today's study
3. Log **Mock Tests** if you took any

---

## 🎯 Navigation Overview

### 1. Dashboard 🎯
- Today's tasks preview
- Phase information
- Study streak counter
- Readiness gauges (Placement, SSC, MPSC)
- Status update buttons

### 2. Checklist 📋
- **Today Tab:** See and complete today's tasks
- **This Week Tab:** View entire week's schedule
- **Date Range Tab:** Custom date filtering
- **Overdue Tab:** Catch up on missed tasks

### 3. Roadmap 🗺️
- Complete phase timeline (Phase 1-5)
- Date ranges for each phase
- Focus areas per phase
- Current phase progress

### 4. Progress 📊
- Weekly completion charts
- Subject-wise analysis
- Readiness score trends
- Study hours tracking

### 5. Notes 📝
- Create markdown notes
- Link to subjects/topics
- Tag for organization
- Pin important notes
- Search functionality

### 6. Mock Tests 🎯
- Log test scores
- Track accuracy trends
- Analyze weak subjects
- View improvement over time

---

## 💡 Pro Tips

### Task Completion
- ✅ Check tasks as you complete them - data saves immediately
- ⏱️ Log time spent - this improves analytics accuracy
- 📅 Move overdue tasks to today using "Move to Today" button
- ⏭️ Skip tasks only when necessary (sick/emergency)

### Spaced Repetition
- After completing a LEARN task, revision tasks auto-schedule:
  - **D3:** 3 days after learning
  - **D7:** 7 days after learning
  - **D10:** 10 days after learning
- These appear automatically in your checklist
- Complete all 5 stages (Learn + Practice + 3 Revisions) to master a topic

### Phase Transitions
- **Phase 1 → 2:** Auto-starts October 1, 2026
- **Phase 2 → 3:** Auto-starts March 1, 2027 OR when placement secured
- **Phase 3 → 4:** Auto-starts July 1, 2027
- **Phase 4 → 5:** Auto-starts October 1, 2027

### Data Safety
- Database auto-backs up daily at midnight
- Backups stored in `/backups/` folder
- Completion data NEVER deleted (even if you uncheck)
- Safe to close browser - data persists in SQLite

---

## 🐛 Common Issues & Solutions

### "Module not found" error
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### App won't start
**Solution:** Check if port 8501 is free
```bash
streamlit run app.py --server.port 8502
```

### Database error on first launch
**Solution:** Delete `career_data.db` and restart - app will recreate it

### Revisions not appearing
**Solution:** Make sure you marked LEARN tasks as complete. Revisions only schedule after learn completion.

### Slow performance
**Solution:** 
- Close other browser tabs
- Check database size (should be < 50MB)
- Restart the app

---

## 🔄 Updating Your Status

Use the buttons on Dashboard:

### ✅ Mark Placement Secured
- Click when you get a placement offer
- App switches to Phase 3 (SSC focus)
- Previous placement tasks become inactive

### ✅ Group C Prelim Cleared
- Click when you clear MPSC Group C prelims
- Activates Group C Mains preparation in Phase 2
- Adjusts focus split to 70% Placement + 30% Mains

### ❌ Placement Failed (Feb 2027)
- Use if campus placement doesn't work out
- No impact on SSC/MPSC preparation
- Continues to Phase 3 as planned

---

## 📞 Need Help?

### Check These First:
1. README.md - Full documentation
2. This QUICK_START.md - Daily usage guide
3. Database backup in `/backups/` - For recovery

### Still Stuck?
- Restart the app: Close terminal, re-run `streamlit run app.py`
- Check database: Restore from backup if needed
- Fresh start: Delete `career_data.db` and run onboarding again

---

## 🎓 Remember

**This app is your command center, not a passive tracker.**

- Open it every morning
- Complete tasks every day
- Review progress every week
- Update status as you progress

**Mission 2027 Goal:** ASO at Ministry of External Affairs through SSC CGL 2027

**Placement & MPSC:** Financial safety nets while pursuing the ultimate goal

**Stay consistent. Track daily. Trust the process.** 💪

---

**Start Date:** June 26, 2026  
**Target:** December 31, 2027  
**Total Days:** 551

**Let's make it happen! 🚀**
