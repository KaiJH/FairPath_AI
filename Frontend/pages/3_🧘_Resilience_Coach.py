import streamlit as st
import requests
import os

st.set_page_config(page_title="Resilience Coach", layout="wide")
st.title("🧘 Resilience Coach - Skill Simulator")

# 1. 檢查 Phase 1 資料
if "result" not in st.session_state or not st.session_state["result"]:
    st.info("Please run analysis on the Home page first.")
    st.stop()

# 2. 初始化模擬結果的持久化狀態
if "sim_result" not in st.session_state:
    st.session_state["sim_result"] = None

res = st.session_state["result"]
orig_score = int(res["matching"]["match_score"])
masked_profile = res["privacy"]["masked_content"]
target_job = st.session_state.get("target_job", "the target role")

st.markdown(f"### Current Status: **{orig_score}** Score for **{target_job}**")

# 3. 輸入介面
with st.container():
    new_skills = st.text_input("Enter hypothetical new skills:", placeholder="e.g., AWS, Tableau, Python")
    btn = st.button("Run 'What-if' Simulation")

# 4. 點擊按鈕時更新持久化狀態
if btn:
    if not new_skills:
        st.warning("Please enter at least one skill.")
    else:
        with st.spinner("Calculating potential improvements..."):
            try:
                base_url = os.getenv("BACKEND_URL", "http://fairpath-backend:8000/api/v1/analyze-career")
                url = base_url.replace("analyze-career", "simulate-skills")
                
                payload = {
                    "profile": masked_profile,
                    "target_job": target_job,
                    "original_score": orig_score,
                    "new_skills": new_skills
                }
                
                resp = requests.post(url, data=payload)
                if resp.status_code == 200:
                    # 🚀 將結果鎖定在 session_state
                    st.session_state["sim_result"] = resp.json()
                    st.success("Simulation complete! Results will stay until you re-run.")
                else:
                    st.error("Backend error.")
            except Exception as e:
                st.error(f"Connection failed: {str(e)}")

# 5. 顯示持久化結果 (即使切換頁面回來也會存在)
if st.session_state["sim_result"]:
    sim = st.session_state["sim_result"]
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Original Score", orig_score)
    with col2:
        # 🚀 顯示校正後的 +Delta (綠色數值)
        st.metric("Potential New Score", sim["potential_new_score"], f"+{sim['score_increase']}")

    st.divider()
    
    st.subheader("🛠️ Your Anxiety-Reduction Roadmap")
    # 🚀 使用 markdown 渲染並處理換行
    st.markdown(sim["anxiety_reduction_roadmap"])
    
    with st.expander("Detailed Simulation Reasoning"):
        st.write(sim["simulation_results"])