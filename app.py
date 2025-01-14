import streamlit as st
import sqlite3
import os

# Define the database connection
def get_db_connection():
    return sqlite3.connect("streets_assignment.db")

def local_css(file_name):
    """Load CSS styles from a local file."""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def authenticate(username, password):
    """Check if the username exists and the password matches."""
    if password != 'admin':
        return False
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_name FROM user_details WHERE user_name = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    return user is not None

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

def get_user_data(username):
    """Fetch user data from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT street_index FROM user_street_assignment WHERE user_id = (SELECT user_id FROM user_details WHERE user_name = ?)", (username,))
    streets = cursor.fetchall()

    cursor.execute("SELECT name, age, days_from_start FROM user_details WHERE user_name = ?", (username,))
    user_info = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) FROM street_mapping")
    total_streets = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM user_details")
    active_users = cursor.fetchone()[0]

    conn.close()

    map_html_file = f"data/{username}_map.html"
    num_streets_visited = len(streets)
    name, age, days_from_start = user_info

    percentage_visited = (num_streets_visited / total_streets) * 100 if total_streets else 0

    return map_html_file, num_streets_visited, total_streets, active_users, percentage_visited, name, age, days_from_start

def display_metrics(num_streets_visited, total_streets, active_users, percentage_visited):
    """Display metrics."""
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([2, 2, 2, 3])
    with col1:
        st.metric(label="Total Streets", value=str(total_streets))
    with col2:
        st.metric(label="Streets Visited", value=str(num_streets_visited))
    with col3:
        st.metric(label="Active Users", value=str(active_users))
    with col4:
        st.metric(label="Percentage of Streets Visited", value=f"{percentage_visited:.2f}%")
    st.markdown("---")

def display_profile(name, age, days_from_start):
    """Display user profile information."""
    st.markdown(f"### User Profile")
    st.write(f"**Name**: {name}")
    st.write(f"**Age**: {age}")
    st.write(f"**Membership Days**: {days_from_start}")

def display_map(html_file):
    """Display the map."""
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
            st.components.v1.html(html_content, height=600, scrolling=False)
    else:
        st.error("Map file not found. Please generate maps first.")

def sidebar_controls():
    """Manage sidebar login/logout."""
    st.sidebar.title("Login to Urban Footprints")
    if not st.session_state.get('logged_in'):
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=handle_login)
    else:
        st.button("Logout", on_click=handle_logout)

def display_footer():
    """Display a fixed footer."""
    st.markdown("""
        <footer>
            &copy; 2025 Urban Footprints. All rights reserved.
        </footer>
    """, unsafe_allow_html=True)

# Main app setup
st.set_page_config(page_title="Urban Footprints", layout="wide")
local_css("style.css")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

sidebar_controls()

if st.session_state.get('logged_in'):
    st.title("Urban Footprints - Interactive Dashboard")
    map_html_file, num_streets_visited, total_streets, active_users, percentage_visited, name, age, days_from_start = get_user_data(st.session_state['user'])

    # Display user profile
    display_profile(name, age, days_from_start)

    # Toggle to display metrics
    show_metrics = st.checkbox("Show Metrics", value=True)
    
    if show_metrics:
        display_metrics(num_streets_visited, total_streets, active_users, percentage_visited)
    
    display_map(map_html_file)
else:
    st.info("Please log in to access the dashboard.")

display_footer()
