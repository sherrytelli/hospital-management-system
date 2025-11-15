import streamlit as st

if not st.session_state.authenticated or st.session_state.userrole != "admin":
    st.error("Access Denied: Admins only. ")
    st.stop()
    
st.title("Audit Log")