# Quick Reference Card - Career Command Center

## 🚀 Essential Commands

```bash
# Install
pip install -r requirements.txt

# Launch
streamlit run app.py

# OR (Windows)
run.bat

# Verify Setup
python verify_setup.py
```

---

## 📍 URLs

**Local App:** http://localhost:8501  
**Alternate Port:** http://localhost:8502  

---

## 📂 Key Files

| File | Purpose |
|------|---------|
| `career_data.db` | Your main database (DON'T DELETE!) |
| `/backups/` | Daily auto-backups |
| `app.py` | Main application entry point |
| `requirements.txt` | Python dependencies |

---

## 📚 Documentation Quick Links

| Need | Read This |
|------|-----------|
| Get started NOW | **START_HERE.md** |
| Daily workflow | **QUICK_START.md** |
| Setup problems | **INSTALLATION.md** |
| Test everything | **VERIFICATION_CHECKLIST.md** |
| Understand system | **PROJECT_SUMMARY.md** |
| Build info | **BUILD_COMPLETE.md** |
| Feature list | **README.md** |

---

## 🎯 Daily Workflow

1. **Open app** (`run.bat` or `streamlit run app.py`)
2. **Dashboard** → See today's tasks
3. **Checklist** → Check off as you complete
4. **Log time** → Click time button after checking
5. **Review progress** → Weekly check

---

## 📊 The 6 Sections

| Section | Shortcut | Purpose |
|---------|----------|---------|
| 🎯 Dashboard | First page | Daily command center |
| 📋 Checklist | Click "Checklist" | Task management |
| 🗺️ Roadmap | Click "Roadmap" | Phase timeline |
| 📊 Progress | Click "Progress" | Analytics |
| 📝 Notes | Click "Notes" | Knowledge base |
| 🎯 Mock Tests | Click "Mock Tests" | Test tracking |

---

## ⚡ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Refresh page | `Ctrl + R` or `F5` |
| Stop app | `Ctrl + C` (in terminal) |
| Zoom in | `Ctrl + Plus` |
| Zoom out | `Ctrl + Minus` |

---

## 🎨 Color Meanings

| Color | Meaning |
|-------|---------|
| 🟡 Gold (#C9A84C) | LEARN tasks, Primary buttons |
| 🟢 Sage (#6B8F71) | REVISE tasks, Completion |
| 🔵 Slate (#5B7FA6) | PRACTICE tasks, Links |
| 🔴 Terracotta (#A0522D) | Overdue, Warnings |

---

## 🏷️ Badge Types

| Badge | Task Type | When It Appears |
|-------|-----------|-----------------|
| **LEARN** | New concept | Every new topic |
| **PRACTICE** | Apply concept | After Learn is done |
| **REVISE D3** | 1st revision | 3 days after Learn |
| **REVISE D7** | 2nd revision | 7 days after Learn |
| **REVISE D10** | 3rd revision | 10 days after Learn |
| **CURRENT AFFAIRS** | Daily news | Every day in Phase 1 & 3 |
| **MOCK** | Full test | Phase 4 & 5 mostly |

---

## 📅 Phase Timeline

| Phase | Dates | Focus | Auto-Switch |
|-------|-------|-------|-------------|
| 1 | Jun-Sep 2026 | DSA + Aptitude + GS | Oct 1, 2026 |
| 2 | Oct 2026-Feb 2027 | Placement 70-100% | Mar 1, 2027 |
| 3 | Mar-Jun 2027 | SSC 80% + MPSC 20% | Jul 1, 2027 |
| 4 | Jul-Sep 2027 | PYQs + Mocks | Oct 1, 2027 |
| 5 | Oct-Dec 2027 | Peak readiness | Dec 31, 2027 |

---

## 🔢 Key Metrics

| Metric | Formula | Goal |
|--------|---------|------|
| **Placement Readiness** | DSA (40%) + ARE (60%) | >80% |
| **SSC Readiness** | Avg all subjects | >80% |
| **Study Streak** | Consecutive days with ≥1 task | 30+ days |
| **Overall Progress** | Tasks done / Total tasks | 100% by Dec 2027 |
| **Topic Mastery** | All 6 stages complete | As many as possible |

---

## ✅ Completion Stages (6 total)

1. ✓ LEARN
2. ✓ PRACTICE
3. ✓ REVISE D3
4. ✓ REVISE D7
5. ✓ REVISE D10
6. ✓ MASTERED (auto-flag when all above done)

---

## 🚨 Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| App won't start | `pip install -r requirements.txt` |
| Port in use | `streamlit run app.py --server.port 8502` |
| Tasks not showing | Check database file exists (>100KB) |
| Data disappeared | SHOULD NEVER HAPPEN - restore from backup |
| Slow performance | Close other tabs, restart app |
| No revisions | Check if LEARN tasks are marked complete |

---

## 💾 Backup & Restore

### Manual Backup
```bash
# Windows
copy career_data.db backup.db

# Mac/Linux
cp career_data.db backup.db
```

### Restore from Backup
```bash
# Windows
copy backup.db career_data.db

# Mac/Linux
cp backup.db career_data.db
```

### Auto Backups
- **When:** Every night at 00:05
- **Where:** `/backups/` folder
- **Format:** `career_db_YYYYMMDD.sqlite`

---

## 🎯 "Counts For" Tags

| Tag | Exam |
|-----|------|
| **[Placement]** | Campus placement |
| **[SSC]** | SSC CGL |
| **[MPSC Group C]** | MPSC Group C |
| **[MPSC Group B]** | MPSC Group B |

*Same task can have multiple tags = study once, benefit multiple times!*

---

## 📝 Note Tags (Suggested)

| Tag | Use For |
|-----|---------|
| `formula` | Mathematical formulas |
| `mnemonic` | Memory tricks |
| `pyq-insight` | Previous year question patterns |
| `weak-point` | Topics you struggle with |
| `important` | Critical concepts |
| `revision` | Quick review points |

---

## 🎯 Mission Goals

| Goal | Exam | Timeline | Priority |
|------|------|----------|----------|
| **ASO at MEA** | SSC CGL 2027 | Throughout 2027 | ⭐⭐⭐ |
| **Campus Placement** | Various | Feb 2027 | ⭐⭐ |
| **MPSC Group B/C** | MPSC | 2027 | ⭐ |

**Primary target:** Assistant Section Officer at Ministry of External Affairs  
**Method:** SSC CGL 2027  
**Backup:** Placement + MPSC for financial security

---

## 📞 When You Need Help

1. **Terminal shows error** → Copy error text, search in INSTALLATION.md
2. **Feature doesn't work** → Run `python verify_setup.py`
3. **Confused about workflow** → Read QUICK_START.md
4. **Want to understand why** → Read PROJECT_SUMMARY.md

---

## ✨ Pro Tips

1. **Open app EVERY morning** - builds habit
2. **Check tasks off immediately** - data saves instantly
3. **Log time spent** - improves analytics accuracy
4. **Don't skip revisions** - they're scientifically timed
5. **Trust the system** - it knows the optimal path
6. **Check backups weekly** - peace of mind
7. **Review progress on Sundays** - weekly reflection
8. **Pin important notes** - quick access
9. **Log every mock test** - trend analysis works best with data
10. **Follow the phases** - don't skip ahead

---

## 🔐 Security Reminders

✅ **Data stored locally** - you control it  
✅ **No cloud sync** - privacy by design  
✅ **Daily backups** - disaster recovery ready  
✅ **Transaction safe** - data integrity guaranteed  

❌ **Never share database file** - contains your personal data  
❌ **Don't edit manually** - use app interface only  

---

## 📊 Success Milestones

| Milestone | When | Metric |
|-----------|------|--------|
| 🔥 First Streak | Week 1 | 7 days |
| 📚 Foundation | Month 1 | 30 topics mastered |
| 💪 Discipline | Month 2 | 60 day streak |
| 🎯 Readiness | Month 3 | 40%+ placement score |
| 🏆 Phase 1 Done | Sep 2026 | All Phase 1 topics |
| 💼 Placement | Feb 2027 | Job offer |
| 🎓 SSC CGL | 2027 | ASO rank |
| ✅ Mission Complete | Dec 2027 | All goals achieved |

---

## ⏱️ Time Estimates

| Activity | Duration |
|----------|----------|
| LEARN task | 45-60 min |
| PRACTICE task | 45-60 min |
| REVISE task | 15-20 min |
| CURRENT AFFAIRS | 10 min |
| MOCK test (full) | 120 min |
| Daily total | 2-3 hours |

---

## 🎮 Gamification Elements

- 🔥 **Streak Counter** - Don't break the chain!
- 📊 **Readiness Gauges** - Watch them grow!
- ✅ **Completion Checkmarks** - Satisfying clicks!
- 🏆 **Mastery Badges** - Topics fully conquered!
- 📈 **Trend Charts** - Visualize improvement!

---

## 💬 Daily Affirmations

**Morning:** "The app tells me what to do. I trust the system."  
**During study:** "This task counts for multiple exams. Efficient learning."  
**After completing:** "Data saved. Progress logged. One day closer."  
**Evening:** "Streak maintained. Readiness increased. Mission continues."

---

## 📅 The Numbers

**Total Days:** 551  
**Start:** June 26, 2026  
**End:** December 31, 2027  
**Phases:** 5  
**Subjects:** 6 main (DSA, Aptitude, Reasoning, English, GS, Current Affairs)  
**Topics:** 150+ (across all subjects)  
**Goal:** ASO at Ministry of External Affairs  

---

## 🎯 One-Sentence Summary

**"Open app → See tasks → Complete them → Log time → Repeat for 551 days → Achieve goals."**

---

## ✅ Before You Close This Card

- [ ] Bookmark this page
- [ ] Read START_HERE.md next
- [ ] Install dependencies
- [ ] Launch app
- [ ] Complete onboarding
- [ ] Check first task
- [ ] Begin Mission 2027

---

**Quick Reference v1.0**  
**Last Updated:** June 25, 2026  
**Keep this handy throughout your journey!**

🚀 **Now go build your future!** 🚀
