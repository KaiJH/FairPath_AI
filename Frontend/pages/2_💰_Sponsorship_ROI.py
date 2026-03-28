import streamlit as st

st.set_page_config(page_title="Sponsorship Business Case", layout="wide", page_icon="💰")
st.title("💰 Sponsorship Business Case")

# 1. 檢查基礎數據
if not st.session_state.get("result"):
    st.info("Please complete the analysis on the Home page first.")
    st.stop()

res = st.session_state["result"]
# 🚀 安全讀取贊助數據，避免 KeyError
sponsorship_data = res.get("sponsorship", {})

st.write("This customized business case is designed to help you negotiate H-1B sponsorship by focusing on your unique merit and ROI.")

st.divider()

# 🚀 修正點：改為讀取 business_case 而非 simulation_results
# 使用 .get() 確保即便 API 出錯，頁面也不會報紅字
case_content = sponsorship_data.get("business_case", "Generating business case details...")

if "error" in res:
    st.error(f"Analysis Error: {res['error']}")
else:
    st.subheader("📢 Your H-1B Sponsorship Value Proposition")
    # 渲染 Markdown 內容
    st.markdown(case_content)

st.divider()
st.caption("Tip: Use the data above during your final interview rounds to demonstrate how your immediate productivity offsets legal sponsorship costs.")