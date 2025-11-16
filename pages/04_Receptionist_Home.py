import streamlit as st
from database import log_action, anonymize_patient_data, add_patient

if not st.session_state.authenticated or st.session_state.userrole != "receptionist":
    st.error("Access Denied: Receptionists only. ")
    st.stop()
    
#logging page viewed 
if st.session_state.userid:
    log_action(st.session_state.userid, st.session_state.userrole, 'Viewed Receptionist Dashboard')
    
st.title(f"Receptionist View - Welcome {st.session_state.username}")

#form to add new patient
st.header("Add New Patient")
with st.form("add_patient_form", clear_on_submit=True, enter_to_submit=False):
    name = st.text_input("Full Name")
    contact = st.text_input("Contact Number")
    diagnosis = st.text_area("Diagnosis")
    submitted = st.form_submit_button("Add Patient")
    
    if submitted:
        if name and contact and diagnosis:
            inserted = anonymize_patient_data(add_patient(name, contact, diagnosis))
            if inserted:
                st.success(f"Patient '{name}' added successfully!")
                log_action(st.session_state.userid, st.session_state.userrole, 'Added Patient', f"Patient '{name}' added successfully")
            
            else:
                st.error("Failed to add patient.")
        
        else:
            missing_fields = []
            if not name:
                missing_fields.append("Full Name")
                
            if not contact:
                missing_fields.append("Contact Number")
                
            if not diagnosis:
                missing_fields.append("Diagnosis")
            
            st.error(f"Please fill in all required fields: {', '.join(missing_fields)}")