import streamlit as st

st.title("🛡️ Privacy Guardian & Career Architect Report")

if not st.session_state.get("result"):
    st.info("Please run analysis on the Home page first.")
else:
    res = st.session_state["result"]
    
    # 隱私報告 [cite: 7]
    st.subheader("1. Privacy Protection")
    st.warning(f"**Bias Risk Alert:** {res['privacy']['bias_risk_alert']}")
    st.text_area("Masked Profile (PII Removed)", res['privacy']['masked_content'], height=200)
    
    st.divider()
    
    # 職涯建築師報告 [cite: 13]
    st.subheader("2. Skill Alignment (Merit-Based)")
    # 🚀 修正：直接顯示整數分數，不加百分比
    st.metric("Merit Match Score", res['matching']['match_score'])
    
    st.write("**Match Analysis:**")
    st.info(res['matching']['match_analysis'])
    
    st.write("**Skill Gaps Identified:**")
    for gap in res['matching']['skill_gap_list']:
        st.error(f"- {gap}")