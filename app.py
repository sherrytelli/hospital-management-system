import streamlit as st
from database import authenticate_user, log_action
from time import sleep

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    
if "userrole" not in st.session_state:
    st.session_state.userrole = None
    
if "userid" not in st.session_state:
    st.session_state.userid = None
    
if "username" not in st.session_state:
    st.session_state.username = None

def main():
    """the main function to run the application"""
    
    #creating pages
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
                    st.session_state.userrole = role
                    st.session_state.userid = user_id
                    st.session_state.username = username
                    log_action(user_id, role, 'Login', f'User {username} logged in successfully.')
                    st.success(f"Welcome, {username}! Redirecting...")
                    sleep(2)
                    st.rerun()
                    
                else:
                    st.error("Invalid username or password")

            else:
                st.error("Please enter both username and password")
    
    def logout():
        log_action(st.session_state.userid, st.session_state.userrole, f'User {st.session_state.username} logged out.')
        st.session_state.authenticated = False
        st.session_state.userrole = None
        st.session_state.userid = None
        st.session_state.username = None
        st.rerun()
        
    logout_page = st.Page(logout, title=f"Logout", icon=":material/logout:") 
    
    admin_home = st.Page("pages/01_Admin_Home.py", title="Admin Dashboard", icon=":material/dashboard:")
    admin_audit = st.Page("pages/02_Admin_Audit.py", title="Audit Log", icon=":material/list_alt:")
    
    doctor_home = st.Page("pages/03_Doctor_Home.py", title="Doctor View", icon=":material/medication:")
    
    receptionist_home = st.Page("pages/04_Receptionist_Home.py", title="Receptionist View", icon=":material/person_add:")
    
    #check authentication status
    if st.session_state.authenticated == False:
        pg = st.navigation([
            st.Page(login_page, title="Login", default=True)
        ], position="hidden") # Hide the navigation menu
        pg.run()
        return
    
    #user authenticated
    
    #creating side_panals for each page
    
    if st.session_state.userrole == "admin":
        pg = st.navigation({
            "Admin Panal": [admin_home, admin_audit],
            "Account": [logout_page]
        })
    
    elif st.session_state.userrole == "doctor":
        pg = st.navigation({
            "Doctor Panal": [doctor_home],
            "Account": [logout_page]
        })
        
    elif st.session_state.userrole == "receptionist":
        pg = st.navigation({
            "Receptionist Panal": [receptionist_home],
            "Account": [logout_page]
        })
    else:
        st.error("Role not recognized. Please log in again.")
        logout()
        return
    
    #run the created pages
    pg.run()
    
if __name__ == "__main__":
    main()