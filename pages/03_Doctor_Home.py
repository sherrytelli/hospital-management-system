import streamlit as st
from database import log_action, get_anon_patient_data

if not st.session_state.authenticated or st.session_state.userrole != "doctor":
    st.error("Access Denied: Doctors only. ")
    st.stop()
    
#logging page viewed 
if st.session_state.userid:
    log_action(st.session_state.userid, st.session_state.userrole, 'Viewed Doctor Dashboard')
    
st.title(f"Doctor View - Welcome {st.session_state.username}")

#displaying anonymized patient data
st.header("Patient Data")
got_data, data = get_anon_patient_data()
if got_data:
    st.dataframe(data, use_container_width=True)
    
else:
    st.info(data)