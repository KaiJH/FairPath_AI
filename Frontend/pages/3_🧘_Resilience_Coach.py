import streamlit as st
import requests
import os

st.set_page_config(page_title="Resilience Coach", layout="wide", page_icon="🧘")
st.title("🧘 Resilience Coach - Skill Simulator")

# 1. 檢查基礎資料
if not st.session_state.get("result"):
    st.info("Please complete the analysis on the Home page first.")
    st.stop()

# 持久化狀態初始化
if "sim_result" not in st.session_state:
    st.session_state["sim_result"] = None

res = st.session_state["result"]
matching_data = res.get("matching", {})
orig_score = int(matching_data.get("match_score", 0))
masked_profile = res.get("privacy", {}).get("masked_content", "")
target_job = st.session_state.get("target_job", "the specified role")

st.markdown(f"### Current Status: **{orig_score}** Score for **{target_job}**")

# 2. 使用者輸入區
new_skills = st.text_input("Simulation Input (Skills to learn):", placeholder="e.g., Python, SQL, AWS Certification")

if st.button("Run 'What-if' Simulation"):
    if not new_skills:
        st.warning("Please enter at least one skill to simulate.")
    else:
        with st.spinner("Analyzing market data for simulation..."):
            try:
                base_url = os.getenv("BACKEND_URL", "http://fairpath-backend:8000/api/v1/analyze-career")
                sim_url = base_url.replace("analyze-career", "simulate-skills")
                
                payload = {
                    "profile": masked_profile,
                    "target_job": target_job,
                    "original_score": orig_score,
                    "new_skills": new_skills
                }
                resp = requests.post(sim_url, data=payload)
                if resp.status_code == 200:
                    st.session_state["sim_result"] = resp.json()
                else:
                    st.error("Backend error during simulation.")
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")

# 3. 呈現結果 (包含數據背景資訊)
if st.session_state["sim_result"]:
    sim = st.session_state["sim_result"]
    st.divider()
    
    # 🚀 新增：數據透明度資訊列 (呈現數據筆數與時間區間)
    col_a, col_b = st.columns(2)
    with col_a:
        st.caption(f"📊 **Data Points Analyzed:** {sim.get('data_points_count', 'N/A')} job postings")
    with col_b:
        st.caption(f"📅 **Data Time Range:** {sim.get('data_time_range', 'Last 12 Months')}")

    st.divider()
    
    # 分數對比區
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Original Match Score", orig_score)
    with c2:
        pot = sim.get("potential_new_score", orig_score)
        inc = sim.get("score_increase", 0)
        st.metric("Potential New Score", pot, f"+{inc}")

    st.divider()

    # 詳細模擬分析
    st.subheader("📝 Detailed Simulation Analysis")
    st.markdown(sim.get("simulation_results", "Analysis details unavailable."))
    
    st.info("The simulation above is calculated by comparing your profile against verified market demands within the specified time range.")