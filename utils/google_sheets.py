"""
Google Sheets integration module for SocksQuads CRM.
Handles all interactions with Google Sheets for data persistence.
"""

import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st
from typing import List, Dict, Optional
import json
import os


class GoogleSheetsConnector:
    """Manages connections and operations with Google Sheets."""
    
    def __init__(self, credentials_path: str = "credentials.json", sheet_name: str = "SocksQuads CRM"):
        """
        Initialize Google Sheets connector.
        
        Args:
            credentials_path: Path to Google service account credentials JSON
            sheet_name: Name of the Google Sheet
        """
        self.credentials_path = credentials_path
        self.sheet_name = sheet_name
        self.client = None
        self.sheet = None
        self._initialize_connection()
    
    def _load_credentials(self, scope):
        """Load Google credentials from Streamlit secrets or local file."""
        try:
            # Try Streamlit secrets first
            if hasattr(st, 'secrets') and st.secrets is not None:
                secret_creds = st.secrets.get('google_credentials')
                if secret_creds:
                    if isinstance(secret_creds, str):
                        secret_creds = json.loads(secret_creds)
                    if isinstance(secret_creds, dict):
                        return Credentials.from_service_account_info(secret_creds, scopes=scope)

            # Fallback to local credentials.json file
            if os.path.exists(self.credentials_path):
                return Credentials.from_service_account_file(self.credentials_path, scopes=scope)

            return None
        except Exception as e:
            st.error(f"Unable to load Google credentials: {str(e)}")
            return None

    def _initialize_connection(self):
        """Initialize connection to Google Sheets."""
        try:
            # Define scope for Google Sheets and Drive
            scope = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]

            credentials = self._load_credentials(scope)
            if not credentials:
                st.error("Google credentials are not configured. Please add them to Streamlit secrets or upload a local credentials.json file.")
                st.info("To use Google Sheets integration:\n1. Add Google service account credentials to Streamlit secrets as 'google_credentials' or\n2. Save 'credentials.json' in the project root.")
                return

            self.client = gspread.authorize(credentials)

            # Try to open or create the sheet
            try:
                self.sheet = self.client.open(self.sheet_name)
            except gspread.exceptions.SpreadsheetNotFound:
                st.warning(f"Sheet '{self.sheet_name}' not found. Create it in Google Drive first.")
                self.sheet = None

        except Exception as e:
            st.error(f"Error initializing Google Sheets: {str(e)}")
            self.sheet = None
    
    def _get_worksheet(self, name: str):
        """Get a worksheet by name, create if it doesn't exist."""
        if not self.sheet:
            return None
        
        try:
            return self.sheet.worksheet(name)
        except gspread.exceptions.WorksheetNotFound:
            return self.sheet.add_worksheet(name, rows=1000, cols=20)
    
    def save_sales_report(self, report_data: Dict) -> bool:
        """
        Save a daily sales report to Google Sheets.
        
        Args:
            report_data: Dictionary containing sales report fields
            
        Returns:
            True if successful, False otherwise
        """
        try:
            worksheet = self._get_worksheet("Sales Reports")
            if not worksheet:
                return False
            
            # Prepare data row
            data_row = [
                report_data.get('date', ''),
                report_data.get('salesman', ''),
                report_data.get('retailer', ''),
                report_data.get('retailer_mobile', ''),
                report_data.get('area', ''),
                report_data.get('city', ''),
                report_data.get('order_quantity', 0),
                report_data.get('order_value', 0),
                report_data.get('collection', 0),
                report_data.get('outstanding', 0),
                report_data.get('next_visit', ''),
                report_data.get('remarks', ''),
                datetime.now().isoformat()
            ]
            
            # Add headers if worksheet is empty
            if len(worksheet.get_all_values()) == 0:
                headers = ['Date', 'Salesman', 'Retailer', 'Retailer Mobile', 'Area', 
                          'City', 'Order Qty', 'Order Value', 'Collection', 'Outstanding',
                          'Next Visit', 'Remarks', 'Timestamp']
                worksheet.insert_rows([headers], 1)
            
            # Append new row
            worksheet.append_row(data_row)
            st.success("✓ Report saved to Google Sheets!")
            return True
            
        except Exception as e:
            st.error(f"Error saving to Google Sheets: {str(e)}")
            return False
    
    def save_retailer(self, retailer_data: Dict) -> bool:
        """
        Save or update a retailer in Google Sheets.
        
        Args:
            retailer_data: Dictionary containing retailer information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            worksheet = self._get_worksheet("Retailers")
            if not worksheet:
                return False
            
            # Prepare data row
            data_row = [
                retailer_data.get('name', ''),
                retailer_data.get('owner', ''),
                retailer_data.get('mobile', ''),
                retailer_data.get('address', ''),
                retailer_data.get('gst', ''),
                retailer_data.get('area', ''),
                retailer_data.get('city', ''),
                retailer_data.get('last_visit', ''),
                retailer_data.get('last_order', ''),
                retailer_data.get('lifetime_sales', 0),
                retailer_data.get('outstanding', 0),
                retailer_data.get('preferred_product', ''),
                retailer_data.get('notes', ''),
                datetime.now().isoformat()
            ]
            
            # Add headers if worksheet is empty
            if len(worksheet.get_all_values()) == 0:
                headers = ['Name', 'Owner', 'Mobile', 'Address', 'GST', 'Area', 'City',
                          'Last Visit', 'Last Order', 'Lifetime Sales', 'Outstanding',
                          'Preferred Product', 'Notes', 'Created Date']
                worksheet.insert_rows([headers], 1)
            
            worksheet.append_row(data_row)
            st.success("✓ Retailer added to database!")
            return True
            
        except Exception as e:
            st.error(f"Error saving retailer: {str(e)}")
            return False
    
    def get_sales_reports(self) -> pd.DataFrame:
        """
        Retrieve all sales reports from Google Sheets.
        
        Returns:
            DataFrame containing all sales reports
        """
        try:
            worksheet = self._get_worksheet("Sales Reports")
            if not worksheet:
                return pd.DataFrame()
            
            data = worksheet.get_all_values()
            if len(data) <= 1:
                return pd.DataFrame()
            
            df = pd.DataFrame(data[1:], columns=data[0])
            return df
            
        except Exception as e:
            st.error(f"Error retrieving sales reports: {str(e)}")
            return pd.DataFrame()
    
    def get_retailers(self) -> pd.DataFrame:
        """
        Retrieve all retailers from Google Sheets.
        
        Returns:
            DataFrame containing all retailers
        """
        try:
            worksheet = self._get_worksheet("Retailers")
            if not worksheet:
                return pd.DataFrame()
            
            data = worksheet.get_all_values()
            if len(data) <= 1:
                return pd.DataFrame()
            
            df = pd.DataFrame(data[1:], columns=data[0])
            return df
            
        except Exception as e:
            st.error(f"Error retrieving retailers: {str(e)}")
            return pd.DataFrame()
    
    def search_retailer_by_mobile(self, mobile: str) -> Optional[Dict]:
        """Search for retailer by mobile number."""
        try:
            df = self.get_retailers()
            if df.empty:
                return None
            
            result = df[df['Mobile'] == mobile]
            if result.empty:
                return None
            
            return result.iloc[0].to_dict()
            
        except Exception as e:
            st.error(f"Error searching retailer: {str(e)}")
            return None
    
    def get_sales_by_salesman(self, salesman: str) -> pd.DataFrame:
        """Get all sales reports for a specific salesman."""
        try:
            df = self.get_sales_reports()
            if df.empty:
                return pd.DataFrame()
            
            return df[df['Salesman'] == salesman]
            
        except Exception as e:
            st.error(f"Error retrieving salesman data: {str(e)}")
            return pd.DataFrame()
    
    def get_data_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Get sales reports within a date range."""
        try:
            df = self.get_sales_reports()
            if df.empty:
                return pd.DataFrame()
            
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            
            return df[(df['Date'] >= start) & (df['Date'] <= end)]
            
        except Exception as e:
            st.error(f"Error filtering by date: {str(e)}")
            return pd.DataFrame()


@st.cache_resource
def get_sheets_connector():
    """Get or create Google Sheets connector (cached)."""
    return GoogleSheetsConnector()
