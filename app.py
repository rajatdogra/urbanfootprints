import streamlit as st
import os

# Define user credentials and HTML file mapping
user_data = {f'user{i}': f'data/user{i}_map.html' for i in range(1, 11)}

def local_css(file_name):
    """Load CSS styles from a local file."""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def authenticate(username, password):
    """Check if the username and password are correct."""
    return username in user_data and password == 'admin'

def handle_login():
    """Handle user login."""
    username = st.session_state.username
    password = st.session_state.password
    if authenticate(username, password):
        st.session_state['logged_in'] = True
        st.session_state['user'] = username
    else:
        st.error("Incorrect username or password.")

def handle_logout():
    """Handle user logout."""
    st.session_state['logged_in'] = False
    st.session_state.pop('user', None)

def display_map(html_file):
    """Display the map and metrics if available."""
    show_metrics = st.sidebar.checkbox("Show Metrics", True)
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
            st.components.v1.html(html_content, height=600, scrolling=False)
        if show_metrics:
            st.metric(label="Total Streets", value="37,000")
            st.metric(label="Streets Visited", value="10,000", delta="270% increase")
            st.metric(label="Active Users", value="120", delta="-30 last week")
    else:
        st.error("Map file not found. Please generate maps first.")

def sidebar_controls():
    """Manage sidebar for login and logout."""
    st.sidebar.title("Login to Urban Footprints")
    if not st.session_state.get('logged_in'):
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=handle_login)
    else:
        st.button("Logout", on_click=handle_logout)

def display_user():
    """Display the username of the logged-in user."""
    if 'user' in st.session_state:
        st.title(f"Logged in as {st.session_state['user']}")

def display_footer():
    """Display copyright footer."""
    st.markdown("""
        <footer>
            <p>&copy; 2025 Urban Footprints. All rights reserved.</p>
        </footer>
        """, unsafe_allow_html=True)

# Main app setup
st.set_page_config(page_title="Urban Footprints", layout="wide")
local_css("style.css")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Manage sidebar and main area
sidebar_controls()

# Display user information
display_user()

if st.session_state.get('logged_in'):
    st.title("Urban Footprints - Your Interactive Map Dashboard")
    display_map(user_data[st.session_state['user']])
else:
    st.info("Please login to access the map dashboard.")

display_footer()
