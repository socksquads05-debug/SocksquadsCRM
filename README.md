# SocksQuads CRM - Sales Dashboard

A complete, production-ready Sales CRM Dashboard for managing daily sales reports, retailer database, and business analytics. Built with Python, Streamlit, and Google Sheets.

## Features

- **📊 Executive Dashboard**: Real-time sales metrics, charts, and analytics
- **💼 Daily Sales Reports**: Easy submission of sales data with mobile-friendly interface
- **🏪 Retailer Database**: Complete CRM for managing retailer information
- **📈 Advanced Analytics**: Performance analysis, trends, and business insights
- **📋 Multiple Reports**: Daily, weekly, monthly, and custom reports with CSV export
- **🔐 Role-Based Access**: Admin and Salesman roles with different permissions
- **📱 Mobile Friendly**: Responsive design works on all devices
- **☁️ Cloud Ready**: Deploy to Streamlit Community Cloud for free

## Technology Stack

- **Backend**: Python 3
- **Frontend**: Streamlit
- **Database**: Google Sheets
- **Visualization**: Plotly
- **Deployment**: Streamlit Community Cloud
- **Version Control**: GitHub

## Project Structure

```
SocksquadsCRM/
├── app.py                    # Main application file with login
├── pages/                    # Page modules
│   ├── dashboard.py         # Main dashboard
│   ├── salesman.py          # Daily sales reporting
│   ├── retailers.py         # Retailer management
│   ├── reports.py           # Report generation
│   └── analytics.py         # Advanced analytics
├── utils/                   # Utility modules
│   ├── google_sheets.py    # Google Sheets integration
│   ├── helpers.py          # Helper functions and authentication
│   └── charts.py           # Plotting and visualization functions
├── .streamlit/             # Streamlit configuration
│   └── config.toml         # Theme and settings
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore            # Git ignore file
```

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SocksquadsCRM.git
cd SocksquadsCRM
```

2. Create a virtual environment:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Google Sheets integration (see below)

5. Run the application:
```bash
streamlit run app.py
```

6. Open in browser: `http://localhost:8501`

## Google Sheets Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Create Project"
3. Enter "SocksQuads CRM" as project name
4. Wait for project creation

### Step 2: Enable APIs

1. In Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google Sheets API" and click "Enable"
3. Search for "Google Drive API" and click "Enable"

### Step 3: Create Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Enter:
   - Service Account Name: "socksquads-crm"
   - Service Account ID: (auto-fill)
   - Click "Create and Continue"
4. Grant Basic Editor Role and click "Continue"
5. Click "Create Key" > "JSON"
6. Download the JSON file and save it as `credentials.json` in the project root

### Step 4: Create Google Sheet

1. Go to [Google Drive](https://drive.google.com/)
2. Create a new Google Sheet
3. Name it: "SocksQuads CRM"
4. Share it with the service account email (found in credentials.json) with "Editor" access

### Step 5: Add Sample Data (Optional)

The app automatically creates worksheet tabs when you first use each feature:
- **Sales Reports**: Created when first report is submitted
- **Retailers**: Created when first retailer is added

## Demo Credentials

Use these credentials to test the application:

### Admin Users
- Username: `admin` | Password: `admin123`
- Username: `owner` | Password: `owner123`

### Salesmen
- Username: `raj` | Password: `raj123`
- Username: `priya` | Password: `priya123`
- Username: `amit` | Password: `amit123`

## Updating Credentials

To add or modify users, edit `utils/helpers.py`:

```python
CREDENTIALS = {
    'new_user': {
        'password': 'password123',
        'role': 'salesman',  # or 'admin'
        'name': 'User Name'
    }
}
```

## Deployment to Streamlit Community Cloud

### Step 1: Prepare GitHub Repository

1. Create a GitHub account if you don't have one
2. Create a new repository: `SocksquadsCRM`
3. Initialize git in your project:
```bash
git init
git add .
git commit -m "Initial commit: SocksQuads CRM"
git branch -M main
git remote add origin https://github.com/yourusername/SocksquadsCRM.git
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - Repository: `yourusername/SocksquadsCRM`
   - Branch: `main`
   - Main file path: `app.py`
5. Click "Deploy"

### Step 3: Add Secrets

1. In Streamlit Cloud dashboard, click on your app
2. Click menu (...) > "Settings"
3. Go to "Secrets"
4. Copy the entire contents of your `credentials.json` file
5. Paste it in the secrets box with key: `google_credentials`

**Alternatively**, create `.streamlit/secrets.toml`:

```toml
[google_credentials]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "your-private-key"
client_email = "your-client-email"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

(Never commit credentials.json or secrets.toml to GitHub!)

### Step 4: Access Your App

Your app will be available at: `https://share.streamlit.io/yourusername/SocksquadsCRM`

## Features Overview

### Dashboard (Admin Only)
- **Key Metrics**: Today's sales, collections, outstanding, order count
- **Sales Trends**: Daily and monthly sales charts
- **Top Performers**: Top salesmen and retailers
- **Area Analysis**: Sales distribution by area
- **Collection Status**: Collection rate and outstanding amount
- **Detailed Tables**: Breakdown by salesman, area, and retailer

### Daily Sales Report (Salesman & Admin)
- Submit daily sales with:
  - Date
  - Retailer Name & Mobile
  - Area & City
  - Order Quantity & Value
  - Collection & Outstanding
  - Next Visit Date
  - Remarks
- View personal performance metrics
- Download reports as CSV

### Retailer Management (Admin Only)
- Search retailers by: Name, Mobile, Area, or City
- View detailed retailer information
- Add new retailers with complete details
- Track: Lifetime sales, outstanding, last visit, preferred products
- Analytics: Distribution by area, top outstanding retailers

### Reports (Admin Only)
- **Daily Reports**: Sales for specific date
- **Weekly Reports**: 7-day analysis
- **Monthly Reports**: Full month breakdown
- **Salesman Reports**: Individual performance
- **Area Reports**: Area-wise analysis
- **Collection Reports**: Payment tracking
- **Custom Reports**: Any date range
- Export all reports as CSV

### Analytics (Admin Only)
- **Key Insights**: Sales trends and growth metrics
- **Retailer Analysis**:
  - Top 10 retailers
  - Bottom 10 retailers
  - Inactive retailers (30+ days)
  - High outstanding amounts
  - New retailers
- **Sales Team Performance**: Individual and team statistics
- **Alerts & Warnings**:
  - Low collection rates
  - High outstanding
  - Inactive retailers
  - Current day status

## Data Structure

### Sales Reports Table
| Column | Type | Required |
|--------|------|----------|
| Date | Date | Yes |
| Salesman | Text | Yes |
| Retailer | Text | Yes |
| Retailer Mobile | Number | Yes |
| Area | Text | Yes |
| City | Text | Yes |
| Order Qty | Number | No |
| Order Value | Currency | No |
| Collection | Currency | No |
| Outstanding | Currency | No |
| Next Visit | Date | No |
| Remarks | Text | No |
| Timestamp | DateTime | Auto |

### Retailers Table
| Column | Type | Required |
|--------|------|----------|
| Name | Text | Yes |
| Owner | Text | Yes |
| Mobile | Number | Yes |
| Address | Text | Yes |
| GST | Text | No |
| Area | Text | Yes |
| City | Text | Yes |
| Last Visit | Date | Auto |
| Last Order | Date | No |
| Lifetime Sales | Currency | Auto |
| Outstanding | Currency | Auto |
| Preferred Product | Text | No |
| Notes | Text | No |
| Created Date | DateTime | Auto |

## Configuration

### Changing Theme Colors

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#0066cc"      # Blue accent
backgroundColor = "#ffffff"   # White background
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### Changing Login Credentials

Edit `utils/helpers.py` and modify the `CREDENTIALS` dictionary:

```python
AuthenticationManager.CREDENTIALS = {
    'username': {
        'password': 'secure_password',
        'role': 'admin',  # or 'salesman'
        'name': 'Display Name'
    }
}
```

## Troubleshooting

### Issue: "Credentials file not found"
**Solution**: Make sure `credentials.json` is in the project root directory.

### Issue: "Sheet not found"
**Solution**: 
1. Create a Google Sheet named "SocksQuads CRM"
2. Share it with the service account email
3. Restart the app

### Issue: Streamlit Cloud shows 403 error
**Solution**: Add secrets as described in the Deployment section.

### Issue: Data not persisting
**Solution**: 
1. Verify Google Sheets credentials are correct
2. Check that the sheet is shared with service account
3. Verify internet connection

## Performance Tips

- **For large datasets**: Filter data by date range
- **Mobile optimization**: Use mobile-friendly browsers (Chrome, Safari)
- **Google Sheets limits**: 
  - Max 10 million cells per sheet
  - For large datasets, consider archiving old data
  - Create separate sheets for historical data

## Security Considerations

1. **Credentials**:
   - Never commit `credentials.json` to GitHub
   - Always use `.gitignore`
   - Use Streamlit Secrets for cloud deployment

2. **Google Sheets**:
   - Share only with service account email
   - Do not make sheets publicly accessible
   - Use strong Google account passwords

3. **User Passwords**:
   - Change demo passwords in production
   - Use strong passwords (12+ characters)
   - Consider integrating with enterprise authentication

## Maintenance & Updates

### Regular Tasks
- Review inactive retailers weekly
- Archive old data monthly
- Backup Google Sheet monthly
- Monitor outstanding amounts

### Updating the Application

1. Make changes locally and test
2. Commit to GitHub:
```bash
git add .
git commit -m "Description of changes"
git push
```

3. Streamlit Cloud will auto-deploy from main branch

## Backup Strategy

1. **Google Sheets**: Automatically backed up by Google
2. **Code Backup**: Committed to GitHub
3. **Manual Backup**: Export data as CSV monthly

## Support & Documentation

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Plotly Documentation](https://plotly.com/python/)

## License

MIT License - Feel free to modify and use for your business.

## Author

Built for SocksQuads Sales Team

---

**Version**: 1.0
**Last Updated**: July 2026
**Status**: Production Ready ✅
