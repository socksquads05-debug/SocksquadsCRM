"""
Dashboard page for SocksQuads CRM.
Shows all key metrics and analytics.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.google_sheets import get_sheets_connector
from utils.helpers import (
    calculate_metrics,
    format_currency,
    format_number,
    get_salesman_stats,
    get_area_stats,
    get_sales_by_day,
    get_sales_by_month,
    get_retailers_by_performance
)
from utils.charts import (
    sales_by_day_chart,
    sales_by_month_chart,
    top_salesman_chart,
    top_retailer_chart,
    sales_by_area_chart,
    collection_vs_outstanding_chart,
    retailer_growth_chart,
    collection_rate_chart
)


def show():
    """Display the main dashboard."""
    
    st.title("📊 SocksQuads CRM Dashboard")
    st.markdown("---")
    
    # Get data from Google Sheets
    sheets = get_sheets_connector()
    sales_df = sheets.get_sales_reports()
    
    # Date range filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=30),
            key="dashboard_start"
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now(),
            key="dashboard_end"
        )
    
    # Filter data by date range
    if not sales_df.empty:
        try:
            sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')
            filtered_df = sales_df[
                (sales_df['Date'].dt.date >= start_date) &
                (sales_df['Date'].dt.date <= end_date)
            ]
        except:
            filtered_df = sales_df
    else:
        filtered_df = sales_df
    
    # Calculate metrics
    metrics = calculate_metrics(filtered_df)
    
    # Display key metrics in cards
    st.subheader("📈 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Today's Sales",
            value=format_currency(metrics['total_sales']),
            delta="Last 30 days" if len(filtered_df) > 0 else "No data"
        )
    
    with col2:
        st.metric(
            label="Collections",
            value=format_currency(metrics['total_collection']),
            delta=f"{metrics['collection_rate']:.1f}% rate"
        )
    
    with col3:
        st.metric(
            label="Outstanding",
            value=format_currency(metrics['outstanding']),
            delta="To be collected"
        )
    
    with col4:
        st.metric(
            label="Total Orders",
            value=format_number(metrics['total_orders']),
            delta=f"Avg: {format_currency(metrics['avg_order_value'])}"
        )
    
    st.markdown("---")
    
    # Dashboard charts
    if not filtered_df.empty:
        # Sales and Collections section
        st.subheader("📉 Sales Trends")
        col1, col2 = st.columns(2)
        
        with col1:
            fig = sales_by_day_chart(filtered_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = sales_by_month_chart(filtered_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Top performers section
        st.subheader("🌟 Top Performers")
        col1, col2 = st.columns(2)
        
        with col1:
            fig = top_salesman_chart(filtered_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = top_retailer_chart(filtered_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Area and Collection Analysis
        st.subheader("🗺️ Area Analysis & Collection Status")
        col1, col2 = st.columns(2)
        
        with col1:
            fig = sales_by_area_chart(filtered_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = collection_rate_chart(filtered_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Additional Analytics
        st.subheader("📊 Additional Analytics")
        col1, col2 = st.columns(2)
        
        with col1:
            fig = collection_vs_outstanding_chart(filtered_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = retailer_growth_chart(filtered_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Detailed Tables
        st.subheader("📋 Detailed Breakdown")
        
        tab1, tab2, tab3 = st.tabs(["By Salesman", "By Area", "By Retailer"])
        
        with tab1:
            salesman_stats = get_salesman_stats(filtered_df)
            if not salesman_stats.empty:
                st.dataframe(
                    salesman_stats.style.format({
                        'Sales': '₹{:,.2f}',
                        'Collection': '₹{:,.2f}',
                        'Outstanding': '₹{:,.2f}'
                    }),
                    use_container_width=True
                )
        
        with tab2:
            area_stats = get_area_stats(filtered_df)
            if not area_stats.empty:
                st.dataframe(
                    area_stats.style.format({
                        'Sales': '₹{:,.2f}',
                        'Collection': '₹{:,.2f}',
                        'Outstanding': '₹{:,.2f}'
                    }),
                    use_container_width=True
                )
        
        with tab3:
            retailer_perf = get_retailers_by_performance(filtered_df, top_n=20)
            if not retailer_perf.empty:
                st.dataframe(
                    retailer_perf.style.format({
                        'Total Sales': '₹{:,.2f}',
                        'Collection': '₹{:,.2f}',
                        'Outstanding': '₹{:,.2f}'
                    }),
                    use_container_width=True
                )
        
    else:
        st.info("📌 No sales data available. Start by submitting sales reports.")


if __name__ == "__main__":
    show()
