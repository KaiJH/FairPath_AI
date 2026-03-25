import requests
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1/analyze-career")

def call_full_analysis(file, target_job, company_name, sentiment_data):
    """
    呼叫後端 FastAPI 進行完整分析，並將結果存入 session_state
    """
    try:
        files = {"file": (file.name, file.getvalue(), "application/pdf")}
        data = {
            "target_job": target_job,
            "company_name": company_name,
            "sentiment_data": sentiment_data
        }
        
        response = requests.post(API_URL, files=files, data=data)
        response.raise_for_status()
        
        # 將結果存入 session_state 供各個 Page 使用
        st.session_state["analysis_result"] = response.json()
        return True
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return False