import streamlit as st
import os
import requests

# 🚀 修正重點：改為讀取環境變數，預設值僅供本機開發使用
# 在 Docker Compose 中，這會被設定為 http://fairpath-backend:8000/...
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1/analyze-career")

# 修復 Protobuf 衝突
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

st.set_page_config(page_title="FairPath AI", layout="wide")
st.title("🚀 FairPath AI: Multi-Agent Navigation")

if "result" not in st.session_state:
    st.session_state["result"] = None

with st.form("input_form"):
    st.subheader("Candidate Information")
    col1, col2 = st.columns(2)
    with col1:
        job = st.text_input("Target Job (e.g., Data Scientist)")
        comp = st.text_input("Target Company")
    with col2:
        resume = st.file_uploader("Upload Resume (PDF)", type="pdf")
        sentiment = st.text_area("Sponsorship Info (Optional)")
    
    submit = st.form_submit_button("Start Fair Evaluation")

if submit and resume and job:
    with st.spinner("Agents are de-biasing and analyzing your profile..."):
        try:
            files = {"file": (resume.name, resume.getvalue(), "application/pdf")}
            data = {
                "target_job": job,
                "company_name": comp,
                "sentiment_data": sentiment
            }
            
            # 🚀 使用動態載入的 BACKEND_URL
            resp = requests.post(BACKEND_URL, files=files, data=data, timeout=60)
            
            if resp.status_code == 200:
                st.session_state["result"] = resp.json()
                st.success("Analysis Complete! Please check the sub-pages in the sidebar.")
            else:
                st.error(f"Backend returned an error: {resp.status_code}")
        except Exception as e:
            st.error(f"Could not connect to backend at {BACKEND_URL}. Error: {str(e)}")

st.info("System Goal: Ensure international students are evaluated based on merit while building a strong ROI case.")