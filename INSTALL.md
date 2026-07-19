# SocksQuads CRM - Installation & Setup Guide

Complete step-by-step instructions for setting up and running the SocksQuads CRM Dashboard.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Local Installation](#local-installation)
3. [Google Sheets Setup](#google-sheets-setup)
4. [Running the Application](#running-the-application)
5. [Cloud Deployment](#cloud-deployment)
6. [Post-Installation](#post-installation)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 7+, macOS 10.12+, or Linux
- **Python**: 3.7 or higher
- **RAM**: 2 GB
- **Disk Space**: 500 MB
- **Internet**: Required (for Google Sheets and Streamlit Cloud)

### Recommended Setup
- **OS**: Windows 10+, macOS 11+, or Ubuntu 20.04+
- **Python**: 3.9 or higher
- **RAM**: 4 GB
- **Internet Speed**: 5+ Mbps

### Required Accounts
- Google Account (free)
- GitHub Account (free)
- Streamlit Community Account (free)

---

## Local Installation

### Step 1: Download Python

1. Visit [python.org](https://www.python.org/downloads/)
2. Download Python 3.9 or higher
3. **Windows Users**: During installation, check "Add Python to PATH"
4. **Mac/Linux Users**: Usually pre-installed
5. Verify installation:
   ```bash
   python --version
   # Should show Python 3.9.x or higher
   ```

### Step 2: Clone or Download the Project

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/yourusername/SocksquadsCRM.git
cd SocksquadsCRM
```

**Option B: Download as ZIP**
1. Go to GitHub repository
2. Click "Code" > "Download ZIP"
3. Extract the ZIP file
4. Open command prompt in the extracted folder

### Step 3: Create Virtual Environment

Virtual environment keeps dependencies isolated and clean.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your command line.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- streamlit (web framework)
- pandas (data processing)
- plotly (charts)
- gspread (Google Sheets API)
- google-auth (authentication)
- python-dateutil (date handling)

**If installation fails:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Try again
pip install -r requirements.txt
```

### Step 5: Verify Installation

```bash
# Check if Streamlit is installed
streamlit --version

# Check installed packages
pip list
```

---

## Google Sheets Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. At the top, click on the project dropdown
4. Click "NEW PROJECT"
5. Fill in:
   - Project name: `SocksQuads CRM Dashboard`
   - Click "CREATE"
6. Wait 1-2 minutes for project to be created

### Step 2: Enable APIs

**Enable Google Sheets API:**
1. Click "APIs & Services" from left menu
2. Click "Library"
3. Search for "Google Sheets API"
4. Click on it
5. Click "ENABLE" button
6. Wait for it to complete

**Enable Google Drive API:**
1. Click "Library" again
2. Search for "Google Drive API"
3. Click on it
4. Click "ENABLE"

### Step 3: Create Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "+ CREATE CREDENTIALS"
3. Select "Service Account"
4. Fill in the form:
   - Service account name: `socksquads-crm-app`
   - Service account ID: (auto-filled)
   - Description: (optional)
   - Click "CREATE AND CONTINUE"
5. On the "Grant this service account access to project" screen:
   - Click "CONTINUE"
6. On the "Grant users access to this service account" screen:
   - Click "CREATE KEY"
   - Select "JSON"
   - Click "CREATE"
7. A JSON file downloads automatically

### Step 4: Save Credentials

1. Rename the downloaded file to: `credentials.json`
2. Move it to your SocksquadsCRM project root folder (same level as `app.py`)
3. **IMPORTANT**: This file is in `.gitignore`, never commit it!

### Step 5: Create Google Sheet

1. Go to [Google Drive](https://drive.google.com/)
2. Click "+ New" > "Google Sheets" > "Blank spreadsheet"
3. Name it: `SocksQuads CRM` (exactly this name)
4. In your `credentials.json` file, find the line:
   ```
   "client_email": "socksquads-crm-app@PROJECT_ID.iam.gserviceaccount.com"
   ```
5. Copy that email address
6. In the Google Sheet, click "Share"
7. Paste the email address
8. In the permissions dropdown, select "Editor"
9. Uncheck "Notify people"
10. Click "Share"

---

## Running the Application

### Local Testing

1. Activate virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. Make sure you're in the project directory: `SocksquadsCRM`

3. Run the app:
   ```bash
   streamlit run app.py
   ```

4. Your browser will open automatically to: `http://localhost:8501`

5. If browser doesn't open, manually go to that URL

### First-Time Login

1. You should see the login page
2. Use demo credentials:
   - **Username**: `admin`
   - **Password**: `admin123`
3. Click "🔓 Login"
4. If successful, you'll see the Dashboard

### Testing Features

**As Admin:**
- View Dashboard (will be empty initially)
- Go to "Daily Reports" and submit a test report
- Check Dashboard again to see the data

**As Salesman:**
- Log out (click "🔓 Logout" in sidebar)
- Log in with:
  - **Username**: `raj`
  - **Password**: `raj123`
- Submit a daily report
- View your personal performance

---

## Cloud Deployment

### Step 1: Prepare for GitHub

1. Make sure all files are ready locally
2. Make sure `credentials.json` is in `.gitignore` (it is by default)
3. Test everything locally first

### Step 2: Create GitHub Repository

1. Go to [GitHub](https://github.com/)
2. Click "+" icon > "New repository"
3. Name: `SocksquadsCRM`
4. Description: `Sales CRM Dashboard for SocksQuads`
5. Make it **PUBLIC** (required for free Streamlit deployments)
6. Click "Create repository"

### Step 3: Push Code to GitHub

In your project directory:

```bash
# Initialize git (if first time)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: SocksQuads CRM Dashboard"

# Set main branch
git branch -M main

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/SocksquadsCRM.git

# Push
git push -u origin main
```

**Need GitHub help?**
- Make sure you have Git installed: [git-scm.com](https://git-scm.com/)
- Follow the on-screen instructions

### Step 4: Deploy to Streamlit Cloud

1. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
2. Click "Sign in with GitHub"
3. Authorize Streamlit
4. Click "New app" button
5. Fill in the form:
   - Repository: `YOUR_USERNAME/SocksquadsCRM`
   - Branch: `main`
   - Main file path: `app.py`
6. Click "Deploy"
7. Wait 2-3 minutes for deployment

### Step 5: Set Up Secrets (Important!)

1. Go to your deployed app on Streamlit Cloud
2. Click menu (•••) in top right
3. Click "Settings"
4. Click "Secrets" in left panel
5. Open your local `credentials.json` file in a text editor
6. Copy all the contents
7. Paste into the Secrets box
8. Click "Save"
9. App will automatically reboot

### Step 6: Test Cloud Deployment

1. Refresh the Streamlit Cloud page
2. Try logging in
3. Try submitting a report
4. Check that data appears in Google Sheets

**Your app is now live!** 🎉

Share the URL with your team members.

---

## Post-Installation

### Change Demo Passwords

**IMPORTANT: Do this before giving access to your team!**

1. Open `utils/helpers.py`
2. Find the `CREDENTIALS` section
3. Change all passwords to strong ones:
   ```python
   CREDENTIALS = {
       'admin': {
           'password': 'YOUR_NEW_STRONG_PASSWORD',  # Change this!
           'role': 'admin',
           'name': 'Administrator'
       },
       # ... other users
   }
   ```
4. Save the file
5. Commit to GitHub:
   ```bash
   git add utils/helpers.py
   git commit -m "Update passwords for production"
   git push
   ```
6. Streamlit Cloud will auto-deploy

### Add New Users

To add a new salesman, edit `utils/helpers.py`:

```python
'new_username': {
    'password': 'secure_password',
    'role': 'salesman',
    'name': 'John Doe'
}
```

Save and commit:
```bash
git add utils/helpers.py
git commit -m "Add new salesman: John Doe"
git push
```

### Customize App Settings

Edit `config.py` to customize:
- App name
- Report types
- Collection rate threshold
- Inactive retailer days
- Currency settings

Edit `.streamlit/config.toml` to customize:
- Theme colors
- Server settings
- Logging level

---

## Troubleshooting

### Issue: "Python not found"

**Solution:**
- Make sure Python is in PATH
- Windows: Uninstall and reinstall Python, checking "Add Python to PATH"
- Verify: Open new terminal and type `python --version`

### Issue: "pip command not found"

**Solution:**
```bash
# Windows
python -m pip install --upgrade pip

# macOS/Linux
python3 -m pip install --upgrade pip
```

### Issue: Virtual environment not activating

**Solution:**
- Windows: Try `venv\Scripts\activate.bat`
- Make sure you're in the project directory
- Check file path has no spaces

### Issue: "Module not found"

**Solution:**
- Make sure virtual environment is activated (you see `(venv)` prefix)
- Reinstall: `pip install -r requirements.txt`

### Issue: Streamlit won't start

**Solution:**
```bash
# Kill any existing Streamlit processes
# Then try again
streamlit run app.py

# If still failing, try
streamlit run app.py --logger.level=debug
```

### Issue: "Credentials file not found"

**Solution:**
- Make sure `credentials.json` is in project root (same directory as `app.py`)
- Check file name is exactly `credentials.json` (lowercase)
- If you don't have it yet, follow Google Sheets Setup section

### Issue: "Sheet not found" error

**Solution:**
1. Verify sheet is named exactly "SocksQuads CRM"
2. Verify sheet is shared with service account email
3. Check Google Drive > the sheet should be there
4. Restart Streamlit app

### Issue: Deployment to Streamlit Cloud failing

**Solution:**
1. Check repository is PUBLIC
2. Check `requirements.txt` exists
3. Check `app.py` is in root directory
4. Try redeploying
5. Check logs for specific error messages

### Issue: Slow performance

**Solution:**
- Free Streamlit tier sleeps after 15 minutes - first load will be slow
- Consider upgrading to Pro tier
- Restrict date ranges in reports to limit data

---

## Verification Checklist

- [ ] Python installed (verify with `python --version`)
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Google Cloud project created
- [ ] Google Sheets API enabled
- [ ] Google Drive API enabled
- [ ] Service account created with JSON key
- [ ] `credentials.json` saved in project root
- [ ] Google Sheet created and shared with service account
- [ ] Local app runs (`streamlit run app.py`)
- [ ] Can log in with demo credentials
- [ ] can submit a test report
- [ ] Data appears in Google Sheet
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] App deployed to Streamlit Cloud
- [ ] Secrets configured in Streamlit Cloud
- [ ] Cloud deployment works
- [ ] All passwords changed
- [ ] Users added as needed

---

## Next Steps

1. ✅ Complete installation
2. ✅ Add your sales team members
3. ✅ Add retailers to the database
4. ✅ Train team on usage
5. ✅ Start submitting daily reports
6. ✅ Review dashboard daily
7. ✅ Export reports weekly

---

## Getting Help

- **Installation Issues**: See Troubleshooting section above
- **Usage Questions**: See README.md and FEATURES.md
- **Deployment Issues**: See DEPLOYMENT.md
- **Quick Start**: See QUICKSTART.md

---

## Support Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [Google Cloud Docs](https://cloud.google.com/docs)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Python Docs](https://www.python.org/doc/)
- [GitHub Help](https://docs.github.com)
- [Streamlit Community Forum](https://discuss.streamlit.io)

---

**Installation Complete!** 🎉

Your SocksQuads CRM is ready to use. Share the access with your team and start tracking sales today!
