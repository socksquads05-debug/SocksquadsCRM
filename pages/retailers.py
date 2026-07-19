"""
Retailers management page for SocksQuads CRM.
Allows viewing, searching, and managing retailer information.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.google_sheets import get_sheets_connector
from utils.helpers import format_currency


def show():
    """Display retailers management page."""
    st.set_page_config(page_title="Retailers", layout="wide")
    
    st.title("🏪 Retailer Database")
    st.markdown("Manage and view all retailer information.")
    st.markdown("---")
    
    sheets = get_sheets_connector()
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["🔍 Search & View", "➕ Add New Retailer", "📊 Analysis"])
    
    # Tab 1: Search and View
    with tab1:
        st.subheader("Search Retailers")
        
        retailers_df = sheets.get_retailers()
        
        if retailers_df.empty:
            st.info("No retailers in database yet. Add your first retailer!")
        else:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                search_type = st.selectbox(
                    "Search by",
                    ["Name", "Mobile", "Area", "City"]
                )
            
            with col2:
                if search_type == "Name":
                    search_value = st.text_input("Enter retailer name", placeholder="Search name")
                elif search_type == "Mobile":
                    search_value = st.text_input("Enter mobile number", placeholder="Search mobile", max_chars=10)
                elif search_type == "Area":
                    areas = retailers_df['Area'].unique().tolist()
                    search_value = st.selectbox("Select area", ["All"] + sorted(areas))
                else:  # City
                    cities = retailers_df['City'].unique().tolist()
                    search_value = st.selectbox("Select city", ["All"] + sorted(cities))
            
            with col3:
                st.empty()
            with col4:
                st.empty()
            
            # Filter data
            if search_value and search_value != "All":
                if search_type == "Name":
                    filtered_df = retailers_df[retailers_df['Name'].str.contains(search_value, case=False, na=False)]
                elif search_type == "Mobile":
                    filtered_df = retailers_df[retailers_df['Mobile'] == search_value]
                else:
                    filtered_df = retailers_df[retailers_df[search_type] == search_value]
            else:
                filtered_df = retailers_df if search_value != "All" else retailers_df
            
            if filtered_df.empty:
                st.warning("No retailers found matching your search.")
            else:
                st.subheader(f"Found {len(filtered_df)} Retailer(s)")
                
                # Display as expandable cards
                for idx, row in filtered_df.iterrows():
                    with st.expander(f"🏢 {row['Name']} - {row['Mobile']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Basic Information**")
                            st.write(f"**Name:** {row['Name']}")
                            st.write(f"**Owner:** {row['Owner']}")
                            st.write(f"**Mobile:** {row['Mobile']}")
                            st.write(f"**Address:** {row['Address']}")
                            st.write(f"**GST Number:** {row['GST'] if row['GST'] else 'N/A'}")
                        
                        with col2:
                            st.write("**Location & Performance**")
                            st.write(f"**Area:** {row['Area']}")
                            st.write(f"**City:** {row['City']}")
                            st.write(f"**Last Visit:** {row['Last Visit']}")
                            st.write(f"**Last Order:** {row['Last Order']}")
                        
                        st.markdown("---")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Financial**")
                            st.write(f"**Lifetime Sales:** {format_currency(float(row['Lifetime Sales']))}")
                            st.write(f"**Outstanding:** {format_currency(float(row['Outstanding']))}")
                        
                        with col2:
                            st.write("**Preferences**")
                            st.write(f"**Preferred Product:** {row['Preferred Product']}")
                            st.write(f"**Notes:** {row['Notes']}")
    
    # Tab 2: Add New Retailer
    with tab2:
        st.subheader("Add New Retailer")
        
        with st.form("add_retailer_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                retailer_name = st.text_input("Retailer Name *", placeholder="Enter retailer name")
                owner_name = st.text_input("Owner Name *", placeholder="Enter owner name")
                mobile = st.text_input("Mobile Number *", placeholder="10-digit mobile number", max_chars=10)
                address = st.text_area("Address *", placeholder="Enter complete address", height=80)
            
            with col2:
                gst = st.text_input("GST Number", placeholder="Optional")
                area = st.text_input("Area *", placeholder="e.g., North, South, East, West")
                city = st.text_input("City *", placeholder="Enter city name")
                preferred_product = st.text_input("Preferred Product", placeholder="Main products they buy")
            
            notes = st.text_area("Notes", placeholder="Additional notes about retailer")
            
            submitted = st.form_submit_button(
                "✅ Add Retailer",
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                if not (retailer_name and owner_name and mobile and area and city and address):
                    st.error("Please fill in all required fields (marked with *).")
                else:
                    retailer_data = {
                        'name': retailer_name,
                        'owner': owner_name,
                        'mobile': mobile,
                        'address': address,
                        'gst': gst,
                        'area': area,
                        'city': city,
                        'last_visit': datetime.now().strftime('%Y-%m-%d'),
                        'last_order': '-',
                        'lifetime_sales': 0,
                        'outstanding': 0,
                        'preferred_product': preferred_product,
                        'notes': notes
                    }
                    
                    if sheets.save_retailer(retailer_data):
                        st.success("✓ Retailer added successfully!")
    
    # Tab 3: Analysis
    with tab3:
        st.subheader("Retailer Analytics")
        
        retailers_df = sheets.get_retailers()
        
        if retailers_df.empty:
            st.info("No retailers in database yet.")
        else:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Retailers", len(retailers_df))
            
            with col2:
                unique_areas = retailers_df['Area'].nunique()
                st.metric("Unique Areas", unique_areas)
            
            with col3:
                unique_cities = retailers_df['City'].nunique()
                st.metric("Unique Cities", unique_cities)
            
            with col4:
                try:
                    total_outstanding = float(retailers_df['Outstanding'].sum())
                    st.metric("Total Outstanding", format_currency(total_outstanding))
                except:
                    st.metric("Total Outstanding", "₹0.00")
            
            st.markdown("---")
            
            # Retailers by area
            st.subheader("Retailers by Area")
            area_dist = retailers_df['Area'].value_counts().reset_index()
            area_dist.columns = ['Area', 'Count']
            
            import plotly.express as px
            fig = px.bar(area_dist, x='Area', y='Count', color_discrete_sequence=['#0066cc'])
            fig.update_layout(template='plotly_white', height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Outstanding by retailer
            st.subheader("Top Outstanding Retailers")
            top_outstanding = retailers_df.nlargest(10, 'Outstanding')[
                ['Name', 'Area', 'Outstanding', 'Preferred Product']
            ].copy()
            
            st.dataframe(
                top_outstanding.style.format({'Outstanding': '₹{:,.2f}'}),
                use_container_width=True,
                hide_index=True
            )


if __name__ == "__main__":
    show()
