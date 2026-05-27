import streamlit as st
import requests
import datetime

st.set_page_config(page_title="DevSecOps Triage Center", layout="wide")
st.title("🛡️ Autonomous Triage Control Room")

st.markdown("### Simulate a Production Crash")
with st.form("crash_simulator"):
    service = st.selectbox("Service", ["PaymentGateway", "AuthService", "DatabaseWorker"])
    error = st.text_input("Error Type", value="psycopg2.OperationalError")
    trace = st.text_area("Stack Trace", value='File "db.py", line 42, in connect\nconnection refused by host.')
    
    if st.form_submit_button("Trigger Mock Crash"):
        payload = {
            "service_name": service,
            "error_type": error,
            "stack_trace": trace,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        try:
            res = requests.post("http://127.0.0.1:8000/v1/triage/report", json=payload)
            
            if res.status_code == 200:
                data = res.json()
                
                # Safely check if the response is a dictionary before looking for "status"
                if isinstance(data, dict):
                    st.success(data.get("status", "Incident received successfully!"))
                else:
                    # If it is a list or something else, just print it directly so it doesn't crash
                    st.success(f"Incident Processed. API returned: {data}")
                    
                st.info("Check your FastAPI terminal to see the LangGraph agent processing the incident!")
            else:
                st.error(f"Server Error: {res.status_code} - {res.text}")
        except Exception as e:
            # This will now print the exact error if it fails again
            st.error(f"Connection Failed: {e}")