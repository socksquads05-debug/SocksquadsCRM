"""
Helper functions for SocksQuads CRM Dashboard.
Includes authentication, data processing, and utility functions.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import hashlib


class AuthenticationManager:
    """Manages user authentication and authorization."""
    
    # Credentials stored locally (can be moved to environment variables or config file)
    CREDENTIALS = {
        'admin': {
            'password': 'admin123',  # CHANGE THIS IN PRODUCTION
            'role': 'admin',
            'name': 'Administrator'
        },
        'owner': {
            'password': 'owner123',  # CHANGE THIS IN PRODUCTION
            'role': 'admin',
            'name': 'Owner'
        },
        'raj': {
            'password': 'raj123',  # CHANGE THIS IN PRODUCTION
            'role': 'salesman',
            'name': 'Raj Kumar'
        },
        'priya': {
            'password': 'priya123',  # CHANGE THIS IN PRODUCTION
            'role': 'salesman',
            'name': 'Priya Singh'
        },
        'amit': {
            'password': 'amit123',  # CHANGE THIS IN PRODUCTION
            'role': 'salesman',
            'name': 'Amit Patel'
        }
    }
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def authenticate(username: str, password: str) -> Tuple[bool, Optional[Dict]]:
        """
        Authenticate user credentials.
        
        Returns:
            Tuple of (success: bool, user_data: dict)
        """
        if not username or not password:
            return False, None

        username = username.strip().lower()
        password = password.strip()

        if username not in AuthenticationManager.CREDENTIALS:
            return False, None
        
        user = AuthenticationManager.CREDENTIALS[username]
        if user['password'] != password:
            return False, None
        
        return True, {
            'username': username,
            'name': user['name'],
            'role': user['role']
        }
    
    @staticmethod
    def is_admin(user_data: Dict) -> bool:
        """Check if user is admin."""
        return user_data and user_data.get('role') == 'admin'
    
    @staticmethod
    def is_salesman(user_data: Dict) -> bool:
        """Check if user is salesman."""
        return user_data and user_data.get('role') == 'salesman'
    
    @staticmethod
    def add_user(username: str, password: str, name: str, role: str):
        """Add a new user to credentials."""
        AuthenticationManager.CREDENTIALS[username] = {
            'password': password,
            'role': role,
            'name': name
        }


def initialize_session_state():
    """Initialize session state variables."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Dashboard'


def format_currency(amount) -> str:
    """Format amount as currency (Indian Rupees)."""
    try:
        return f"₹{float(amount):,.2f}"
    except:
        return "₹0.00"


def format_number(value) -> str:
    """Format number with thousand separators."""
    try:
        return f"{int(float(value)):,}"
    except:
        return "0"


def parse_date(date_string: str) -> Optional[datetime]:
    """Parse date string to datetime object."""
    try:
        return pd.to_datetime(date_string)
    except:
        return None


def get_date_range(days: int = 30) -> Tuple[datetime, datetime]:
    """Get date range for last N days."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def filter_dataframe(df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
    """
    Apply multiple filters to a DataFrame.
    
    Args:
        df: Input DataFrame
        filters: Dictionary of column_name: value pairs
        
    Returns:
        Filtered DataFrame
    """
    if df.empty:
        return df
    
    result = df.copy()
    
    for column, value in filters.items():
        if value and column in result.columns:
            if isinstance(value, list):
                result = result[result[column].isin(value)]
            else:
                result = result[result[column] == value]
    
    return result


def calculate_metrics(df: pd.DataFrame) -> Dict:
    """
    Calculate key metrics from sales data.
    
    Args:
        df: Sales data DataFrame
        
    Returns:
        Dictionary of calculated metrics
    """
    if df.empty:
        return {
            'total_sales': 0,
            'total_collection': 0,
            'total_orders': 0,
            'avg_order_value': 0,
            'collection_rate': 0,
            'outstanding': 0
        }
    
    metrics = {
        'total_sales': df['Order Value'].astype(float).sum() if 'Order Value' in df.columns else 0,
        'total_collection': df['Collection'].astype(float).sum() if 'Collection' in df.columns else 0,
        'total_orders': len(df),
        'avg_order_value': df['Order Value'].astype(float).mean() if 'Order Value' in df.columns else 0,
        'outstanding': df['Outstanding'].astype(float).sum() if 'Outstanding' in df.columns else 0,
    }
    
    # Calculate collection rate
    if metrics['total_sales'] > 0:
        metrics['collection_rate'] = (metrics['total_collection'] / metrics['total_sales']) * 100
    else:
        metrics['collection_rate'] = 0
    
    return metrics


def get_salesman_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Get statistics grouped by salesman."""
    if df.empty:
        return pd.DataFrame()
    
    stats = df.groupby('Salesman').agg({
        'Order Value': 'sum',
        'Collection': 'sum',
        'Outstanding': 'sum',
        'Retailer': 'count'
    }).rename(columns={'Retailer': 'Orders'})
    
    stats.columns = ['Sales', 'Collection', 'Outstanding', 'Orders']
    stats = stats.sort_values('Sales', ascending=False)
    
    return stats


def get_area_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Get statistics grouped by area."""
    if df.empty:
        return pd.DataFrame()
    
    stats = df.groupby('Area').agg({
        'Order Value': 'sum',
        'Collection': 'sum',
        'Outstanding': 'sum',
        'Retailer': 'count'
    }).rename(columns={'Retailer': 'Orders'})
    
    stats.columns = ['Sales', 'Collection', 'Outstanding', 'Orders']
    stats = stats.sort_values('Sales', ascending=False)
    
    return stats


def get_product_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Get statistics by product (from notes/remarks field)."""
    if df.empty:
        return pd.DataFrame()
    
    return df.groupby('Remarks').agg({
        'Order Qty': 'sum',
        'Order Value': 'sum'
    }).rename(columns={'Order Qty': 'Quantity', 'Order Value': 'Sales'}).sort_values('Sales', ascending=False)


def export_to_csv(df: pd.DataFrame, filename: str) -> bytes:
    """Convert DataFrame to CSV bytes for download."""
    return df.to_csv(index=False).encode('utf-8')


def get_sales_by_day(df: pd.DataFrame) -> pd.DataFrame:
    """Get sales aggregated by day."""
    if df.empty:
        return pd.DataFrame()
    
    try:
        df_copy = df.copy()
        df_copy['Date'] = pd.to_datetime(df_copy['Date'], errors='coerce')
        daily = df_copy.groupby(df_copy['Date'].dt.date).agg({
            'Order Value': 'sum',
            'Collection': 'sum',
            'Outstanding': 'sum',
            'Retailer': 'count'
        }).rename(columns={'Retailer': 'Orders'})
        daily.columns = ['Sales', 'Collection', 'Outstanding', 'Orders']
        return daily
    except:
        return pd.DataFrame()


def get_sales_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Get sales aggregated by month."""
    if df.empty:
        return pd.DataFrame()
    
    try:
        df_copy = df.copy()
        df_copy['Date'] = pd.to_datetime(df_copy['Date'], errors='coerce')
        monthly = df_copy.groupby(df_copy['Date'].dt.to_period('M')).agg({
            'Order Value': 'sum',
            'Collection': 'sum',
            'Outstanding': 'sum',
            'Retailer': 'count'
        }).rename(columns={'Retailer': 'Orders'})
        monthly.columns = ['Sales', 'Collection', 'Outstanding', 'Orders']
        return monthly
    except:
        return pd.DataFrame()


def get_retailers_by_performance(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Get top retailers by sales value."""
    if df.empty:
        return pd.DataFrame()
    
    top_retailers = df.groupby('Retailer').agg({
        'Order Value': 'sum',
        'Collection': 'sum',
        'Outstanding': 'sum',
        'Area': 'first'
    }).rename(columns={'Order Value': 'Total Sales', 'Area': 'Area'})
    
    top_retailers = top_retailers.sort_values('Total Sales', ascending=False).head(top_n)
    return top_retailers


def get_inactive_retailers(df: pd.DataFrame, days: int = 30) -> pd.DataFrame:
    """Get retailers with no orders in last N days."""
    if df.empty:
        return pd.DataFrame()
    
    try:
        df_copy = df.copy()
        df_copy['Date'] = pd.to_datetime(df_copy['Date'], errors='coerce')
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_orders = df_copy[df_copy['Date'] >= cutoff_date]['Retailer'].unique()
        all_retailers = df_copy['Retailer'].unique()
        
        inactive = [r for r in all_retailers if r not in recent_orders]
        return pd.DataFrame({'Retailer': inactive})
    except:
        return pd.DataFrame()
