# SocksQuads CRM - Deployment Guide

Complete step-by-step instructions for deploying the CRM to Streamlit Community Cloud.

## Overview

This guide covers:
1. Setting up Google Cloud credentials
2. Creating a GitHub repository
3. Deploying to Streamlit Community Cloud
4. Configuring data access
5. Troubleshooting common issues

## Prerequisites

- Google account
- GitHub account
- Internet connection
- No credit card required (all services have free tiers)

---

## Part 1: Google Cloud Setup

### 1.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown at the top
3. Click "NEW PROJECT"
4. Name: `SocksQuads CRM Dashboard`
5. Leave Organization as "No organization"
6. Click "CREATE"
7. Wait 1-2 minutes for project creation

### 1.2 Enable Required APIs

1. In the Google Cloud Console, click "APIs & Services" in the left menu
2. Click "Library"

**Enable Google Sheets API:**
1. Search for "Google Sheets API"
2. Click on it
3. Click "ENABLE"
4. Wait for it to complete

**Enable Google Drive API:**
1. Go back to Library (click "Library" in left menu)
2. Search for "Google Drive API"
3. Click on it
4. Click "ENABLE"

### 1.3 Create Service Account

1. In Google Cloud Console, go to "APIs & Services" > "Credentials"
2. Click "+ CREATE CREDENTIALS" at the top
3. Select "Service Account"
4. Fill in:
   - Service account name: `socksquads-crm-app`
   - Service account ID: (auto-filled)
   - Click "CREATE AND CONTINUE"
5. Click "CONTINUE" on the "Grant this service account access" screen
6. Click "CREATE KEY"
7. Select "JSON"
8. Click "CREATE"
9. A JSON file will download automatically - **SAVE THIS CAREFULLY**

### 1.4 Save Credentials Locally

1. Rename the downloaded file to `credentials.json`
2. Place it in the project root directory (same level as `app.py`)
3. **NEVER commit this file to GitHub** - it's already in `.gitignore`

---

## Part 2: Google Sheets Setup

### 2.1 Create and Share Google Sheet

1. Go to [Google Drive](https://drive.google.com/)
2. Right-click in empty area > "Google Sheets" > "Blank spreadsheet"
3. Name the sheet: `SocksQuads CRM`
4. Open the credentials.json file you downloaded and find the `client_email` value
   - It looks like: `socksquads-crm-app@projectname.iam.gserviceaccount.com`
5. Share the sheet with this email:
   - Click "Share" button (top right)
   - Paste the service account email
   - Change permission to "Editor"
   - Click "Share" (uncheck "Notify people")

### 2.2 Add Sample Data (Optional)

1. Run the sample data generator:
```bash
python sample_data.py
```

2. This creates CSV files in the `data/` folder
3. Manually create worksheets in your Google Sheet:
   - Right-click sheet tab > "Insert 1 sheet above"
   - Name: `Sales Reports`
   - Name: `Retailers`
4. Copy-paste the CSV data into these sheets

**OR** Let the app create them automatically:
1. Just submit your first sales report
2. Add your first retailer
3. The app will create the sheets automatically

---

## Part 3: GitHub Repository Setup

### 3.1 Create GitHub Repository

1. Go to [GitHub](https://github.com/)
2. Click the "+" icon (top right) > "New repository"
3. Settings:
   - Repository name: `SocksquadsCRM`
   - Description: `Sales CRM Dashboard for SocksQuads`
   - Visibility: **Public** (required for free Streamlit deployment)
   - **DO NOT** initialize with README (we have one)
   - Click "Create repository"

### 3.2 Push Code to GitHub

In your project directory, run these commands:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: SocksQuads CRM Sales Dashboard"

# Rename branch to main (if needed)
git branch -M main

# Add remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/SocksquadsCRM.git

# Push to GitHub
git push -u origin main
```

### 3.3 Verify on GitHub

1. Go to your repository on GitHub
2. You should see all project files
3. Make sure `credentials.json` is NOT visible (it's in .gitignore)

---

## Part 4: Streamlit Cloud Deployment

### 4.1 Deploy the App

1. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
2. Click "Sign in with GitHub" (if not already logged in)
3. Authorize Streamlit to access GitHub
4. Click "New app" (or "Create app" button)
5. Fill in:
   - Repository: `USERNAME/SocksquadsCRM`
   - Branch: `main`
   - Main file path: `app.py`
6. Click "Deploy"
7. Wait 2-3 minutes for deployment
8. You'll get a URL like: `https://share.streamlit.io/username/sockquadscrm`

### 4.2 Add Google Credentials as Secrets

**Important:** You need to add your credentials to Streamlit Secrets so the cloud app can access Google Sheets.

1. In Streamlit Cloud dashboard, click on your app ("SocksquadsCRM")
2. Click menu (⋮) in top right > "Settings"
3. Click "Secrets" panel on the left
4. Open your local `credentials.json` file with a text editor
5. Copy the **entire contents**
6. In the Secrets box, paste with this format:

```
[google_credentials]
type = "service_account"
project_id = "<paste from credentials.json>"
private_key_id = "<paste from credentials.json>"
private_key = "<paste from credentials.json>"
client_email = "<paste from credentials.json>"
client_id = "<paste from credentials.json>"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "<paste from credentials.json>"
```

**OR (Easier method):** Use TOML format:

1. Open `credentials.json` with text editor
2. Copy all content
3. In Secrets box, paste everything (Streamlit usually auto-formats it)
4. Click "Save"

### 4.3 Test Your Deployment

1. Go to your Streamlit app URL
2. Log in with demo credentials:
   - Username: `admin`
   - Password: `admin123`
3. If you see data, it's working! ✅
4. If not, check:
   - Google Sheet exists and is named "SocksQuads CRM"
   - Sheet is shared with service account email
   - Secrets are properly configured

---

## Part 5: Post-Deployment Configuration

### 5.1 Change Passwords

In `utils/helpers.py`, change all demo passwords:

```python
CREDENTIALS = {
    'admin': {
        'password': 'YOUR_SECURE_PASSWORD_HERE',
        'role': 'admin',
        'name': 'Administrator'
    },
    # ... etc
}
```

Commit and push:
```bash
git add utils/helpers.py
git commit -m "Update credentials for production"
git push
```

### 5.2 Customize Theme

Edit `.streamlit/config.toml` to match your brand colors

### 5.3 Add More Users

Edit `utils/helpers.py` to add more salesmen or admins

### 5.4 Configure Settings

Edit `config.py` to customize:
- Report types
- Analytics thresholds
- Currency settings
- Date formats

---

## Part 6: Updating the Application

### Making Changes

1. Make changes locally
2. Test with `streamlit run app.py`
3. Commit changes:
```bash
git add .
git commit -m "Description of changes"
git push
```

The Streamlit Cloud app will **automatically redeploy** within 1-2 minutes.

### Viewing Logs

1. In Streamlit Cloud, click on your app
2. Click "Manage app" > "Logs" tab
3. View real-time logs and errors

---

## Troubleshooting

### Issue: "Credentials file not found" or "Sheet not found"

**Solution:**
1. Check Streamlit Secrets are properly configured
2. Verify Google Sheet is named "SocksQuads CRM"
3. Verify sheet is shared with service account email
4. Click "Manage app" > "Reboot app"

### Issue: 403 Forbidden Error

**Solution:**
1. Google Sheet might not be shared correctly
2. Share permissions might be "View only" instead of "Edit"
3. Solution: Open sheet, click Share, change to "Editor"

### Issue: Slow Load Times

**Solution:**
1. Free Streamlit tier sleeps after 15 min of inactivity
2. Usually wakes up within 30 seconds
3. First load might be slow
4. Consider upgrading to paid tier if this is persistent

### Issue: Data Not Saving

**Solution:**
1. Check internet connection (on your device)
2. Verify Google Sheets API is enabled
3. Verify sheet has correct column headers
4. Check Google Sheet is shared and accessible

### Issue: Can't Log In

**Solution:**
1. Case-sensitive username and password
2. Check spelling exactly (no spaces before/after)
3. Default demo creds:
   - Username: `admin` (lowercase)
   - Password: `admin123`

### Issue: GitHub Push Fails

**Common error:** "fatal: not a git repository"

**Solution:**
```bash
# Initial setup
git init
git config user.name "Your Name"
git config user.email "your@email.com"
git add .
git commit -m "Initial commit"
```

---

## Maintenance Checklist

- [ ] Change all demo passwords
- [ ] Test login with new credentials
- [ ] Verify Google Sheet access
- [ ] Run sample report submission
- [ ] Test data appears in Google Sheet
- [ ] Check all pages load correctly
- [ ] Test on mobile device
- [ ] Backup important data monthly
- [ ] Monitor Streamlit logs regularly
- [ ] Update code and dependencies when needed

---

## Useful URLs

- **Streamlit Cloud Dashboard:** https://share.streamlit.io
- **Google Cloud Console:** https://console.cloud.google.com
- **Google Drive:** https://drive.google.com
- **GitHub:** https://github.com
- **Streamlit Docs:** https://docs.streamlit.io
- **Google Sheets API Docs:** https://developers.google.com/sheets/api

---

## Support

If you encounter issues:

1. Check the [Streamlit Community Forum](https://discuss.streamlit.io)
2. Check [Google Cloud documentation](https://cloud.google.com/docs)
3. Review error messages in Streamlit logs
4. Ensure all prerequisites are met

---

## Security Reminders

✅ **DO:**
- Keep `credentials.json` secure and local only
- Use `.gitignore` (already configured)
- Change demo passwords before production use
- Use strong passwords (12+ characters)
- Regularly review Google Drive sharing settings

❌ **DON'T:**
- Commit `credentials.json` to GitHub
- Share credentials via email
- Use simple passwords
- Make Google Sheet publicly accessible
- Leave demo accounts unchanged in production

---

**Deployment Complete!** 🎉

Your SocksQuads CRM Dashboard is now live and accessible at your Streamlit Cloud URL.

Share this URL with your sales team to start using it!
