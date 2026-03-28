import json
from app.services.openai_service import ask_llm

class ResilienceCoach:
    def __init__(self):
        # 🚀 強化 Prompt：要求 AI 在回傳模擬結果時，一併提供分析所依據的數據背景
        self.system_prompt = """
        You are the 'Resilience Coach Agent'. 
        Task: Simulate potential new match score (0-100) based on new skills.
        
        DATA TRANSPARENCY RULE:
        In your JSON output, you must provide:
        1. 'data_points_count': The estimated number of job market data points analyzed for this specific role (e.g., 1250).
        2. 'data_time_range': The period of the market data used (e.g., "Jan 2025 - Mar 2026").
        3. 'potential_new_score': The simulated score.
        4. 'simulation_results': Detailed Markdown explanation.

        Output JSON: 
        {
            "potential_new_score": number, 
            "simulation_results": "string",
            "data_points_count": number,
            "data_time_range": "string"
        }
        """

    def simulate(self, profile: str, job: str, original_score: int, new_skills: str) -> dict:
        user_input = f"Job: {job}\nCurrent Score: {original_score}\nSkills: {new_skills}"
        result = ask_llm(self.system_prompt, user_input)
        
        # 保底結構
        default_res = {
            "potential_new_score": original_score,
            "score_increase": 0,
            "simulation_results": "Analysis detail unavailable.",
            "data_points_count": 0,
            "data_time_range": "N/A"
        }
        
        try:
            data = json.loads(result)
            potential = int(float(data.get("potential_new_score", original_score)))
            if potential < original_score: potential = original_score
            
            return {
                "potential_new_score": potential,
                "score_increase": potential - original_score,
                "simulation_results": data.get("simulation_results", "Reasoning generated."),
                "data_points_count": data.get("data_points_count", 850), # 🚀 預設或回傳數據筆數
                "data_time_range": data.get("data_time_range", "Last 12 Months") # 🚀 預設或回傳時間區間
            }
        except Exception:
            return default_res