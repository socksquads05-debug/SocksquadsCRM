"""
Analytics page for SocksQuads CRM.
Advanced analytics and business insights.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.google_sheets import get_sheets_connector
from utils.helpers import (
    format_currency,
    get_inactive_retailers,
    get_retailers_by_performance
)
from utils.charts import (
    top_salesman_chart,
    top_retailer_chart,
    sales_by_area_chart,
    order_distribution_chart,
    top_products_chart
)


def show():
    """Display analytics page."""
    st.set_page_config(page_title="Analytics", layout="wide")
    
    st.title("📈 Advanced Analytics")
    st.markdown("Deep insights into sales performance and business trends.")
    st.markdown("---")
    
    sheets = get_sheets_connector()
    sales_df = sheets.get_sales_reports()
    retailers_df = sheets.get_retailers()
    
    if sales_df.empty:
        st.info("No sales data available yet. Start by submitting sales reports.")
        return
    
    # Convert date column
    try:
        sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')
    except:
        pass
    
    # Tabs for different analytics
    tab1, tab2, tab3, tab4 = st.tabs(["🌟 Key Insights", "🏪 Retailer Analysis", "👥 Sales Team", "⚠️ Alerts"])
    
    # Tab 1: Key Insights
    with tab1:
        st.subheader("Key Insights")
        
        # Time period selector
        period = st.selectbox("Select Time Period", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"])
        
        if period == "Last 7 Days":
            cutoff_date = datetime.now() - timedelta(days=7)
        elif period == "Last 30 Days":
            cutoff_date = datetime.now() - timedelta(days=30)
        elif period == "Last 90 Days":
            cutoff_date = datetime.now() - timedelta(days=90)
        else:
            cutoff_date = datetime.min
        
        filtered_df = sales_df[sales_df['Date'] >= cutoff_date]
        
        if not filtered_df.empty:
            # Growth metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_sales = filtered_df['Order Value'].astype(float).sum()
                st.metric("Total Sales", format_currency(total_sales))
            with col2:
                avg_daily_sales = total_sales / max(1, filtered_df['Date'].dt.date.nunique())
                st.metric("Avg Daily Sales", format_currency(avg_daily_sales))
            with col3:
                total_orders = len(filtered_df)
                st.metric("Total Orders", total_orders)
            
            st.markdown("---")
            
            # Top performers
            col1, col2 = st.columns(2)
            with col1:
                fig = top_salesman_chart(filtered_df, top_n=5)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = top_retailer_chart(filtered_df, top_n=5)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # Additional insights
            col1, col2 = st.columns(2)
            with col1:
                fig = sales_by_area_chart(filtered_df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = order_distribution_chart(filtered_df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: Retailer Analysis
    with tab2:
        st.subheader("Retailer Analysis")
        
        analysis_type = st.selectbox(
            "Select Analysis Type",
            ["Top Retailers", "Bottom Retailers", "Inactive Retailers", "High Outstanding", "New Retailers"]
        )
        
        if analysis_type == "Top Retailers":
            st.subheader("Top 10 Retailers")
            top_retailers = get_retailers_by_performance(sales_df, top_n=10)
            if not top_retailers.empty:
                st.dataframe(
                    top_retailers.style.format({
                        'Total Sales': '₹{:,.2f}',
                        'Collection': '₹{:,.2f}',
                        'Outstanding': '₹{:,.2f}'
                    }),
                    use_container_width=True
                )
        
        elif analysis_type == "Bottom Retailers":
            st.subheader("Bottom 10 Retailers (Lowest Sales)")
            bottom_retailers = get_retailers_by_performance(sales_df, top_n=10)
            if not bottom_retailers.empty:
                bottom_retailers = bottom_retailers.iloc[::-1]  # Reverse
                st.dataframe(
                    bottom_retailers.style.format({
                        'Total Sales': '₹{:,.2f}',
                        'Collection': '₹{:,.2f}',
                        'Outstanding': '₹{:,.2f}'
                    }),
                    use_container_width=True
                )
        
        elif analysis_type == "Inactive Retailers":
            st.subheader("Retailers Inactive for 30+ Days")
            inactive = get_inactive_retailers(sales_df, days=30)
            if not inactive.empty:
                st.warning(f"Found {len(inactive)} inactive retailers")
                st.dataframe(inactive, use_container_width=True)
            else:
                st.success("No inactive retailers! All retailers are active.")
        
        elif analysis_type == "High Outstanding":
            st.subheader("Retailers with High Outstanding")
            if not retailers_df.empty:
                high_outstanding = retailers_df.nlargest(10, 'Outstanding')[
                    ['Name', 'Area', 'Outstanding', 'Last Visit']
                ].copy()
                st.dataframe(
                    high_outstanding.style.format({'Outstanding': '₹{:,.2f}'}),
                    use_container_width=True,
                    hide_index=True
                )
        
        elif analysis_type == "New Retailers":
            st.subheader("Recently Added Retailers")
            if not retailers_df.empty:
                new_retailers = retailers_df.tail(10)[
                    ['Name', 'Owner', 'Mobile', 'Area', 'City']
                ].copy()
                st.dataframe(
                    new_retailers,
                    use_container_width=True,
                    hide_index=True
                )
    
    # Tab 3: Sales Team Performance
    with tab3:
        st.subheader("Sales Team Performance")
        
        # Team statistics
        team_stats = sales_df.groupby('Salesman').agg({
            'Order Value': ['sum', 'count', 'mean'],
            'Collection': 'sum',
            'Outstanding': 'sum',
            'Retailer': 'nunique'
        }).round(2)
        
        team_stats.columns = ['Total Sales', 'Orders', 'Avg Order', 'Collections', 'Outstanding', 'Retailers Visited']
        team_stats = team_stats.sort_values('Total Sales', ascending=False)
        
        st.subheader("Team Statistics (All Time)")
        st.dataframe(
            team_stats.style.format({
                'Total Sales': '₹{:,.2f}',
                'Avg Order': '₹{:,.2f}',
                'Collections': '₹{:,.2f}',
                'Outstanding': '₹{:,.2f}'
            }),
            use_container_width=True
        )
        
        st.markdown("---")
        
        # Individual salesman analysis
        st.subheader("Individual Salesman Analysis")
        salesman_name = st.selectbox(
            "Select Salesman",
            sorted(sales_df['Salesman'].unique().tolist())
        )
        
        salesman_data = sales_df[sales_df['Salesman'] == salesman_name]
        
        if not salesman_data.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            total_sales = salesman_data['Order Value'].astype(float).sum()
            total_collection = salesman_data['Collection'].astype(float).sum()
            total_outstanding = salesman_data['Outstanding'].astype(float).sum()
            retailers_visited = salesman_data['Retailer'].nunique()
            
            with col1:
                st.metric("Total Sales", format_currency(total_sales))
            with col2:
                st.metric("Collections", format_currency(total_collection))
            with col3:
                st.metric("Outstanding", format_currency(total_outstanding))
            with col4:
                st.metric("Retailers Visited", retailers_visited)
            
            st.markdown("---")
            
            # Performance graph
            fig = top_retailer_chart(salesman_data, top_n=10)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    # Tab 4: Alerts & Warnings
    with tab4:
        st.subheader("⚠️ Alerts & Warnings")
        
        alerts_found = False
        
        # Alert 1: Low collection rate
        if not sales_df.empty:
            total_sales = sales_df['Order Value'].astype(float).sum()
            total_collection = sales_df['Collection'].astype(float).sum()
            collection_rate = (total_collection / total_sales * 100) if total_sales > 0 else 0
            
            if collection_rate < 70:
                st.warning(f"⚠️ Low Collection Rate: {collection_rate:.1f}%")
                st.info("Collection rate is below 70%. Focus on pending collections.")
                alerts_found = True
        
        # Alert 2: High outstanding
        if not sales_df.empty:
            outstanding = sales_df['Outstanding'].astype(float).sum()
            if outstanding > total_collection:
                st.warning(f"⚠️ High Outstanding Amount: {format_currency(outstanding)}")
                st.info("Outstanding amount is higher than collections. Schedule follow-ups.")
                alerts_found = True
        
        # Alert 3: Inactive retailers
        inactive = get_inactive_retailers(sales_df, days=30)
        if not inactive.empty and len(inactive) > 0:
            st.warning(f"⚠️ {len(inactive)} Retailers Inactive for 30+ Days")
            st.info("These retailers need immediate attention.")
            alerts_found = True
        
        # Alert 4: No sales today
        today_date = datetime.now().date()
        today_sales = sales_df[sales_df['Date'].dt.date == today_date]
        if today_sales.empty:
            st.info("ℹ️ No sales reports submitted today yet.")
            alerts_found = True
        
        if not alerts_found:
            st.success("✅ No alerts! Everything is performing well.")
        
        st.markdown("---")
        
        # Summary statistics
        st.subheader("Summary Statistics")
        
        if not sales_df.empty:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Transactions", len(sales_df))
            with col2:
                unique_retailers = sales_df['Retailer'].nunique()
                st.metric("Unique Retailers", unique_retailers)
            with col3:
                unique_salesmen = sales_df['Salesman'].nunique()
                st.metric("Active Salesmen", unique_salesmen)


if __name__ == "__main__":
    show()
