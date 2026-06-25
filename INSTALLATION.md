# Installation Guide - Career Command Center

## 📋 Prerequisites

### Required Software
1. **Python 3.11 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   
2. **pip** (comes with Python)
   - Verify: `pip --version`

### Recommended (Optional)
- **Git** (for version control)
- **VS Code** (for editing/viewing code)

---

## 🛠️ Installation Methods

### Method 1: Quick Install (Windows - Recommended)

1. **Download/Extract** the project folder
2. **Double-click** `run.bat`
   - This will automatically:
     - Create a virtual environment
     - Install all dependencies
     - Launch the application

3. **Wait** for browser to open with the app

**That's it! Skip to "First Launch" section below.**

---

### Method 2: Manual Install (All Platforms)

#### Step 1: Open Terminal/Command Prompt

**Windows:**
- Press `Win + R`
- Type `cmd` and press Enter
- Navigate to project folder:
  ```bash
  cd C:\Users\Shrijay\Desktop\Mission-2027-Tracker
  ```

**Mac/Linux:**
- Open Terminal
- Navigate to project folder:
  ```bash
  cd /path/to/Mission-2027-Tracker
  ```

#### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

**Activate virtual environment:**

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (web framework)
- SQLAlchemy (database ORM)
- Plotly (charts)
- APScheduler (background jobs)
- And other dependencies

**Installation takes 2-5 minutes depending on internet speed.**

#### Step 4: Verify Installation

```bash
python verify_setup.py
```

This will check:
- Python version
- All dependencies
- File structure
- Database access

If all checks pass ✅, proceed to Step 5.

#### Step 5: Launch the App

```bash
streamlit run app.py
```

The app will open automatically in your default browser at `http://localhost:8501`

---

## 🚀 First Launch

### Onboarding Screen

When you first open the app, you'll see:

```
🎯 Career Command Center
Mission 2027

Welcome!
This is your unified command center for:
- 🏢 Campus Placement (Feb 2027)
- 📚 SSC CGL 2027 (Ultimate Goal: ASO at MEA)
- 🏛️ MPSC Group B/C (Financial Safety Net)

Enter your name: [          ]
Start date: [June 26, 2026]

         [🚀 Start Journey]
```

### Complete Onboarding

1. **Enter your name** (e.g., "Shrijay")
2. **Confirm start date** (default: June 26, 2026)
3. **Click "Start Journey"**

### What Happens Next?

The app will:
- Create `career_data.db` (SQLite database)
- Seed all subjects (DSA, Aptitude, Reasoning, English, GS)
- Create topics and subtopics
- Generate initial checklist structure
- Set up revision schedule framework

**⏱️ This takes 10-20 seconds. DO NOT close the app!**

### Success!

You'll see the Dashboard with:
- Today's date and day counter
- Current phase information
- Study streak (starts at 0)
- Overall progress (starts at 0%)
- Readiness gauges (all at 0%)

**You're all set! Check QUICK_START.md for daily usage guide.**

---

## 🔧 Troubleshooting

### Issue: Python not found

**Error:**
```
'python' is not recognized as an internal or external command
```

**Solution:**
1. Reinstall Python from python.org
2. During installation, check "Add Python to PATH"
3. Restart Command Prompt
4. Verify: `python --version`

---

### Issue: pip not found

**Error:**
```
'pip' is not recognized as an internal or external command
```

**Solution:**
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

---

### Issue: Module not found during installation

**Error:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
1. Ensure virtual environment is activated (see `(venv)` in prompt)
2. Run: `pip install -r requirements.txt`
3. If still fails, install individually:
   ```bash
   pip install streamlit
   pip install sqlalchemy
   pip install plotly
   # ... etc
   ```

---

### Issue: Port 8501 already in use

**Error:**
```
Port 8501 is in use by another program
```

**Solution:**
1. Close other Streamlit apps
2. OR use different port:
   ```bash
   streamlit run app.py --server.port 8502
   ```

---

### Issue: Database locked

**Error:**
```
database is locked
```

**Solution:**
1. Close all instances of the app
2. If problem persists, restart computer
3. SQLite WAL mode should prevent this, but can occur if app crashes

---

### Issue: Slow performance

**Symptoms:**
- App takes long to load
- Charts render slowly
- Lag when clicking tasks

**Solution:**
1. Check database size:
   - Should be < 50MB for optimal performance
   - Large backups? Delete old ones in `/backups/`

2. Clear browser cache

3. Restart the app:
   ```bash
   # Press Ctrl+C in terminal
   # Then run again:
   streamlit run app.py
   ```

4. Check system resources (Task Manager on Windows)

---

### Issue: Can't see today's tasks

**Problem:**
Dashboard shows "No tasks scheduled for today"

**Solution:**
1. Check if database was seeded:
   - File `career_data.db` should exist
   - Size should be > 100KB

2. Re-run onboarding:
   - Delete `career_data.db`
   - Restart app
   - Complete onboarding again

3. Manually trigger revision check:
   - This is automatic at midnight
   - If app wasn't running at midnight, tasks may not generate

---

### Issue: Revisions not appearing

**Problem:**
Completed LEARN tasks but no revision tasks showing up

**Solution:**
1. Revisions schedule after LEARN is marked complete
2. Check Overdue tab in Checklist section
3. Revision dates:
   - D3: 3 days after learning
   - D7: 7 days after learning
   - D10: 10 days after learning

4. Manually trigger:
   ```python
   # In Python console:
   from engines.revision_engine import RevisionEngine
   engine = RevisionEngine()
   engine.run_catch_up()
   ```

---

### Issue: Data disappeared after browser refresh

**Problem:**
Checked off tasks but they're unchecked after refresh

**This should NEVER happen** - if it does:

1. Check `career_data.db` file size
   - Should grow as you add data
   - If stays same size, database writes are failing

2. Check file permissions
   - Ensure you have write access to project folder

3. Check for database backup
   - Look in `/backups/` folder
   - Restore latest backup if needed

4. Last resort: Report as bug
   - This violates core data integrity rules

---

## 🔄 Updating the App

### If you get new files/updates:

1. **Backup your database first!**
   ```bash
   copy career_data.db career_data_backup.db
   ```

2. **Replace files** (except `career_data.db`)

3. **Install new dependencies** (if any)
   ```bash
   pip install -r requirements.txt --upgrade
   ```

4. **Restart the app**
   ```bash
   streamlit run app.py
   ```

---

## 🗑️ Uninstalling

### Complete Removal

1. **Delete project folder**
   - This removes all code, database, and backups

2. **Remove virtual environment** (if created outside project)
   ```bash
   deactivate  # First, exit venv
   rmdir /s venv  # Windows
   rm -rf venv  # Mac/Linux
   ```

### Keep Data, Remove App

1. **Backup database**
   ```bash
   copy career_data.db ~/Desktop/career_backup.db
   ```

2. **Delete everything else**

3. **Later, restore data**
   - Put `career_backup.db` in new installation as `career_data.db`

---

## 📦 Dependencies Reference

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | ≥1.35.0 | Web framework |
| sqlalchemy | ≥2.0.0 | Database ORM |
| plotly | ≥5.22.0 | Interactive charts |
| pandas | ≥2.2.0 | Data manipulation |
| pydantic | ≥2.0.0 | Data validation |
| apscheduler | ≥3.10.4 | Background jobs |
| reportlab | ≥4.2.0 | PDF export |
| openpyxl | ≥3.1.2 | Excel export |
| python-docx | ≥1.1.2 | Word export |
| bcrypt | ≥4.1.3 | Password hashing |
| streamlit-aggrid | ≥0.3.4 | Advanced tables |
| streamlit-calendar | ≥1.0.3 | Calendar view |

---

## ✅ Post-Installation Checklist

- [ ] Python 3.11+ installed
- [ ] All dependencies installed (`pip list`)
- [ ] `verify_setup.py` runs without errors
- [ ] App launches in browser
- [ ] Onboarding completed
- [ ] Dashboard shows today's date
- [ ] Can navigate between sections
- [ ] Database file created (`career_data.db` exists)
- [ ] Can create a note (test Notes section)
- [ ] Can check off a task (test Checklist)

---

## 🆘 Still Need Help?

### Check These Resources:
1. **README.md** - Full project documentation
2. **QUICK_START.md** - Daily usage guide
3. **This file (INSTALLATION.md)** - Setup help
4. **verify_setup.py** - Diagnostic script

### Last Resort:
- Delete everything and start fresh
- Follow Method 1 (run.bat) for cleanest install

---

**Installation should take 5-10 minutes total.**

**Once set up, you'll use this app daily for the next 551 days!** 💪

**Good luck with Mission 2027! 🚀**
