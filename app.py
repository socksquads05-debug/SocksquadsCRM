"""
SocksQuads CRM - Sales Dashboard
Main application file with login and navigation
"""

import logging
import traceback

import streamlit as st
from utils.helpers import AuthenticationManager, initialize_session_state
from app_pages import dashboard, salesman, retailers, reports, analytics


# Configure logging
logging.basicConfig(level=logging.INFO)

# Page configuration
st.set_page_config(
    page_title="SocksQuads CRM",
    page_icon="🧦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for branding
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #f0f2f6;
        }
        
        .stMetric {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .login-container {
            max-width: 400px;
            margin: 50px auto;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            background-color: white;
        }
    </style>
""", unsafe_allow_html=True)


def login_page():
    """Display login page."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.image("https://via.placeholder.com/200?text=SocksQuads", width=200)
        st.title("SocksQuads CRM")
        st.subheader("Sales Dashboard")
        st.markdown("---")
        
        with st.form("login_form"):
            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username"
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )
            
            submitted = st.form_submit_button(
                "🔓 Login",
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                success, user_data = AuthenticationManager.authenticate(username, password)
                
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_data = user_data
                    st.session_state.current_page = 'Dashboard'
                    st.success(f"Welcome, {user_data['name']}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")
        
        st.markdown("---")
        st.markdown("""
        ### Demo Credentials:
        
        **Admin Users:**
        - Username: `admin` | Password: `admin123`
        - Username: `owner` | Password: `owner123`
        
        **Salesmen:**
        - Username: `raj` | Password: `raj123`
        - Username: `priya` | Password: `priya123`
        - Username: `amit` | Password: `amit123`
        """)


def main_app():
    """Display main application."""
    # Sidebar
    with st.sidebar:
        st.title("🧦 SocksQuads CRM")
        
        # User info
        user_data = st.session_state.user_data
        st.write(f"**{user_data['name']}** ({user_data['role'].upper()})")
        st.markdown("---")
        
        # Navigation menu
        st.subheader("📋 Menu")
        
        if AuthenticationManager.is_admin(user_data):
            # Admin menu
            menu_options = [
                "Dashboard",
                "Daily Reports",
                "Retailers",
                "Reports",
                "Analytics"
            ]
        else:
            # Salesman menu
            menu_options = [
                "Daily Reports"
            ]
        
        current_page = st.radio(
            "Navigate to:",
            menu_options,
            key="menu_radio"
        )
        
        st.session_state.current_page = current_page
        
        st.markdown("---")
        
        # Logout button
        if st.button("🔓 Logout", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.session_state.current_page = 'Dashboard'
            st.rerun()
        
        st.markdown("---")
        st.markdown("**SocksQuads CRM v1.0**")
        st.markdown("*Powered by Streamlit*")
    
    # Main content
    page = st.session_state.current_page
    
    try:
        if page == "Dashboard":
            if not AuthenticationManager.is_admin(user_data):
                st.error("🔒 Access Denied! Only admins can view the dashboard.")
            else:
                dashboard.show()
        
        elif page == "Daily Reports":
            if AuthenticationManager.is_admin(user_data):
                st.info("You are viewing the daily sales reports section.")
                salesman.show()
            else:
                salesman.show()
        
        elif page == "Retailers":
            if not AuthenticationManager.is_admin(user_data):
                st.error("🔒 Access Denied! Only admins can manage retailers.")
            else:
                retailers.show()
        
        elif page == "Reports":
            if not AuthenticationManager.is_admin(user_data):
                st.error("🔒 Access Denied! Only admins can view reports.")
            else:
                reports.show()
        
        elif page == "Analytics":
            if not AuthenticationManager.is_admin(user_data):
                st.error("🔒 Access Denied! Only admins can view analytics.")
            else:
                analytics.show()
    
    except Exception as e:
        st.error(f"❌ Error loading page: {str(e)}")
        st.info("Please refresh the page or contact support.")


def main():
    """Main entry point."""
    try:
        # Initialize session state
        initialize_session_state()
        
        # Check authentication
        if not st.session_state.authenticated:
            login_page()
        else:
            main_app()
    except Exception as exc:
        logging.exception("Unhandled exception in app")
        st.title("⚠️ Application Error")
        st.error("A fatal error occurred while loading the application.")
        st.write("Please check the deployment logs and verify your Streamlit secrets configuration.")
        st.text(traceback.format_exc())


if __name__ == "__main__":
    main()
