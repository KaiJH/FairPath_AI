import json
from app.services.openai_service import ask_llm

class CareerArchitect:
    def __init__(self):
        self.system_prompt = """
        You are the 'Career Architect Agent'. Output MUST be JSON.
        Keys: "match_score" (0-100), "skill_gap_list" (list), "match_analysis" (string).
        """

    def analyze(self, masked_profile: str, target_job: str) -> dict:
        user_input = f"Job: {target_job}\nProfile: {masked_profile}"
        result = ask_llm(self.system_prompt, user_input)
        
        try:
            data = json.loads(result)
            score = float(data.get("match_score", 0))
            
            # 🚀 修正：解決 0.72/100 的異常。如果 AI 給的是小數，自動轉為整數。
            if 0 < score <= 1:
                score = score * 100
            
            return {
                "match_score": int(score),
                "skill_gap_list": data.get("skill_gap_list", []),
                "match_analysis": data.get("match_analysis", "Detailed analysis generated.")
            }
        except Exception:
            return {"match_score": 0, "skill_gap_list": [], "match_analysis": "Error"}