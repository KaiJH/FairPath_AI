import json
from app.services.openai_service import ask_llm

class PrivacyGuardian:
    def __init__(self):
        # 🚀 強化 Prompt：核心修改在於將「地理位置」列為最高優先級遮蔽項目，並強制保留原始換行結構。
        self.system_prompt = """
        You are the 'Privacy Guardian Agent'. 
        
        CRITICAL TASK: 
        Perform a precision audit and MASKING of the input text to eliminate ALL Personally Identifiable Information (PII) and geographic bias triggers.
        
        1. MASKING RULES (Highest Priority):
           - ALL Geographic Locations: Mask City, State, Country, Zip Codes, and specific addresses (e.g., "San Francisco, CA" -> "[LOCATION]").
           - Names & Contacts: Full names, emails, phone numbers.
           - Specific Company Names: If requested or overly specific, mask them.

        2. CONTENT PRESERVATION:
           - Retain skills, job titles, education levels, and project descriptions.
           - IMPORTANT: You MUST preserve the original document's structural layout and LINE BREAKS. Sections like Summary, Experience, Education must remain on separate lines.

        3. BIAS RISK LOGIC (Formatting Rule):
           starts with 'Potential bias risks identified\\n',
           followed by a numbered list starting from (1) for each distinct risk,
           each point separated by a newline character (\\n).

        Output JSON: {"masked_content": "string with structure", "bias_risk_alert": "string formatted"}
        """

    def process(self, raw_text: str) -> dict:
        result = ask_llm(self.system_prompt, f"Raw Profile Text for audit: {raw_text}")
        try:
            return json.loads(result)
        except Exception as e:
            print(f"Privacy Guardian Error: {str(e)}")
            return {
                "masked_content": raw_text, 
                "bias_risk_alert": "Potential bias risks identified\\n(1) Data parsing error during audit."
            }