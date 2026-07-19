# SocksQuads CRM - Quick Start Guide

Get up and running in 15 minutes! 🚀

## Prerequisites Check

- [ ] Python 3.7+ installed
- [ ] pip package manager
- [ ] Google account
- [ ] GitHub account (for cloud deployment)
- [ ] Internet connection

---

## 5-Minute Local Setup

### Step 1: Install Python Dependencies (2 min)

```bash
# On Windows
pip install -r requirements.txt

# On macOS/Linux
pip3 install -r requirements.txt
```

### Step 2: Get Google Credentials (2 min)

For **local testing only** (skip if doing cloud deployment):

1. Download a test Google Sheet credentials file
   - For now, just create a dummy `credentials.json` file with:
   ```json
   {
     "type": "service_account",
     "project_id": "test-project"
   }
   ```
   - This allows the app to start without errors

2. The app will prompt you to create a real one later

### Step 3: Run the App (1 min)

```bash
streamlit run app.py
```

Your app opens at: `http://localhost:8501`

### Step 4: Login (1 min)

Use demo credentials:
- **Username:** `admin`
- **Password:** `admin123`

---

## 15-Minute Cloud Deployment

### Step 1: Complete Local Setup (5 min)
Follow the 5-minute setup above

### Step 2: Get Real Google Credentials (5 min)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project > name it "SocksQuads CRM"
3. Go to APIs > Library
   - Enable "Google Sheets API"
   - Enable "Google Drive API"
4. Go to Credentials > +Create > Service Account
5. Download JSON key and save as `credentials.json` in project root
6. Create Google Sheet "SocksQuads CRM" and share with service account email

### Step 3: Deploy to GitHub (3 min)

```bash
git init
git add .
git commit -m "Initial SocksQuads CRM"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/SocksquadsCRM.git
git push -u origin main
```

### Step 4: Deploy to Streamlit Cloud (2 min)

1. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
2. "New app" > Select your repo > `app.py`
3. In Settings > Secrets, paste your `credentials.json` content
4. Done! 🎉

Your app is live at: `https://share.streamlit.io/yourname/sockquadscrm`

---

## Database Setup

### Option A: Let App Create Tables (Easiest)

1. Just use the app normally
2. First time you:
   - Submit a sales report → "Sales Reports" sheet created
   - Add a retailer → "Retailers" sheet created
3. Done!

### Option B: Pre-populate with Sample Data

```bash
python sample_data.py
```

This creates CSV files in `data/` folder that you can manually paste into Google Sheets.

---

## User Management

### Add New Salesman

Edit `utils/helpers.py`:

```python
CREDENTIALS = {
    'new_username': {
        'password': 'strong_password_here',
        'role': 'salesman',
        'name': 'John Doe'
    }
}
```

Save and redeploy if on cloud.

### Change Admin Password

Edit `utils/helpers.py`:

```python
'admin': {
    'password': 'NEW_STRONG_PASSWORD',  # Change this!
    'role': 'admin',
    'name': 'Administrator'
}
```

---

## Common First Steps

1. **Log in as Admin**
   - Username: `admin`
   - Password: `admin123`

2. **Check Dashboard** (should show "No data" initially)

3. **Log in as Salesman** (choose one):
   - Username: `raj` | Password: `raj123`
   - Username: `priya` | Password: `priya123`
   - Username: `amit` | Password: `amit123`

4. **Submit a test report** in "Daily Sales Report" tab

5. **Log back as Admin** and check Dashboard
   - Your data should appear! 📊

---

## Troubleshooting Quick Fixes

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Credentials file not found"
- Create `credentials.json` in project root (even if dummy)
- For real setup, follow Google Sheets Setup guide

### "Sheet not found" error
1. Google Sheets API might not be enabled
2. Check sheet is shared with service account email
3. Try restarting the app

### App won't start
```bash
# Check Python version
python --version  # Should be 3.7+

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Login not working
- Check exact username (case-sensitive)
- Check password (case-sensitive, no spaces)
- Demo user: `admin` / `admin123`

---

## Next Steps

1. ✅ Set up Google Sheets integration
2. ✅ Change all demo passwords
3. ✅ Add your salesmen as users
4. ✅ Add retailers to the database
5. ✅ Train salesmen on submitting reports
6. ✅ Monitor dashboard regularly

---

## Free Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [Google Sheets API Guide](https://developers.google.com/sheets/api)
- [Plotly Charts](https://plotly.com/python/)
- [GitHub Help](https://docs.github.com)
- [Python Tutorial](https://www.python.org/doc/)

---

## File Organization

```
Project Root/
├── app.py                 ← Main file (run this!)
├── requirements.txt       ← Dependencies
├── credentials.json       ← Google auth (create this)
├── config.py             ← Settings
├── sample_data.py        ← Generate test data
├── QUICKSTART.md         ← This file
├── README.md             ← Detailed docs
├── DEPLOYMENT.md         ← Cloud deployment
├── FEATURES.md           ← Feature documentation
├── pages/                ← Page modules
├── utils/                ← Helper modules
└── .streamlit/           ← Streamlit config
```

---

## Essential Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run app locally
streamlit run app.py

# Generate sample data
python sample_data.py

# Push to GitHub
git add .
git commit -m "description"
git push

# Check Python version
python --version
```

---

## Key URLs

| Purpose | URL |
|---------|-----|
| Streamlit Community Cloud | https://streamlit.io/cloud |
| Google Cloud Console | https://console.cloud.google.com |
| Google Drive | https://drive.google.com |
| GitHub | https://github.com |
| Your Local App | http://localhost:8501 |

---

## Support Resources

- **Documentation**: See README.md and FEATURES.md
- **Deployment Help**: See DEPLOYMENT.md
- **Code Questions**: Check comments in Python files
- **Google API Help**: Google Cloud documentation
- **Streamlit Help**: Community forum at discuss.streamlit.io

---

**Time to Production: ~15 minutes** ⏱️

After setup, you'll have a fully functional Sales CRM running in the cloud! 🎉

For detailed information, see the main README.md file.
