import uvicorn
import io
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

from app.agents.privacy_guardian import PrivacyGuardian
from app.agents.career_architect import CareerArchitect
from app.agents.sponsorship_strategist import SponsorshipStrategist
from app.agents.resilience_coach import ResilienceCoach
from app.agents.policy_sentry import PolicySentry

app = FastAPI(title="FairPath AI Full System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化所有 Agent，確保功能完整
guardian = PrivacyGuardian()
architect = CareerArchitect()
strategist = SponsorshipStrategist()
coach = ResilienceCoach()
sentry = PolicySentry()

@app.post("/api/v1/analyze-career")
async def analyze_career(
    file: UploadFile = File(...), 
    target_job: str = Form(...),
    company_name: str = Form("Target Company"),
    sentiment_data: str = Form("General Market")
):
    try:
        pdf_content = await file.read()
        reader = PdfReader(io.BytesIO(pdf_content))
        raw_text = "".join([p.extract_text() for p in reader.pages if p.extract_text()])

        privacy = guardian.process(raw_text)
        matching = architect.analyze(privacy.get("masked_content", ""), target_job)
        
        # 產生贊助案例
        sponsorship = strategist.generate_case(
            matching.get("match_analysis", ""), 
            company_name, 
            sentiment_data
        )

        return {
            "privacy": privacy,
            "matching": matching,
            "sponsorship": sponsorship
        }
    except Exception as e:
        return {"error": str(e)}

# 🚀 補回 Entrypoint: 技能模擬 (Resilience Coach)
@app.post("/api/v1/simulate-skills")
async def simulate_skills(
    profile: str = Form(...), 
    target_job: str = Form(...),
    original_score: int = Form(...),
    new_skills: str = Form(...)
):
    return coach.simulate(profile, target_job, original_score, new_skills)

# 🚀 補回 Entrypoint: 市場更新 (Policy Sentry)
@app.post("/api/v1/market-update")
async def market_update(context: str = Form("General")):
    return sentry.get_report(context)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)