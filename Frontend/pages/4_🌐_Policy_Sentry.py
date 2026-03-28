import streamlit as st
import requests
import os

st.set_page_config(page_title="Policy Sentry", layout="wide", page_icon="🌐")
st.title("🌐 Policy Sentry - Market Weather Report")

if "market_report" not in st.session_state:
    st.session_state["market_report"] = None

st.write("Get the latest insights on H-1B policies and tech market trends.")

if st.button("Fetch Market Weather Report"):
    with st.spinner("Scanning market trends..."):
        try:
            base_url = os.getenv("BACKEND_URL", "http://fairpath-backend:8000/api/v1/analyze-career")
            update_url = base_url.replace("analyze-career", "market-update")
            
            # 🚀 修正：確保發送 Form Data 格式
            resp = requests.post(update_url, data={"context": "US Tech Job Market 2026"})
            
            if resp.status_code == 200:
                # 🚀 修正：使用 .get() 讀取 report，避免 KeyError
                st.session_state["market_report"] = resp.json().get("report", "No report content found.")
            else:
                st.error(f"Server Error: {resp.status_code}")
        except Exception as e:
            st.error(f"Connection Failed: {str(e)}")

if st.session_state["market_report"]:
    st.divider()
    st.subheader("📢 Market Outlook & Policy Update")
    st.markdown(st.session_state["market_report"])