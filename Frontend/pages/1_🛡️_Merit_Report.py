import streamlit as st

st.set_page_config(page_title="Merit Report", layout="wide", page_icon="🛡️")
st.title("🛡️ Merit & Privacy Analysis")

# 1. 檢查基礎資料是否存在
if not st.session_state.get("result"):
    st.info("Please complete the analysis on the Home page first.")
    st.stop()

# 數據防護讀取
res = st.session_state["result"]
matching_data = res.get("matching", {})
privacy_data = res.get("privacy", {})

col1, col2 = st.columns([1, 2])
with col1:
    # 顯示數值成績單
    score = matching_data.get("match_score", 0)
    st.metric("Merit Match Score", score)
    
    st.subheader("Skill Gaps")
    gaps = matching_data.get("skill_gap_list", [])
    for gap in gaps:
        st.error(f"- {gap}")
        
with col2:
    st.subheader("Privacy Protection")
    
    # 🚀 調整點 1：將 De-identified Profile 的排版風格改為對齊旁邊的 Skill Gaps (實心紅底、白色粗體字型)
    st.subheader("De-identified Profile") # 子標題
    
    masked_profile_text = privacy_data.get("masked_content", "No profile data.")
    
    # 使用 Markdown 配合 HTML/CSS，強制將內容放在固定的可捲動區域 (height: 300px, overflow-y: scroll)
    st.markdown(
        f"""
        <div style="background-color: #220088; color: white; font-weight: bold; padding: 15px; border-radius: 5px; height: 300px; overflow-y: scroll; font-family: sans-serif; white-space: pre-wrap; font-size: 14px;">
{masked_profile_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()
    
    # 🚀 調整點 2：還原 Screenshot 19.36.02 的紅色實心背景 Bias Risk 區塊
    
    st.subheader("Bias Risk") # 粗體子標題
    
    bias_risk_content = privacy_data.get("bias_risk_alert", "Potential bias risks identified\n(1) No specific risks analyzed.")
    
    # 使用 Markdown 配合 HTML/CSS 自定義渲染紅色實心背景區塊
    st.markdown(
        f"""
        <div style="background-color: #880000; color: white; font-weight: bold; padding: 15px; border-radius: 5px; height: 300px; overflow-y: scroll; font-family: sans-serif; white-space: pre-wrap; font-size: 14px;">
{bias_risk_content}
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()
st.subheader("AI Analysis")
st.info(matching_data.get("match_analysis", "No detailed analysis available."))