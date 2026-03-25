import streamlit as st
import requests

st.title("🧘 Resilience Coach - Skill Simulator")
st.markdown("Run 'What-if' simulations to see how new skills reduce uncertainty.")

if st.session_state.get("result"):
    masked_profile = st.session_state["result"]["privacy"]["masked_content"]
    new_skills = st.text_input("Enter hypothetical new skills (e.g., AWS, Docker, React)")
    
    if st.button("Simulate Impact"):
        with st.spinner("Simulating..."):
            # resp = requests.post("http://localhost:8000/api/v1/simulate-skills", 
            #                      data={"profile": masked_profile, "new_skills": new_skills})
            resp = requests.post("http://fairpath-backend:8000/api/v1/simulate-skills", 
                                 data={"profile": masked_profile, "new_skills": new_skills})
            data = resp.json()
            st.subheader("Anxiety-Reduction Roadmap")
            st.info(data["anxiety_reduction_roadmap"])
            st.write(data["simulation_results"])