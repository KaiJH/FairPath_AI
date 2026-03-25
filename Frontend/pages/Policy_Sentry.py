import streamlit as st
import requests

st.title("🌐 Policy Sentry - Market Update")
st.markdown("Monitoring the external environment to externalize stress factors.")

if st.button("Fetch Market Weather Report"):
    # resp = requests.post("http://localhost:8000/api/v1/market-update")
    resp = requests.post("http://fairpath-backend:8000/api/v1/market-update")
    data = resp.json()
    st.subheader("Market Weather Report")
    st.write(data["market_weather_report"])
    st.subheader("Plan B Risk Mitigation")
    st.warning(data["plan_b_strategy"])