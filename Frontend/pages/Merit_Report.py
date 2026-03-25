import streamlit as st

st.title("🛡️ Privacy & Merit Analysis Report")

if not st.session_state.get("result"):
    st.info("Please upload your resume on the Home page first.")
else:
    res = st.session_state["result"]
    
    st.subheader("1. Privacy & Bias Check")
    st.warning(f"**Risk Alert:** {res['privacy']['bias_risk_alert']}") # 
    st.text_area("De-identified Profile", res['privacy']['masked_content'], height=200) # 
    
    st.divider()
    
    st.subheader("2. Skill Alignment (Merit-Based)")
    st.metric("Match Score", f"{res['matching']['match_score']}%") # 
    st.write(res['matching']['match_analysis']) # 
    
    st.subheader("Granular Skill Gaps")
    for gap in res['matching']['skill_gap_list']: # 
        st.error(f"Need to improve: {gap}")