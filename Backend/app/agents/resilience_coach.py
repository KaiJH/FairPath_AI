import json
from app.services.openai_service import ask_llm

class ResilienceCoach:
    def __init__(self):
        # 規格書：進行 "What-if" 模擬以緩解壓力 [cite: 21]
        self.system_prompt = """
        You are the 'Resilience Coach Agent'.
        Tasks:
        1. Conduct 'What-if' simulations: How would match scores increase if the user adds specific new skills (e.g., AWS, Python)? [cite: 21, 22]
        2. Provide an 'Anxiety-Reduction Roadmap' stating how closing specific gaps reduces uncertainty by X%. [cite: 25]
        Output JSON: {"simulation_results": "string", "anxiety_reduction_roadmap": "string"}
        """

    def simulate(self, current_profile: str, new_skills: str) -> dict:
        user_input = f"Current Profile: {current_profile}\nHypothetical Skills: {new_skills}"
        result = ask_llm(self.system_prompt, user_input)
        return json.loads(result)