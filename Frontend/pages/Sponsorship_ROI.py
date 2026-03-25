import streamlit as st

st.title("💰 Sponsorship Business Case")
if not st.session_state.get("result"):
    st.info("Run evaluation on Home page first.")
else:
    # 假設後端已整合 SponsorshipStrategist 的產出
    res = st.session_state["result"]["sponsorship"]
    st.metric("Sponsorship Confidence Index", f"{res['confidence_index']}/100")
    st.subheader("Your ROI Narrative")
    st.success(res["roi_narrative"])
    
    with st.expander("Negotiation Script: Interview Intro"):
        st.write(res["negotiation_scripts"]["intro"])
    with st.expander("Handling Objections"):
        st.write(res["negotiation_scripts"]["objection_handling"])