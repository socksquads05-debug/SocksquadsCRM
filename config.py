"""
Configuration file for SocksQuads CRM.
Change settings here before deploying.
"""

# ==================== APPLICATION SETTINGS ====================
APP_NAME = "SocksQuads CRM"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Sales Dashboard for SocksQuads"

# ==================== GOOGLE SHEETS SETTINGS ====================
GOOGLE_SHEET_NAME = "SocksQuads CRM"
CREDENTIALS_FILE = "credentials.json"

# ==================== USER ROLES ====================
ROLES = {
    'admin': {
        'permissions': [
            'view_dashboard',
            'view_reports',
            'manage_retailers',
            'view_analytics',
            'export_data'
        ]
    },
    'salesman': {
        'permissions': [
            'submit_reports',
            'view_own_performance'
        ]
    }
}

# ==================== REPORT SETTINGS ====================
# Report types available
REPORT_TYPES = [
    'Daily Report',
    'Weekly Report',
    'Monthly Report',
    'Salesman Report',
    'Area Report',
    'Collection Report',
    'Custom Date Range'
]

# ==================== CHART SETTINGS ====================
CHART_COLORS = {
    'primary': '#0066cc',
    'secondary': '#00cc66',
    'accent': '#ff6600',
    'danger': '#ff0066'
}

# Top N settings for charts
TOP_PERFORMERS_COUNT = 5
TOP_RETAILERS_COUNT = 10
TOP_PRODUCTS_COUNT = 5

# ==================== ANALYTICS SETTINGS ====================
INACTIVE_RETAILER_DAYS = 30  # Retailers inactive for 30+ days
LOW_COLLECTION_RATE_THRESHOLD = 70  # Alert if collection rate < 70%

# ==================== CURRENCY SETTINGS ====================
CURRENCY_SYMBOL = "₹"
CURRENCY_CODE = "INR"

# ==================== DATE FORMATS ====================
DATE_FORMAT = "%d-%m-%Y"
DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"
