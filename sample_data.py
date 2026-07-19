"""
Sample data generator for SocksQuads CRM.
Run this script to populate Google Sheets with sample data for testing.

Usage:
    python sample_data.py
"""

import csv
from datetime import datetime, timedelta
from random import choice, randint, uniform
import os


def generate_sample_sales_reports(num_records=50):
    """Generate sample sales report data."""
    salesmen = ['Raj Kumar', 'Priya Singh', 'Amit Patel']
    areas = ['North', 'South', 'East', 'West', 'Central']
    cities = ['Delhi', 'Mumbai', 'Bangalore', 'Pune', 'Chennai', 'Hyderabad', 'Kolkata']
    
    data = []
    
    # Add header
    data.append([
        'Date', 'Salesman', 'Retailer', 'Retailer Mobile', 'Area', 'City',
        'Order Qty', 'Order Value', 'Collection', 'Outstanding', 'Next Visit', 'Remarks'
    ])
    
    # Generate records
    for i in range(num_records):
        days_ago = randint(0, 30)
        date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        salesman = choice(salesmen)
        area = choice(areas)
        city = choice(cities)
        
        retailer_name = f"Retailer {i+1}"
        retailer_mobile = f"9{randint(100000000, 999999999)}"
        
        order_qty = randint(10, 500)
        order_value = order_qty * uniform(50, 200)
        collection = order_value if randint(0, 100) > 30 else order_value * 0.7
        outstanding = order_value - collection
        
        next_visit = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')
        remarks = f"Popular socks model, good demand"
        
        data.append([
            date,
            salesman,
            retailer_name,
            retailer_mobile,
            area,
            city,
            int(order_qty),
            f"{order_value:.2f}",
            f"{collection:.2f}",
            f"{outstanding:.2f}",
            next_visit,
            remarks
        ])
    
    return data


def generate_sample_retailers(num_records=20):
    """Generate sample retailer data."""
    areas = ['North', 'South', 'East', 'West', 'Central']
    cities = ['Delhi', 'Mumbai', 'Bangalore', 'Pune', 'Chennai', 'Hyderabad', 'Kolkata']
    products = ['Classic Socks', 'Sports Socks', 'Winter Socks', 'Formal Socks', 'Kids Socks']
    
    data = []
    
    # Add header
    data.append([
        'Name', 'Owner', 'Mobile', 'Address', 'GST', 'Area', 'City',
        'Last Visit', 'Last Order', 'Lifetime Sales', 'Outstanding', 'Preferred Product', 'Notes'
    ])
    
    # Generate records
    for i in range(num_records):
        days_ago = randint(0, 30)
        
        retailer_name = f"Shop {i+1}"
        owner_name = f"Owner {i+1}"
        mobile = f"9{randint(100000000, 999999999)}"
        address = f"Address {i+1}, City"
        gst = f"22AABCT{randint(1000, 9999)}M1Z5" if randint(0, 1) else ""
        area = choice(areas)
        city = choice(cities)
        
        last_visit = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        last_order = (datetime.now() - timedelta(days=randint(5, 30))).strftime('%Y-%m-%d')
        
        lifetime_sales = uniform(10000, 500000)
        outstanding = lifetime_sales * uniform(0, 0.3)  # 0-30% outstanding
        
        preferred_product = choice(products)
        notes = f"Regular customer, good payment history"
        
        data.append([
            retailer_name,
            owner_name,
            mobile,
            address,
            gst,
            area,
            city,
            last_visit,
            last_order,
            f"{lifetime_sales:.2f}",
            f"{outstanding:.2f}",
            preferred_product,
            notes
        ])
    
    return data


def save_to_csv(data, filename):
    """Save data to CSV file."""
    filepath = f"data/{filename}"
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    print(f"✓ Saved {len(data)-1} records to {filepath}")


def main():
    """Generate and save sample data."""
    print("🧦 SocksQuads CRM - Sample Data Generator")
    print("=" * 50)
    
    # Generate sales reports
    print("\n📊 Generating sample sales reports...")
    sales_data = generate_sample_sales_reports(50)
    save_to_csv(sales_data, "sample_sales_reports.csv")
    
    # Generate retailers
    print("🏪 Generating sample retailers...")
    retailers_data = generate_sample_retailers(20)
    save_to_csv(retailers_data, "sample_retailers.csv")
    
    print("\n" + "=" * 50)
    print("✅ Sample data generated successfully!")
    print("\nNext steps:")
    print("1. Go to Google Sheets: https://sheets.google.com")
    print("2. Create a new sheet named 'SocksQuads CRM'")
    print("3. In 'Sales Reports' sheet, paste data from: data/sample_sales_reports.csv")
    print("4. In 'Retailers' sheet, paste data from: data/sample_retailers.csv")
    print("5. Run the app: streamlit run app.py")


if __name__ == "__main__":
    main()
