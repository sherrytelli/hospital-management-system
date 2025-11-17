import streamlit as st
from database import log_action, get_logs
import pandas as pd

if not st.session_state.authenticated or st.session_state.userrole != "admin":
    st.error("Access Denied: Admins only. ")
    st.stop()
    
    
#logging page viewed 
if st.session_state.userid:
    log_action(st.session_state.userid, st.session_state.userrole, 'Viewed Admin Logs Page')
    
st.title("Integrity Audit Log")

#displaying logs
got_data, data = get_logs()
if got_data:
    st.header("Complete Audit Log")
    st.dataframe(data, use_container_width=True, hide_index=True)
    
    #displaying graph
    st.header("Activity Overview")
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data['date'] = data['timestamp'].dt.date
    activity_by_date_role = data.groupby(['date', 'role']).size().reset_index(name='count')
    activity_by_date_role = activity_by_date_role.pivot(index='date', columns='role', values='count').fillna(0)
    if not activity_by_date_role.empty:
        st.bar_chart(activity_by_date_role, width="content", height=400)
        
    else:
        st.info("Not enough log data to generate activity chart.")

else:
    st.info(data)