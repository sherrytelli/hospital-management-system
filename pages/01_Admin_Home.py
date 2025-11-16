import streamlit as st
from database import log_action, get_raw_patient_data

#authenticating user
if not st.session_state.authenticated or st.session_state.userrole != "admin":
    st.error("Access Denied: Admins only. ")
    st.stop()

#logging page viewed 
if st.session_state.userid:
    log_action(st.session_state.userid, st.session_state.userrole, 'Viewed Admin Dashboard')

st.title(f"Admin Dashboard - Welcome {st.session_state.username}")

#displaying raw patient data
st.header("Raw Patient Data")
got_data, data = get_raw_patient_data()
if got_data:
    st.dataframe(data, use_container_width=True)

else:
    st.info(data)