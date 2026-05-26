import yaml
import streamlit as st
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
from logger import log_progress
import os
from dotenv import load_dotenv

load_dotenv()

def setup_auth(config_file="config.yaml"):
    """
    Sets up the authentication system using streamlit-authenticator.
    Returns:
        authenticator: The authenticator object.
        name: Name of logged in user (or None)
        authentication_status: Boolean/None status.
        username: Username of logged in user.
    """
    
    # Check if Auth is disabled via ENV (for local dev)
    if os.getenv("ENABLE_AUTH", "true").lower() == "false":
        return None, "Dev User", True, "dev"

    if not os.path.exists(config_file):
        # Create default config if not exists (In prod this should be injected or handled with secrets)
        create_default_config(config_file)
        
    with open(config_file) as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )
    
    # Render login widget
    try:
        results = authenticator.login()
        # Handle the tuple/variable return nature of different versions
        # Older versions return nothing, newer return tuple
    except Exception as e:
        st.error(f"Auth Error: {e}")
        
    return authenticator, st.session_state.get("name"), st.session_state.get("authentication_status"), st.session_state.get("username")

def create_default_config(filepath):
    """Creates a default config file with a default user (admin/admin) hashed."""
    # Note: In a real architecture, we would generate this hash securely.
    # The hash for 'admin' with stauth is roughly this (bcrypt)
    # Use stauth.Hasher(['admin']).generate() to get this.
    
    # We will generate a safe default one dynamically if needed, 
    # but for now we write a template. 
    # Ideally, we should pull from ENV to build this YAML in memory to avoid writing secrets to disk.
    
    # Let's try to build config from ENV instead of file for better security
    pass

def get_auth_config_from_env():
    """
    Constructs the auth config dictionary from Environment variables.
    This is best practice for Docker/Cloud deployments to avoid committing YAML secrets.
    """
    import streamlit_authenticator as stauth
    
    admin_user = os.getenv("APP_USERNAME", "admin")
    admin_pass = os.getenv("APP_PASSWORD", "admin")
    secret_key = os.getenv("APP_SECRET_KEY", "some_random_secret_key")
    
    # Hash the password on startup
    hashed_pass = stauth.Hasher([admin_pass]).generate()[0]
    
    config = {
        'credentials': {
            'usernames': {
                admin_user: {
                    'name': 'Admin User',
                    'password': hashed_pass,
                    'email': 'admin@example.com' # optional
                }
            }
        },
        'cookie': {
            'name': 'content_pipeline_auth',
            'key': secret_key,
            'expiry_days': 30
        },
        'pre-authorized': {
            'emails': []
        }
    }
    return config

def check_authentication():
    """
    Main entry point to check auth.
    Usage:
        if check_authentication():
            # show main app
    """
    if os.getenv("ENABLE_AUTH", "true").lower() == "false":
        return True

    config = get_auth_config_from_env()
    
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )

    name, authentication_status, username = authenticator.login('main')
    
    if authentication_status:
        # Show logout in sidebar
        authenticator.logout('Logout', 'sidebar')
        return True
    elif authentication_status is False:
        st.error('Username/password is incorrect')
        return False
    elif authentication_status is None:
        st.warning('Please enter your username and password')
        return False
        
    return False
