# Deployment Guide - Mission 2027 Tracker

## 🚀 Deploy to Streamlit Community Cloud (Recommended - FREE)

### Prerequisites
- GitHub account
- Repository pushed to GitHub
- Streamlit Community Cloud account (sign up with GitHub)

### Step-by-Step Deployment

#### 1. **Prepare Your Repository**
Your repository is already ready! It includes:
- ✅ `requirements.txt` with all dependencies
- ✅ `.streamlit/config.toml` for app configuration
- ✅ `.gitignore` to exclude unnecessary files
- ✅ `app.py` as the main entry point

#### 2. **Sign Up for Streamlit Community Cloud**
1. Go to https://share.streamlit.io/
2. Click "Sign up" or "Continue with GitHub"
3. Authorize Streamlit to access your GitHub account

#### 3. **Deploy Your App**
1. Click "New app" button
2. Select your repository: `shrimankar16/Mission-2027-Tracker`
3. Choose branch: `main`
4. Main file path: `app.py`
5. Click "Deploy!"

#### 4. **Wait for Deployment**
- Initial deployment takes 2-5 minutes
- Streamlit will install all requirements automatically
- You'll get a public URL like: `https://mission-2027-tracker.streamlit.app`

#### 5. **Access Your App**
- Your app will be live at the provided URL
- Share this URL with anyone to access your tracker
- The app will auto-update when you push to GitHub

---

## 🔧 Configuration

### Environment Variables (if needed)
If you need to set environment variables:
1. Go to your app settings in Streamlit Cloud
2. Click "⋮" menu → "Settings"
3. Go to "Secrets" tab
4. Add secrets in TOML format

### Database Persistence
⚠️ **Important**: Streamlit Community Cloud apps restart periodically, which means:
- SQLite database changes may be lost on restart
- For production use, consider using a cloud database (PostgreSQL, MySQL, etc.)
- Or use Streamlit's built-in secrets management for persistent data

---

## 🌐 Alternative Deployment Options

### Option 2: Deploy to Render
1. Sign up at https://render.com
2. Create new "Web Service"
3. Connect your GitHub repository
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

### Option 3: Deploy to Railway
1. Sign up at https://railway.app
2. Create new project from GitHub repo
3. Railway will auto-detect Streamlit
4. Deploy automatically

### Option 4: Deploy to Heroku
1. Create `Procfile`:
   ```
   web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```
2. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = $PORT
   enableCORS = false
   " > ~/.streamlit/config.toml
   ```
3. Deploy via Heroku CLI or GitHub integration

---

## 📝 Post-Deployment Checklist

- [ ] App loads without errors
- [ ] Database initializes correctly
- [ ] All pages are accessible
- [ ] Authentication works (if enabled)
- [ ] Export features work
- [ ] Analytics display correctly
- [ ] Mobile responsiveness checked

---

## 🔄 Updating Your Deployed App

To update your live app:
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

Streamlit Cloud will automatically detect the changes and redeploy your app within 1-2 minutes.

---

## 🆘 Troubleshooting

### App won't start
- Check the build logs in Streamlit Cloud dashboard
- Verify all dependencies in `requirements.txt` are correct
- Ensure `app.py` is in the root directory

### Database errors
- SQLite may have limitations on Streamlit Cloud
- Consider using cloud database for production

### Performance issues
- Streamlit Community Cloud has resource limits
- Consider upgrading to Streamlit Cloud Pro if needed
- Optimize database queries and data loading

---

## 📞 Support

- Streamlit Docs: https://docs.streamlit.io/
- Streamlit Forum: https://discuss.streamlit.io/
- Repository Issues: https://github.com/shrimankar16/Mission-2027-Tracker/issues

---

**Your app repository**: https://github.com/shrimankar16/Mission-2027-Tracker

**Deployment Status**: Ready to deploy! ✅
