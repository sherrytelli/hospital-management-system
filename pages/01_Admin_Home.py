import streamlit as st
from database import log_action, get_raw_patient_data, anonymize_patient_data
from time import sleep

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
    st.dataframe(data, use_container_width=True, hide_index=True)

else:
    st.info(data)
    
#anonymizing patient data
st.header("Anonymize Patient Data")
patient_id_to_anon = st.number_input("Enter Patient ID to Anonymize", min_value=1, step=1)
if st.button("Trigger Anonymization for Patient ID"):
    if anonymize_patient_data(patient_id_to_anon):
        log_action(st.session_state.userid, st.session_state.userrole, 'Anonymized Patient Data', f'Patient ID: {patient_id_to_anon}')
        msg = st.empty()
        msg.success("Patient ID anonymized successfully.")
        sleep(2)
        msg.empty()
        st.rerun()
    else:
        msg = st.empty()
        msg.error("Failed to anonymize Patient ID.")
        sleep(2)
        msg.empty()