import json
from app.services.openai_service import ask_llm

class SponsorshipStrategist:
    def __init__(self):
        # 🚀 修正：明確定義產出的 Key 為 business_case
        self.system_prompt = """
        You are the 'Sponsorship Strategist Agent'. 
        Task: Create a professional business case for H-1B sponsorship.
        
        Output MUST be a valid JSON object:
        {
            "business_case": "string (Markdown formatted)"
        }
        """

    def generate_case(self, match_analysis: str, company_name: str, sentiment_data: str) -> dict:
        user_input = f"Analysis: {match_analysis}\nCompany: {company_name}\nMarket: {sentiment_data}"
        # 🚀 確保使用更新後的 ask_llm (gpt-4o)
        result = ask_llm(self.system_prompt, user_input)
        
        try:
            data = json.loads(result)
            return {"business_case": data.get("business_case", "Business case generation failed.")}
        except Exception:
            return {"business_case": "The AI could not generate the sponsorship case at this time."}