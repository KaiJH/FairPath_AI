import uvicorn
import io
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from dotenv import load_dotenv

# 🚀 關鍵步驟：必須在導入任何自定義模組（如 Agents）之前先載入環境變數
# 這樣才能確保各個 Agent 內部初始化時能讀取到 OPENAI_API_KEY
load_dotenv()

# 導入各個代理人模組 (依據你目前的資料夾結構)
from app.agents.privacy_guardian import PrivacyGuardian
from app.agents.career_architect import CareerArchitect
from app.agents.sponsorship_strategist import SponsorshipStrategist
from app.agents.resilience_coach import ResilienceCoach
from app.agents.policy_sentry import PolicySentry

# 初始化 FastAPI 應用程式
app = FastAPI(
    title="FairPath AI - Multi-Agent System",
    description="International Student Career Navigation System (Phase 1 & 2)",
    version="1.0.0"
)

# 設定跨域資源共享 (CORS)，讓 Streamlit 前端可以順利呼叫 API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 在開發環境中允許所有來源，部署時可調整為特定網址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------
# 初始化所有代理人實例
# ----------------------------------------------------------------
guardian = PrivacyGuardian()
architect = CareerArchitect()
strategist = SponsorshipStrategist()
coach = ResilienceCoach()
sentry = PolicySentry()

# ----------------------------------------------------------------
# API Endpoints
# ----------------------------------------------------------------

@app.post("/api/v1/analyze-career")
async def analyze_career(
    file: UploadFile = File(...), 
    target_job: str = Form(...),
    company_name: str = Form(""),
    sentiment_data: str = Form("")
):
    """
    主分析流程：
    1. 讀取並解析 PDF 履歷。
    2. Privacy Guardian: 進行去識別化處理。
    3. Career Architect: 進行技能匹配與缺口分析。
    4. Sponsorship Strategist: 建立贊助商務案例與 ROI 分析。
    """
    try:
        # 讀取上傳的 PDF 檔案
        pdf_content = await file.read()
        reader = PdfReader(io.BytesIO(pdf_content))
        raw_text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                raw_text += extracted

        if not raw_text.strip():
            return {"error": "Could not extract any text from the uploaded PDF."}

        # 步驟 1: 執行隱私守護者流程 (去識別化與偏見檢測)
        privacy_result = guardian.process(raw_text)
        
        # 步驟 2: 執行職涯建築師流程 (使用去識別化後的內容進行評估)
        matching_result = architect.analyze(
            privacy_result.get("masked_content", ""), 
            target_job
        )

        # 步驟 3: 執行贊助策略家流程 (產出 ROI 敘事與談判劇本)
        sponsorship_result = strategist.generate_case(
            matching_result.get("match_analysis", ""), 
            company_name, 
            sentiment_data
        )

        return {
            "privacy": privacy_result,
            "matching": matching_result,
            "sponsorship": sponsorship_result
        }
    except Exception as e:
        print(f"Error in analyze_career: {str(e)}")
        return {"error": f"Internal Server Error: {str(e)}"}

@app.post("/api/v1/simulate-skills")
async def simulate_skills(
    profile: str = Form(...), 
    new_skills: str = Form(...)
):
    """
    Resilience Coach 模擬功能：
    分析學習新技能後對匹配率與職涯確定性的影響。
    """
    try:
        simulation_result = coach.simulate(profile, new_skills)
        return simulation_result
    except Exception as e:
        print(f"Error in simulate_skills: {str(e)}")
        return {"error": str(e)}

@app.post("/api/v1/market-update")
async def market_update(context: str = Form("")):
    """
    Policy Sentry 監控功能：
    提供即時市場天氣預報與 Plan B 策略建議。
    """
    try:
        market_report = sentry.get_report(context)
        return market_report
    except Exception as e:
        print(f"Error in market_update: {str(e)}")
        return {"error": str(e)}

# ----------------------------------------------------------------
# 啟動伺服器
# ----------------------------------------------------------------

if __name__ == "__main__":
    # 使用 0.0.0.0 確保在 Synology NAS 的 Docker 環境中可以被外部存取
    uvicorn.run(app, host="0.0.0.0", port=8000)