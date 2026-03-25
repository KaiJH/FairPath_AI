import json
from app.services.openai_service import ask_llm

class CareerArchitect:
    def __init__(self):
        self.system_prompt = """
        You are the 'Career Architect Agent'. [cite: 8]
        Your task is to:
        1. Use O*NET standards to compare skills with the target job. [cite: 11]
        2. Reason 'why' a mismatch exists based on merit. 
        3. Output analysis and a gap list. 
        Output JSON: {"match_analysis": "string", "skill_gap_list": ["string"], "match_score": number} 
        """

    def analyze(self, masked_profile: str, target_job: str) -> dict:
        user_input = f"Profile: {masked_profile}\nTarget Job: {target_job}"
        result = ask_llm(self.system_prompt, user_input)
        return json.loads(result)