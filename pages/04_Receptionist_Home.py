import streamlit as st

if not st.session_state.authenticated or st.session_state.userrole != "receptionist":
    st.error("Access Denied: Receptionists only. ")
    st.stop()
    
st.title("Receptionist View")