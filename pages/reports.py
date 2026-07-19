"""
Reports page for SocksQuads CRM.
Generate daily, weekly, monthly, and custom reports with export options.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.google_sheets import get_sheets_connector
from utils.helpers import (
    format_currency,
    calculate_metrics,
    get_salesman_stats,
    get_area_stats
)


def show():
    """Display reports page."""
    st.set_page_config(page_title="Reports", layout="wide")
    
    st.title("📊 Reports & Analytics")
    st.markdown("Generate and export sales reports in various formats.")
    st.markdown("---")
    
    sheets = get_sheets_connector()
    sales_df = sheets.get_sales_reports()
    
    if sales_df.empty:
        st.info("No sales data available. Start by submitting sales reports.")
        return
    
    # Convert date column
    try:
        sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')
    except:
        pass
    
    # Report type selection
    report_type = st.selectbox(
        "Select Report Type",
        [
            "Daily Report",
            "Weekly Report",
            "Monthly Report",
            "Salesman Report",
            "Area Report",
            "Collection Report",
            "Custom Date Range"
        ]
    )
    
    st.markdown("---")
    
    # Generate report based on selection
    if report_type == "Daily Report":
        show_daily_report(sales_df)
    
    elif report_type == "Weekly Report":
        show_weekly_report(sales_df)
    
    elif report_type == "Monthly Report":
        show_monthly_report(sales_df)
    
    elif report_type == "Salesman Report":
        show_salesman_report(sales_df)
    
    elif report_type == "Area Report":
        show_area_report(sales_df)
    
    elif report_type == "Collection Report":
        show_collection_report(sales_df)
    
    elif report_type == "Custom Date Range":
        show_custom_report(sales_df)


def show_daily_report(sales_df):
    """Display daily sales report."""
    st.subheader("Daily Sales Report")
    
    # Select date
    selected_date = st.date_input("Select Date", value=datetime.now())
    
    # Filter data
    filtered_df = sales_df[sales_df['Date'].dt.date == selected_date]
    
    if filtered_df.empty:
        st.info(f"No sales data for {selected_date.strftime('%d-%m-%Y')}.")
    else:
        # Metrics
        metrics = calculate_metrics(filtered_df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sales", format_currency(metrics['total_sales']))
        with col2:
            st.metric("Collections", format_currency(metrics['total_collection']))
        with col3:
            st.metric("Outstanding", format_currency(metrics['outstanding']))
        with col4:
            st.metric("Orders Count", int(metrics['total_orders']))
        
        st.markdown("---")
        
        # Detailed data
        st.subheader("Transactions for the Day")
        display_df = filtered_df[[
            'Date', 'Salesman', 'Retailer', 'Area', 'Order Qty',
            'Order Value', 'Collection', 'Outstanding'
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
        
        # Download button
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"daily_report_{selected_date.strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )


def show_weekly_report(sales_df):
    """Display weekly sales report."""
    st.subheader("Weekly Sales Report")
    
    # Select week
    selected_date = st.date_input("Select Date (Week)", value=datetime.now())
    week_start = selected_date - timedelta(days=selected_date.weekday())
    week_end = week_start + timedelta(days=6)
    
    # Filter data
    filtered_df = sales_df[
        (sales_df['Date'].dt.date >= week_start) &
        (sales_df['Date'].dt.date <= week_end)
    ]
    
    if filtered_df.empty:
        st.info(f"No sales data for week {week_start} to {week_end}.")
    else:
        # Show summary
        st.subheader(f"Week: {week_start.strftime('%d-%m-%Y')} to {week_end.strftime('%d-%m-%Y')}")
        
        metrics = calculate_metrics(filtered_df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sales", format_currency(metrics['total_sales']))
        with col2:
            st.metric("Collections", format_currency(metrics['total_collection']))
        with col3:
            st.metric("Outstanding", format_currency(metrics['outstanding']))
        with col4:
            st.metric("Orders Count", int(metrics['total_orders']))
        
        st.markdown("---")
        
        # Daily breakdown
        st.subheader("Daily Breakdown")
        daily_stats = filtered_df.groupby(filtered_df['Date'].dt.date).agg({
            'Order Value': 'sum',
            'Collection': 'sum',
            'Outstanding': 'sum',
            'Retailer': 'count'
        }).rename(columns={'Retailer': 'Orders'})
        daily_stats.columns = ['Sales', 'Collection', 'Outstanding', 'Orders']
        
        st.dataframe(
            daily_stats.style.format({
                'Sales': '₹{:,.2f}',
                'Collection': '₹{:,.2f}',
                'Outstanding': '₹{:,.2f}',
                'Orders': '{:.0f}'
            }),
            use_container_width=True
        )
        
        # Download button
        csv = filtered_df[[
            'Date', 'Salesman', 'Retailer', 'Area', 'Order Qty',
            'Order Value', 'Collection', 'Outstanding'
        ]].to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"weekly_report_{week_start.strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )


def show_monthly_report(sales_df):
    """Display monthly sales report."""
    st.subheader("Monthly Sales Report")
    
    # Select month
    cols = st.columns(2)
    with cols[0]:
        month = st.selectbox("Month", range(1, 13), format_func=lambda x: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][x-1])
    with cols[1]:
        year = st.number_input("Year", value=datetime.now().year, min_value=2020)
    
    # Filter data
    filtered_df = sales_df[
        (sales_df['Date'].dt.month == month) &
        (sales_df['Date'].dt.year == year)
    ]
    
    if filtered_df.empty:
        st.info(f"No sales data for {['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][month-1]} {year}.")
    else:
        metrics = calculate_metrics(filtered_df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sales", format_currency(metrics['total_sales']))
        with col2:
            st.metric("Collections", format_currency(metrics['total_collection']))
        with col3:
            st.metric("Outstanding", format_currency(metrics['outstanding']))
        with col4:
            st.metric("Orders Count", int(metrics['total_orders']))
        
        st.markdown("---")
        
        # Salesman breakdown
        st.subheader("Salesman Breakdown")
        salesman_stats = get_salesman_stats(filtered_df)
        st.dataframe(
            salesman_stats.style.format({
                'Sales': '₹{:,.2f}',
                'Collection': '₹{:,.2f}',
                'Outstanding': '₹{:,.2f}',
                'Orders': '{:.0f}'
            }),
            use_container_width=True
        )
        
        # Download button
        csv = filtered_df[[
            'Date', 'Salesman', 'Retailer', 'Area', 'Order Qty',
            'Order Value', 'Collection', 'Outstanding'
        ]].to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"monthly_report_{year}{month:02d}.csv",
            mime="text/csv"
        )


def show_salesman_report(sales_df):
    """Display salesman performance report."""
    st.subheader("Salesman Performance Report")
    
    # Select salesman
    salesmen = sorted(sales_df['Salesman'].unique().tolist())
    selected_salesman = st.selectbox("Select Salesman", salesmen)
    
    # Filter data
    filtered_df = sales_df[sales_df['Salesman'] == selected_salesman]
    
    if filtered_df.empty:
        st.info("No data for this salesman.")
    else:
        metrics = calculate_metrics(filtered_df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sales", format_currency(metrics['total_sales']))
        with col2:
            st.metric("Collections", format_currency(metrics['total_collection']))
        with col3:
            st.metric("Outstanding", format_currency(metrics['outstanding']))
        with col4:
            st.metric("Orders Count", int(metrics['total_orders']))
        
        st.markdown("---")
        
        # Top retailers
        st.subheader("Top Retailers Visited")
        top_retailers = filtered_df.groupby('Retailer')['Order Value'].sum().nlargest(10).reset_index()
        st.dataframe(
            top_retailers.style.format({'Order Value': '₹{:,.2f}'}),
            use_container_width=True,
            hide_index=True
        )
        
        # Download button
        csv = filtered_df[[
            'Date', 'Retailer', 'Area', 'Order Qty',
            'Order Value', 'Collection', 'Outstanding'
        ]].to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"salesman_report_{selected_salesman}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )


def show_area_report(sales_df):
    """Display area performance report."""
    st.subheader("Area Performance Report")
    
    # Select area
    areas = sorted(sales_df['Area'].unique().tolist())
    selected_area = st.selectbox("Select Area", areas)
    
    # Filter data
    filtered_df = sales_df[sales_df['Area'] == selected_area]
    
    if filtered_df.empty:
        st.info("No data for this area.")
    else:
        metrics = calculate_metrics(filtered_df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sales", format_currency(metrics['total_sales']))
        with col2:
            st.metric("Collections", format_currency(metrics['total_collection']))
        with col3:
            st.metric("Outstanding", format_currency(metrics['outstanding']))
        with col4:
            st.metric("Orders Count", int(metrics['total_orders']))
        
        st.markdown("---")
        
        # Area statistics
        st.subheader("Area Statistics")
        area_stats = get_area_stats(filtered_df)
        st.dataframe(
            area_stats.style.format({
                'Sales': '₹{:,.2f}',
                'Collection': '₹{:,.2f}',
                'Outstanding': '₹{:,.2f}',
                'Orders': '{:.0f}'
            }),
            use_container_width=True
        )
        
        # Download button
        csv = filtered_df[[
            'Date', 'Salesman', 'Retailer', 'Order Qty',
            'Order Value', 'Collection', 'Outstanding'
        ]].to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"area_report_{selected_area}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )


def show_collection_report(sales_df):
    """Display collection report."""
    st.subheader("Collection Report")
    
    # Date range
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    # Filter data
    filtered_df = sales_df[
        (sales_df['Date'].dt.date >= start_date) &
        (sales_df['Date'].dt.date <= end_date)
    ]
    
    if filtered_df.empty:
        st.info("No data in selected date range.")
    else:
        total_sales = filtered_df['Order Value'].astype(float).sum()
        total_collection = filtered_df['Collection'].astype(float).sum()
        total_outstanding = filtered_df['Outstanding'].astype(float).sum()
        collection_rate = (total_collection / total_sales * 100) if total_sales > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sales", format_currency(total_sales))
        with col2:
            st.metric("Total Collection", format_currency(total_collection))
        with col3:
            st.metric("Total Outstanding", format_currency(total_outstanding))
        with col4:
            st.metric("Collection Rate", f"{collection_rate:.1f}%")
        
        st.markdown("---")
        
        # Collection by salesman
        st.subheader("Collection by Salesman")
        collection_by_salesman = filtered_df.groupby('Salesman').agg({
            'Collection': 'sum',
            'Outstanding': 'sum'
        }).reset_index()
        collection_by_salesman.columns = ['Salesman', 'Collected', 'Outstanding']
        
        st.dataframe(
            collection_by_salesman.style.format({
                'Collected': '₹{:,.2f}',
                'Outstanding': '₹{:,.2f}'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # Download button
        csv = filtered_df[[
            'Date', 'Salesman', 'Retailer', 'Collection', 'Outstanding'
        ]].to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"collection_report_{start_date.strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )


def show_custom_report(sales_df):
    """Display custom date range report."""
    st.subheader("Custom Date Range Report")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30), key="custom_start")
    with col2:
        end_date = st.date_input("End Date", value=datetime.now(), key="custom_end")
    
    # Filter data
    filtered_df = sales_df[
        (sales_df['Date'].dt.date >= start_date) &
        (sales_df['Date'].dt.date <= end_date)
    ]
    
    if filtered_df.empty:
        st.info("No data in selected date range.")
    else:
        metrics = calculate_metrics(filtered_df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sales", format_currency(metrics['total_sales']))
        with col2:
            st.metric("Collections", format_currency(metrics['total_collection']))
        with col3:
            st.metric("Outstanding", format_currency(metrics['outstanding']))
        with col4:
            st.metric("Orders Count", int(metrics['total_orders']))
        
        st.markdown("---")
        
        # Full data table
        st.subheader("Complete Data")
        display_df = filtered_df[[
            'Date', 'Salesman', 'Retailer', 'Area', 'Order Qty',
            'Order Value', 'Collection', 'Outstanding'
        ]].sort_values('Date', ascending=False).copy()
        
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
        
        # Download button
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"custom_report_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    show()
