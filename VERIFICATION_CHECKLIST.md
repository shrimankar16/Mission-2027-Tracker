# Verification Checklist - Career Command Center

Use this checklist to verify that your Career Command Center is working correctly after installation.

## 📋 Installation Verification

### Step 1: Pre-Launch Checks

- [ ] Python 3.11+ is installed (`python --version`)
- [ ] All dependencies installed (`pip list` shows streamlit, sqlalchemy, etc.)
- [ ] `verify_setup.py` runs without errors
- [ ] No red ❌ marks in verify_setup output

### Step 2: First Launch

- [ ] Run `streamlit run app.py` (or double-click `run.bat`)
- [ ] Browser opens automatically at `localhost:8501`
- [ ] Onboarding screen appears
- [ ] No error messages in terminal/console

### Step 3: Onboarding

- [ ] Can enter your name
- [ ] Can select start date
- [ ] "Start Journey" button works
- [ ] Loading/spinner appears (10-20 seconds)
- [ ] Dashboard appears after seeding

---

## 🎯 Feature Verification

### Dashboard Page

- [ ] **Top Stat Cards Display:**
  - [ ] Today's date shows correctly
  - [ ] "Day X of 551" counter appears
  - [ ] Current Phase shows "Phase 1"
  - [ ] Study streak shows "0 days" initially
  - [ ] Overall progress shows "0%" initially

- [ ] **Today's Checklist Preview:**
  - [ ] Shows 4-5 tasks (or "No tasks scheduled")
  - [ ] Each task has a badge (LEARN/PRACTICE/REVISE)
  - [ ] Subject and topic names display
  - [ ] "Counts For" tags appear (Placement, SSC, etc.)

- [ ] **Readiness Gauges:**
  - [ ] Three gauge charts render (Placement, SSC, MPSC)
  - [ ] All show 0% or low percentage initially
  - [ ] Charts have dark background

- [ ] **Status Buttons:**
  - [ ] Four buttons visible at bottom
  - [ ] Clicking button shows confirmation or warning
  - [ ] No errors when clicking

### Checklist Page

- [ ] **Today Tab:**
  - [ ] Tasks display in cards
  - [ ] Can check off a task
  - [ ] Checkbox state saves (refresh page - stays checked)
  - [ ] Time logging option appears after checking
  - [ ] Can log time spent

- [ ] **This Week Tab:**
  - [ ] Shows 7 days (Mon-Sun)
  - [ ] Today is highlighted
  - [ ] Tasks appear under each day
  - [ ] "No tasks scheduled" for empty days

- [ ] **Date Range Tab:**
  - [ ] Date pickers work
  - [ ] "Load Tasks" button works
  - [ ] Shows tasks for selected range

- [ ] **Overdue Tab:**
  - [ ] Shows "No overdue tasks" initially
  - [ ] (Later: Will show missed tasks from past days)

### Roadmap Page

- [ ] **Phase Timeline:**
  - [ ] All 5 phases listed
  - [ ] Phase 1 shows as "Active"
  - [ ] Date ranges display correctly
  - [ ] Completion percentage shows
  - [ ] Border colors match status

- [ ] **Phase Details:**
  - [ ] Can expand each phase
  - [ ] Focus percentages show
  - [ ] Goal descriptions display

### Progress Page

- [ ] **Overview Tab:**
  - [ ] Week progress chart renders
  - [ ] Chart has dark background
  - [ ] Readiness scores display
  - [ ] All three metrics show

- [ ] **Subject Analysis Tab:**
  - [ ] "Feature coming soon" message
  - [ ] No errors

- [ ] **Phase Progress Tab:**
  - [ ] 5 phases listed
  - [ ] Progress bars display
  - [ ] Percentages show

### Notes Page

- [ ] **Create Note:**
  - [ ] Subject dropdown populates
  - [ ] Topic dropdown works
  - [ ] Can type title and content
  - [ ] Tags field works
  - [ ] Pin checkbox works
  - [ ] "Save Note" button works
  - [ ] Success message appears
  - [ ] Note appears in list below

- [ ] **View Notes:**
  - [ ] Saved notes display in expandable cards
  - [ ] Can see note content
  - [ ] Tags display
  - [ ] Pin icon shows if pinned
  - [ ] Archive button works
  - [ ] Toggle pin works

- [ ] **Search/Filter:**
  - [ ] "Pinned only" checkbox works
  - [ ] Subject filter works
  - [ ] Search box filters notes

### Mock Tests Page

- [ ] **Log Mock Test:**
  - [ ] Exam type dropdown works
  - [ ] All input fields accept values
  - [ ] Auto-calculation works (attempted = correct + wrong)
  - [ ] Notes field works
  - [ ] "Save Mock Test" button works
  - [ ] Test appears in history

- [ ] **View Tests:**
  - [ ] Quick stats display (Total, Avg, Best)
  - [ ] Test list shows saved tests
  - [ ] Can expand test details
  - [ ] All data displays correctly

---

## 🔄 Data Persistence Verification

### Test 1: Browser Refresh

1. [ ] Check off a task in Checklist
2. [ ] Refresh browser (F5 or Ctrl+R)
3. [ ] Verify task stays checked ✓

### Test 2: App Restart

1. [ ] Check off a task
2. [ ] Close browser completely
3. [ ] Stop app (Ctrl+C in terminal)
4. [ ] Restart app (`streamlit run app.py`)
5. [ ] Verify task stays checked ✓

### Test 3: Database File

1. [ ] Check that `career_data.db` file exists in root folder
2. [ ] Note the file size (should be > 100KB)
3. [ ] Complete a task
4. [ ] Check file size again (should grow slightly)

### Test 4: Backup Creation

1. [ ] Check `/backups/` folder
2. [ ] Wait until midnight (or test by changing system time)
3. [ ] Verify backup file appears: `career_db_YYYYMMDD.sqlite`

---

## 🧪 Functionality Tests

### Test A: Complete a Task

- [ ] Go to Checklist → Today
- [ ] Check off any task
- [ ] Dashboard updates automatically
- [ ] "Tasks completed today" increases by 1
- [ ] Task appears as completed in Checklist

### Test B: Log Time

- [ ] Complete a task
- [ ] Click time logging option
- [ ] Enter minutes (e.g., 45)
- [ ] Click save
- [ ] Time displays next to task
- [ ] Dashboard "Study hours today" updates

### Test C: Create and Find Note

- [ ] Go to Notes
- [ ] Create a test note with tags
- [ ] Save note
- [ ] Use search box to find it
- [ ] Pin the note
- [ ] Filter "Pinned only" - note appears

### Test D: Track Mock Test

- [ ] Go to Mock Tests
- [ ] Log a sample mock test
- [ ] Enter fake scores (e.g., 50/100)
- [ ] Save test
- [ ] Check that test appears in list
- [ ] Verify chart updates if multiple tests

### Test E: Phase Information

- [ ] Go to Dashboard
- [ ] Note current phase (should be 1)
- [ ] Check "days remaining in phase"
- [ ] Go to Roadmap
- [ ] Verify Phase 1 is marked "Active"

---

## 🚨 Error Checking

### No Errors Should Appear For:

- [ ] Navigating between pages
- [ ] Checking/unchecking tasks multiple times
- [ ] Creating multiple notes rapidly
- [ ] Filtering and searching
- [ ] Refreshing any page
- [ ] Closing and reopening app

### Terminal/Console Should Show:

- [ ] No Python exceptions
- [ ] No SQLAlchemy warnings
- [ ] No "connection failed" errors
- [ ] Green success messages only

---

## 📊 Data Integrity Checks

### Check 1: Completion Timestamps

1. [ ] Complete a task at a specific time
2. [ ] Note the completion time
3. [ ] Uncheck the task
4. [ ] Re-check the task
5. [ ] Verify original completion time preserved (audit trail)

### Check 2: No Data Loss

1. [ ] Complete 5 tasks
2. [ ] Create 3 notes
3. [ ] Log 1 mock test
4. [ ] Restart app
5. [ ] Verify all data still present
6. [ ] Count: 5 tasks checked, 3 notes, 1 mock test

### Check 3: Overdue Tracking

1. [ ] Leave a task unchecked for today
2. [ ] Change system date to tomorrow (or wait 24 hours)
3. [ ] Restart app
4. [ ] Go to Checklist → Overdue tab
5. [ ] Verify yesterday's unchecked task appears as overdue

---

## 🎨 Visual Verification

### Dark Theme

- [ ] Background is dark (#0D0F12 - almost black)
- [ ] Text is light/white (#E8EAF0)
- [ ] No bright white cards
- [ ] No neon colors visible
- [ ] Gold accent used for primary buttons (#C9A84C)
- [ ] Sage green used for completion (#6B8F71)

### Typography

- [ ] Headings use Space Grotesk font
- [ ] Body text uses Inter font
- [ ] Day counters use JetBrains Mono (monospace)

### Badges

- [ ] LEARN badge is gold
- [ ] PRACTICE badge is slate blue
- [ ] REVISE badge is sage green
- [ ] Badges have uppercase text

### Spacing

- [ ] Cards have consistent spacing
- [ ] No overlapping elements
- [ ] Readable line height
- [ ] Proper margins between sections

---

## ⚡ Performance Verification

### Speed Tests

- [ ] Dashboard loads in < 2 seconds
- [ ] Checklist page loads in < 2 seconds
- [ ] Charts render in < 1 second
- [ ] Task check/uncheck responds immediately (< 500ms)
- [ ] Navigation between pages is instant

### Responsiveness

- [ ] Can click buttons without lag
- [ ] Checkboxes respond immediately
- [ ] Dropdown menus open quickly
- [ ] Search/filter is instant

---

## 🔐 Security Verification

### Database

- [ ] `career_data.db` file is created in project root (not system folder)
- [ ] Backup folder `/backups/` contains only `.sqlite` files
- [ ] No sensitive data in plain text in app UI

### Session State

- [ ] Closing browser doesn't lose data
- [ ] Multiple browser tabs show consistent data
- [ ] No data "leakage" between sessions

---

## 📱 Browser Compatibility

Test in different browsers (if possible):

- [ ] **Chrome:** All features work
- [ ] **Firefox:** All features work
- [ ] **Edge:** All features work
- [ ] **Safari (Mac):** All features work

---

## ✅ Final Verification

### All Green Checklist

- [ ] All sections above completed
- [ ] No errors encountered
- [ ] Data persists correctly
- [ ] Dark theme renders properly
- [ ] All pages accessible
- [ ] Database file exists and grows
- [ ] Can complete full workflow: Check task → Log time → View progress

---

## 🎯 Ready for Daily Use

If all checks above pass ✅, your Career Command Center is:

✅ **FULLY FUNCTIONAL**  
✅ **DATA-SAFE**  
✅ **READY FOR MISSION 2027**

---

## 🐛 If Any Check Fails

1. **Note which check failed**
2. **Check INSTALLATION.md troubleshooting section**
3. **Run `verify_setup.py` again**
4. **Check terminal for error messages**
5. **Try deleting `career_data.db` and re-running onboarding**

---

## 📞 Verification Complete?

Once all checks pass, you're ready to:

1. ✅ Use the app daily
2. ✅ Trust the data
3. ✅ Follow the roadmap
4. ✅ Achieve Mission 2027 goals

**Bookmark this checklist for future reference if you update the app or restore from backup.**

---

**Total Checks:** 150+  
**Expected Time:** 15-20 minutes  
**Result:** Peace of mind that your system is production-ready 💪

**Good luck with Mission 2027! 🚀**
