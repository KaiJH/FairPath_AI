import uvicorn
import io
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from dotenv import load_dotenv

# 🚀 關鍵步驟：必須在導入任何自定義代理人模組之前先載入環境變數
# 確保系統啟動時 OPENAI_API_KEY 已就緒 [cite: 16]
load_dotenv()

# 導入各個代理人實作 (Multi-Agent System) [cite: 1, 2]
from app.agents.privacy_guardian import PrivacyGuardian
from app.agents.career_architect import CareerArchitect
from app.agents.sponsorship_strategist import SponsorshipStrategist
from app.agents.resilience_coach import ResilienceCoach
from app.agents.policy_sentry import PolicySentry

app = FastAPI(
    title="FairPath AI - Multi-Agent Navigation System",
    description="Comprehensive backend support for international students in the US.",
    version="2.0.0"
)

# 設定 CORS 中間件，允許 Streamlit 前端跨域存取
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------
# 初始化代理人實例 (Agents Initialization)
# ----------------------------------------------------------------
# 1. 隱私守護者：負責去識別化與公平性預處理 [cite: 3, 4]
guardian = PrivacyGuardian()
# 2. 職涯建築師：負責語義匹配與技能落差分析 [cite: 8, 9]
architect = CareerArchitect()
# 3. 贊助策略家：建立贊助商務案例與 ROI 分析 [cite: 14, 16]
strategist = SponsorshipStrategist()
# 4. 韌性教練：進行 "What-if" 模擬與焦慮緩解 [cite: 20, 21]
coach = ResilienceCoach()
# 5. 政策哨兵：監控外部政策與市場趨勢 [cite: 26, 27]
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
    Phase 1 & 2 核心工作流：
    整合隱私遮蔽、技能匹配與贊助談判腳本生成。
    """
    try:
        # 讀取 PDF 內容並提取文本 [cite: 4]
        pdf_content = await file.read()
        reader = PdfReader(io.BytesIO(pdf_content))
        raw_text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])

        if not raw_text.strip():
            return {"error": "Failed to extract text from the PDF file."}

        # 步驟 1: Privacy Guardian - 生成遮蔽後的數位檔案 [cite: 7]
        privacy_result = guardian.process(raw_text)
        
        # 步驟 2: Career Architect - 使用脫敏資料進行技能匹配分析 [cite: 10, 13]
        matching_result = architect.analyze(
            privacy_result.get("masked_content", ""), 
            target_job
        )

        # 步驟 3: Sponsorship Strategist - 生成 ROI 敘事與談判劇本 [cite: 18, 19]
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
        return {"error": f"Analysis failed: {str(e)}"}

@app.post("/api/v1/simulate-skills")
async def simulate_skills(
    profile: str = Form(...), 
    target_job: str = Form(...),
    original_score: int = Form(...), # 🚀 新增原始分數參數
    new_skills: str = Form(...)
):
    """
    韌性教練模擬功能，確保分數提升邏輯正確。
    """
    try:
        # 執行 What-if 模擬
        simulation_result = coach.simulate(profile, target_job, original_score, new_skills)
        return simulation_result
    except Exception as e:
        print(f"Error in simulate_skills: {str(e)}")
        return {"error": str(e)}

@app.post("/api/v1/market-update")
async def market_update(context: str = Form("")):
    """
    Policy Sentry 監控功能：
    提供市場天氣報告，區分個人能力與外部宏觀因素 [cite: 28, 29]。
    """
    try:
        market_report = sentry.get_report(context)
        return market_report
    except Exception as e:
        print(f"Error in market_update: {str(e)}")
        return {"error": str(e)}

# ----------------------------------------------------------------
# Server Entry Point
# ----------------------------------------------------------------

if __name__ == "__main__":
    # 使用 0.0.0.0 確保在 Synology NAS 的 Docker 環境中可被存取 
    uvicorn.run(app, host="0.0.0.0", port=8000)