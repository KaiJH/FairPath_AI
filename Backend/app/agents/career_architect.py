import json
from app.services.openai_service import ask_llm

class CareerArchitect:
    def __init__(self):
        # 強制要求回傳 0-100 的整數分數 [cite: 13]
        self.system_prompt = """
        You are the 'Career Architect Agent'[cite: 8]. 
        Tasks:
        1. Perform deep semantic matching between the Masked Profile and the Target Job[cite: 9, 11].
        2. Assign a 'match_score' as an INTEGER between 0 and 100 (e.g., 75, 85). Do NOT use decimals or percentages[cite: 12].
        3. Reason 'why' a mismatch exists[cite: 12].
        Output JSON: {"match_analysis": "string", "skill_gap_list": ["string"], "match_score": number}[cite: 13].
        """

    def analyze(self, masked_profile: str, target_job: str) -> dict:
        user_input = f"Profile: {masked_profile}\nTarget Job: {target_job}"
        result = ask_llm(self.system_prompt, user_input)
        try:
            data = json.loads(result)
            # 強制轉為整數確保前端顯示正常
            data["match_score"] = int(float(data.get("match_score", 0)))
            return data
        except Exception:
            return {"match_analysis": "Error", "skill_gap_list": [], "match_score": 0}