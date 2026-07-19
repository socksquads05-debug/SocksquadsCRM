"""
Salesman page for SocksQuads CRM.
Allows salespeople to submit daily sales reports and view their performance.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.google_sheets import get_sheets_connector
from utils.helpers import (
    calculate_metrics,
    format_currency,
    get_salesman_stats
)
from utils.charts import (
    sales_by_day_chart,
    top_retailer_chart,
    collection_rate_chart
)


def show():
    """Display salesman page."""
    
    st.title("💼 Daily Sales Report")
    st.markdown("Submit your daily sales and collection data here.")
    st.markdown("---")
    
    # Get the current salesman from session
    current_user = st.session_state.get('user_data', {})
    salesman_name = current_user.get('name', 'Salesman')
    
    # Tabs for different sections
    tab1, tab2 = st.tabs(["📝 Submit Report", "📊 My Performance"])
    
    # Tab 1: Submit Report
    with tab1:
        st.subheader("Submit Today's Report")
        
        sheets = get_sheets_connector()
        
        with st.form("daily_report_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                report_date = st.date_input("Date", value=datetime.now())
                retailer_name = st.text_input(
                    "Retailer Name",
                    placeholder="Enter retailer name",
                    key="retailer_name"
                )
                retailer_mobile = st.text_input(
                    "Retailer Mobile",
                    placeholder="Enter mobile number",
                    key="retailer_mobile",
                    max_chars=10
                )
                area = st.text_input(
                    "Area",
                    placeholder="e.g., North, South, East, West",
                    key="area"
                )
            
            with col2:
                city = st.text_input(
                    "City",
                    placeholder="Enter city name",
                    key="city"
                )
                order_quantity = st.number_input(
                    "Order Quantity (units)",
                    min_value=0,
                    value=0,
                    key="order_qty"
                )
                order_value = st.number_input(
                    "Order Value (₹)",
                    min_value=0.0,
                    value=0.0,
                    step=100.0,
                    key="order_value"
                )
                collection = st.number_input(
                    "Collection Received (₹)",
                    min_value=0.0,
                    value=0.0,
                    step=100.0,
                    key="collection"
                )
            
            col1, col2 = st.columns(2)
            
            with col1:
                outstanding = st.number_input(
                    "Outstanding Amount (₹)",
                    min_value=0.0,
                    value=0.0,
                    step=100.0,
                    key="outstanding"
                )
                next_visit = st.date_input(
                    "Next Visit Date",
                    value=datetime.now() + timedelta(days=7),
                    key="next_visit"
                )
            
            with col2:
                remarks = st.text_area(
                    "Remarks / Product Details",
                    placeholder="Add any remarks or product details",
                    height=100,
                    key="remarks"
                )
            
            # Submit button
            submitted = st.form_submit_button(
                "✅ Submit Report",
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                if not retailer_name or not retailer_mobile or not area or not city:
                    st.error("Please fill in all required fields (marked with *).")
                else:
                    report_data = {
                        'date': str(report_date),
                        'salesman': salesman_name,
                        'retailer': retailer_name,
                        'retailer_mobile': retailer_mobile,
                        'area': area,
                        'city': city,
                        'order_quantity': int(order_quantity),
                        'order_value': float(order_value),
                        'collection': float(collection),
                        'outstanding': float(outstanding),
                        'next_visit': str(next_visit),
                        'remarks': remarks
                    }
                    
                    # Save to Google Sheets
                    if sheets.save_sales_report(report_data):
                        st.success("✓ Report submitted successfully!")
                        st.balloons()
    
    # Tab 2: My Performance
    with tab2:
        st.subheader("Your Performance")
        
        sheets = get_sheets_connector()
        all_sales_df = sheets.get_sales_reports()
        
        if all_sales_df.empty:
            st.info("No sales data available yet.")
        else:
            # Filter for current salesman
            salesman_data = all_sales_df[all_sales_df['Salesman'] == salesman_name]
            
            if salesman_data.empty:
                st.info(f"No reports submitted by {salesman_name} yet.")
            else:
                # Show metrics
                st.subheader("📈 Your Metrics (All Time)")
                metrics = calculate_metrics(salesman_data)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Sales", format_currency(metrics['total_sales']))
                with col2:
                    st.metric("Collections", format_currency(metrics['total_collection']))
                with col3:
                    st.metric("Outstanding", format_currency(metrics['outstanding']))
                with col4:
                    st.metric("Total Orders", int(metrics['total_orders']))
                
                st.markdown("---")
                
                # Charts
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = sales_by_day_chart(salesman_data)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = collection_rate_chart(salesman_data)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                
                # Recent reports
                st.subheader("📋 Your Recent Reports")
                display_df = salesman_data.copy()
                display_df = display_df.sort_values('Date', ascending=False).head(10)
                
                # Format for display
                display_df = display_df[[
                    'Date', 'Retailer', 'Area', 'City',
                    'Order Qty', 'Order Value', 'Collection', 'Outstanding'
                ]].copy()
                
                st.dataframe(
                    display_df.style.format({
                        'Order Value': '₹{:,.2f}',
                        'Collection': '₹{:,.2f}',
                        'Outstanding': '₹{:,.2f}',
                        'Order Qty': '{:.0f}'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
                
                # Download option
                csv = display_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"my_reports_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )


if __name__ == "__main__":
    show()
