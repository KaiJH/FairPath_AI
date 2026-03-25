import json
from app.services.openai_service import ask_llm

class ResilienceCoach:
    def __init__(self):
        # 強化格式與數學要求
        self.system_prompt = """
        You are the 'Resilience Coach Agent'. 
        Tasks:
        1. Simulate a potential new match score (0-100) after adding specific skills.
        2. Provide an 'Anxiety-Reduction Roadmap' as a CLEARLY formatted Markdown list. 
        3. FORMATTING: Each step MUST be on a NEW LINE starting with "1.", "2.", etc. (e.g., 1. Step\\n2. Step).
        
        Return a JSON object:
        {
            "potential_new_score": number, 
            "simulation_results": "string", 
            "anxiety_reduction_roadmap": "1. [Step Name]: [Description]\\n2. [Step Name]: [Description]"
        }
        """

    def simulate(self, current_profile: str, target_job: str, original_score: int, new_skills: str) -> dict:
        user_input = f"Profile: {current_profile}\\nJob: {target_job}\\nScore: {original_score}\\nSkills: {new_skills}"
        result = ask_llm(self.system_prompt, user_input)
        try:
            data = json.loads(result)
            # 🚀 數學校正：確保顯示的增量與總分絕對符合邏輯
            potential = int(float(data.get("potential_new_score", original_score)))
            if potential < original_score: potential = original_score
            
            return {
                "potential_new_score": potential,
                "score_increase": potential - original_score,
                "simulation_results": data.get("simulation_results", ""),
                "anxiety_reduction_roadmap": data.get("anxiety_reduction_roadmap", "No roadmap generated.")
            }
        except Exception:
            return {
                "potential_new_score": original_score, 
                "score_increase": 0, 
                "simulation_results": "Simulation failed.", 
                "anxiety_reduction_roadmap": "N/A"
            }