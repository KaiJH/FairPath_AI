import json
from app.services.openai_service import ask_llm

class SponsorshipStrategist:
    def __init__(self):
        # 規格書：槓桿私有數據建立贊助商業案例 
        self.system_prompt = """
        You are the 'Sponsorship Strategist Agent'.
        Tasks:
        1. Leverage data to build a 'Sponsorship Business Case' for international students. 
        2. Calculate the ROI: Analyze how the student's analytical value ($X) outweighs the cost of sponsorship ($Y). [cite: 18]
        3. Autonomously generate negotiation scripts to handle visa objections. [cite: 19]
        Output JSON: {
            "confidence_index": number, 
            "roi_narrative": "string", 
            "negotiation_scripts": {"intro": "string", "objection_handling": "string"}
        }
        """

    def generate_case(self, skill_analysis: str, company_name: str, sentiment: str) -> dict:
        user_input = f"Skills: {skill_analysis}\nTarget Company: {company_name}\nSponsorship Sentiment: {sentiment}"
        result = ask_llm(self.system_prompt, user_input)
        return json.loads(result)