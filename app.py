import streamlit as st
import hashlib
import psycopg2
from database import get_db_conn, verify_password

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    
if "user_role" not in st.session_state:
    st.session_state.user_role = None
    
if "user_name" not in st.session_state:
    st.session_state.user_role = None
    
#function to authenticate user
def authenticate_user(username, password):
    """function to authenticate user"""
    
    conn = get_db_conn()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, password, role FROM users WHERE username = %s;", (username,))
            result = cursor.fetchone()
        
            if result:
                user_id, stored_password, role = result
                if verify_password(stored_password, password):
                    return user_id, role
            return None, None
    
        except Exception as e:
            st.error(f"authentication error {e}")
            return None, None
        
        finally:
            conn.close()
            
    return None, None

def login_page():
    """login page function"""
    
    st.title("Hospital Management System - Login")
    
    username = st.text_input("username")
    password = st.text_input("password", type="password")
    
    if st.button("login"):
        if username and password:
            user_id, role = authenticate_user(username, password)
            if user_id:
                st.session_state.authenticated = True
                st.session_state.user_role = role
                st.session_state.user_name = username
                st.success(f"Welcome, {username}! Redirecting...")
                st.rerun()
                
            else:
                st.error("Invalid username or password")

        else:
            st.error("Please enter both username and password")
            
def main():
    """the main function to run the application"""
    
    #check authentication status
    if st.session_state.authenticated == False:
        login_page()
        return
    
        