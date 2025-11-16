import streamlit as st
from database import log_action, get_logs

if not st.session_state.authenticated or st.session_state.userrole != "admin":
    st.error("Access Denied: Admins only. ")
    st.stop()
    
    
#logging page viewed 
if st.session_state.userid:
    log_action(st.session_state.userid, st.session_state.userrole, 'Viewed Admin Logs Page')
    
st.title("Audit Log")

#displaying logs
got_data, data = get_logs()
if got_data:
    st.dataframe(data, use_container_width=True)

else:
    st.info(data)