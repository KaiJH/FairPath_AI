import streamlit as st
import os
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://fairpath-backend:8000/api/v1/analyze-career")

st.set_page_config(page_title="FairPath AI", layout="wide")
st.title("🚀 FairPath AI: Multi-Agent Navigation")

if "result" not in st.session_state:
    st.session_state["result"] = None
if "target_job" not in st.session_state:
    st.session_state["target_job"] = ""

with st.form("main_form"):
    job = st.text_input("Target Job Title", value=st.session_state["target_job"])
    resume = st.file_uploader("Upload Resume (PDF)", type="pdf")
    submit = st.form_submit_button("Start Analysis")

if submit and resume and job:
    st.session_state["target_job"] = job # 存入 session 供後續頁面使用
    with st.spinner("Analyzing..."):
        try:
            files = {"file": (resume.name, resume.getvalue(), "application/pdf")}
            data = {"target_job": job}
            resp = requests.post(BACKEND_URL, files=files, data=data)
            if resp.status_code == 200:
                st.session_state["result"] = resp.json()
                st.success("Analysis Complete! Go to 'Merit Report' in the sidebar.")
            else:
                st.error("Backend Error.")
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")