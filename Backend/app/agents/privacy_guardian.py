import json
from app.services.openai_service import ask_llm

class PrivacyGuardian:
    def __init__(self):
        self.system_prompt = """
        You are the 'Privacy Guardian Agent'. [cite: 3]
        Your task is to:
        1. Identify and mask PII (Name, gender, ethnicity, address) using tags like [NAME]. [cite: 5]
        2. Reason through context to rewrite nationality-specific descriptions into neutral terms. [cite: 6]
        3. Identify potential bias risks in the resume. 
        Output JSON: {"masked_content": "string", "bias_risk_alert": "string"} 
        """

    def process(self, raw_text: str) -> dict:
        result = ask_llm(self.system_prompt, raw_text)
        return json.loads(result)