"""
SockSquads CRM - Sales Dashboard
Main application file with login and navigation
"""

import logging
import traceback

import streamlit as st
from utils.helpers import AuthenticationManager, initialize_session_state
from utils.theme import inject_theme, render_login_brand, render_sidebar_brand
from app_pages import dashboard, salesman, retailers, reports, analytics


# Configure logging
logging.basicConfig(level=logging.INFO)

# Page configuration
st.set_page_config(
    page_title="Socksquads CRM",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for branding
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #03132e, #071b40);
            color: #f7f5f2;
            background-attachment: fixed;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #061732, #071b40);
            color: #f7f5f2;
        }

        .block-container {
            background-color: rgba(255,255,255,0.94) !important;
            box-shadow: 0 16px 48px rgba(0, 0, 0, 0.09);
            border-radius: 24px;
            padding: 2rem 2rem 3rem;
        }

        .stMetric {
            background-color: rgba(255,255,255,0.98);
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.08);
        }

        .login-container {
            max-width: 440px;
            margin: 50px auto;
            padding: 32px;
            border-radius: 22px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.14);
            background-color: rgba(255,255,255,0.95);
        }

        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stTextArea>div>div>textarea,
        .stDateInput>div>div>input {
            background: #ffffff !important;
            color: #0e203b !important;
        }

        .stTextInput>div>div>input::placeholder,
        .stTextArea>div>div>textarea::placeholder,
        .stDateInput>div>div>input::placeholder {
            color: rgba(14, 32, 59, 0.4) !important;
        }

        .stButton>button {
            border-radius: 999px;
        }
    </style>
""", unsafe_allow_html=True)

inject_theme()


def login_page():
    """Display login page."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        render_login_brand()
        st.caption("Premium socks sales operations dashboard")
        
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
                "Log in",
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
                    st.error("Invalid username or password.")
        
        st.info("For access, please contact your Socksquads administrator. Login credentials are not shown here for security reasons.")


def main_app():
    """Display main application."""
    # Sidebar
    with st.sidebar:
        st.title("🧦 SockSquads CRM")
        
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
        st.markdown("**SockSquads CRM v1.0**")
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
