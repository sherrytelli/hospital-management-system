import streamlit as st

if not st.session_state.authenticated or st.session_state.userrole != "doctor":
    st.error("Access Denied: Doctors only. ")
    st.stop()
    
st.title("Doctor View")