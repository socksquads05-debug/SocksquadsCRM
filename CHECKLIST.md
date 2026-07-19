# 🚀 SocksQuads CRM - Getting Started Checklist

Quick reference checklist for implementing SocksQuads CRM. Print this out or use as you go!

---

## ✅ PRE-INSTALLATION (5 minutes)

- [ ] Downloaded Python 3.7+ from python.org
- [ ] Have git installed (optional but recommended)
- [ ] Have Google account
- [ ] Have GitHub account (for cloud deployment)
- [ ] Have internet connection
- [ ] Downloaded/cloned the SocksquadsCRM project

---

## ✅ LOCAL INSTALLATION (10 minutes)

### Step 1: Setup Environment
- [ ] Unzip/download project files
- [ ] Open terminal/command prompt in project folder
- [ ] Verify Python: `python --version` (should be 3.7+)

### Step 2: Create Virtual Environment
- [ ] **Windows**: `python -m venv venv`
- [ ] **Mac/Linux**: `python3 -m venv venv`
- [ ] **Windows**: `venv\Scripts\activate` (activate it)
- [ ] **Mac/Linux**: `source venv/bin/activate` (activate it)
- [ ] See `(venv)` in your command line prompt

### Step 3: Install Dependencies
- [ ] Run: `pip install -r requirements.txt`
- [ ] Wait for installation to complete
- [ ] Verify: `streamlit --version`

### Step 4: Create Google Credentials
- [ ] Go to Google Cloud Console
- [ ] Create new project named "SocksQuads CRM Dashboard"
- [ ] Enable Google Sheets API
- [ ] Enable Google Drive API
- [ ] Create Service Account
- [ ] Download JSON credentials
- [ ] Rename to `credentials.json`
- [ ] Place in project root folder (same level as app.py)

### Step 5: Create Google Sheet
- [ ] Go to Google Drive
- [ ] Create new Google Sheet
- [ ] Name it: `SocksQuads CRM` (exactly)
- [ ] Find client_email in credentials.json
- [ ] Share sheet with that email (Editor access)

---

## ✅ TEST LOCAL SETUP (5 minutes)

### Step 1: Run Application
- [ ] Make sure you're in project directory
- [ ] Make sure virtual environment is activated: `(venv)` visible
- [ ] Run: `streamlit run app.py`
- [ ] Wait for browser to open (localhost:8501)

### Step 2: Test Login
- [ ] You see login page
- [ ] Username: `admin`
- [ ] Password: `admin123`
- [ ] Click "🔓 Login"
- [ ] You see the Dashboard

### Step 3: Test Data Entry
- [ ] Click "Daily Reports" in sidebar
- [ ] Click "Submit Report" tab
- [ ] Fill in test data
- [ ] Click "✅ Submit Report"
- [ ] You get success message

### Step 4: Verify Data Saved
- [ ] Go to Google Drive
- [ ] Open "SocksQuads CRM" sheet
- [ ] Check "Sales Reports" tab
- [ ] See your test data there
- [ ] ✅ Everything working!

---

## ✅ OPTIONAL: ADD SAMPLE DATA (5 minutes)

- [ ] Terminal: `python sample_data.py`
- [ ] See CSV files created in `data/` folder
- [ ] Go to Google Sheet
- [ ] Create "Sales Reports" worksheet tab
- [ ] Create "Retailers" worksheet tab
- [ ] Copy-paste CSV data into these sheets
- [ ] Go back to app
- [ ] Dashboard now has data!

---

## ✅ GITHUB SETUP (10 minutes) - For Cloud Deployment

### Step 1: Create GitHub Repo
- [ ] Go to GitHub.com
- [ ] Click "+" > "New repository"
- [ ] Name: `SocksquadsCRM`
- [ ] Description: `Sales CRM Dashboard for SocksQuads`
- [ ] Set to **PUBLIC**
- [ ] Click "Create repository"

### Step 2: Push Code to GitHub
- [ ] Terminal in project folder
- [ ] `git init`
- [ ] `git add .`
- [ ] `git commit -m "Initial commit: SocksQuads CRM"`
- [ ] `git branch -M main`
- [ ] `git remote add origin https://github.com/USERNAME/SocksquadsCRM.git`
- [ ] `git push -u origin main`
- [ ] Go to GitHub and verify files are there
- [ ] Check that `credentials.json` is NOT visible

---

## ✅ STREAMLIT CLOUD DEPLOYMENT (10 minutes)

### Step 1: Deploy
- [ ] Go to streamlit.io/cloud
- [ ] Sign in with GitHub
- [ ] Click "New app"
- [ ] Select your SocksquadsCRM repository
- [ ] Select branch: `main`
- [ ] Set main file: `app.py`
- [ ] Click "Deploy"
- [ ] Wait 2-3 minutes

### Step 2: Add Secrets
- [ ] Click on your deployed app
- [ ] Click menu (•••) > Settings
- [ ] Click "Secrets"
- [ ] Open local `credentials.json` in text editor
- [ ] Copy all contents
- [ ] Paste in Secrets box
- [ ] Click "Save"
- [ ] App reboots automatically

### Step 3: Test Cloud App
- [ ] Refresh page
- [ ] Try logging in with `admin` / `admin123`
- [ ] Submit a test report
- [ ] Check it appears in Google Sheets
- [ ] ✅ Cloud deployment working!

---

## ✅ PRODUCTION SETUP (15 minutes)

### Step 1: Change Passwords
- [ ] Edit `utils/helpers.py`
- [ ] Change all demo passwords to strong ones
- [ ] Save file
- [ ] `git add utils/helpers.py`
- [ ] `git commit -m "Update production passwords"`
- [ ] `git push`
- [ ] Streamlit Cloud auto-redeploys

### Step 2: Customize Settings
- [ ] Edit `config.py` (app name, currency, etc.)
- [ ] Edit `.streamlit/config.toml` (colors, theme)
- [ ] Commit and push changes

### Step 3: Add Your Users
- [ ] Edit `utils/helpers.py`
- [ ] Add your salesmen in CREDENTIALS section:
   ```python
   'john_username': {
       'password': 'strong_password',
       'role': 'salesman',
       'name': 'John Doe'
   }
   ```
- [ ] Save, commit, and push
- [ ] Users can now log in with new credentials

### Step 4: Train Your Team
- [ ] Share Streamlit Cloud URL with team
- [ ] Give them their username/password
- [ ] Show them how to submit reports
- [ ] Show admin how to view dashboard

---

## ✅ ONGOING MAINTENANCE

### Daily
- [ ] Check dashboard for new reports
- [ ] Review sales figures
- [ ] Note any alerts

### Weekly
- [ ] Generate weekly report
- [ ] Review performance
- [ ] Check inactive retailers
- [ ] Plan next week's activities

### Monthly
- [ ] Archive old data (optional)
- [ ] Verify all reports correct
- [ ] Review Google Sheet backup
- [ ] Update any settings if needed

### Quarterly
- [ ] Review app performance
- [ ] Collect team feedback
- [ ] Plan any improvements
- [ ] Update passwords

---

## 🆘 TROUBLESHOOTING QUICK REFERENCE

| Problem | Solution |
|---------|----------|
| **Python not found** | Install Python 3.7+, add to PATH |
| **Module not found** | Activate venv: `venv\Scripts\activate` then install: `pip install -r requirements.txt` |
| **Credentials file not found** | Save Google credentials as `credentials.json` in project root |
| **Can't log in** | Username & password are case-sensitive, try: `admin` / `admin123` |
| **Google Sheet issue** | Verify sheet name is exactly "SocksQuads CRM" and shared with service account |
| **App won't start** | Activate virtual environment first |
| **Cloud deployment error** | Make repo PUBLIC and check requirements.txt exists |
| **Slow performance** | Free tier sleeps after 15 min; upgrade to Pro if needed |

---

## 📞 HELP RESOURCES

**Quick Questions?**
- Check README.md for complete documentation
- Check FEATURES.md for feature details
- Check DEPLOYMENT.md for cloud issues

**Technical Help?**
- [Streamlit Docs](https://docs.streamlit.io)
- [Google Sheets API Help](https://developers.google.com/sheets/api)
- [GitHub Help](https://docs.github.com)

**Community Support?**
- [Streamlit Community Forum](https://discuss.streamlit.io)
- [Stack Overflow](https://stackoverflow.com)

---

## 🎯 SUCCESS INDICATORS

### ✅ You're Ready if:
- App runs locally without errors
- You can log in with demo credentials
- You can submit a sales report
- Data appears in Google Sheets
- Dashboard shows your test data

### ✅ Cloud Deployment Successful if:
- Cloud app loads in browser
- You can log in to cloud app
- You can submit report from cloud
- No errors in Streamlit logs

### ✅ Production Ready if:
- All passwords changed
- All users added
- Users can log in and submit reports
- Admin can view dashboard and reports
- Data syncs to Google Sheets

---

## 📋 FINAL CHECKLIST

At this point, your SocksQuads CRM is ready to use!

- [ ] App running locally ✅
- [ ] App deployed to cloud ✅
- [ ] Team has access ✅
- [ ] First reports submitted ✅
- [ ] Dashboard showing data ✅
- [ ] All passwords changed ✅
- [ ] Users trained ✅

**Congratulations! Your SocksQuads CRM is live!** 🎉

---

## 🚀 Now What?

1. **Start using it**: Submit daily reports through the app
2. **Monitor data**: Review dashboard metrics
3. **Generate reports**: Create weekly/monthly reports
4. **Make decisions**: Use data to improve sales
5. **Iterate**: Add features as needed

---

## 📞 Need Help?

Start here based on your issue:

- **Installation issues** → Read INSTALL.md
- **Deployment issues** → Read DEPLOYMENT.md
- **Feature questions** → Read FEATURES.md or README.md
- **General questions** → Read PROJECT_SUMMARY.md

---

**Version**: 1.0
**Last Updated**: July 2026
**Status**: Ready to Use ✅

Print this page and check items off as you complete them!
