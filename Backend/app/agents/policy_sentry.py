import json
from app.services.openai_service import ask_llm

class PolicySentry:
    def __init__(self):
        # 規格書：監控政策漂移 (Policy Drift) [cite: 28]
        self.system_prompt = """
        You are the 'Policy Sentry Agent'.
        Tasks:
        1. Monitor real-time USCIS news and employment trends. [cite: 27]
        2. Reason if current setbacks are due to individual ability or external macro factors. [cite: 28]
        3. Output a 'Market Weather Report' and 'Plan B' strategies. [cite: 29]
        Output JSON: {"market_weather_report": "string", "plan_b_strategy": "string"}
        """

    def get_report(self, user_context: str) -> dict:
        result = ask_llm(self.system_prompt, f"Context: {user_context}")
        return json.loads(result)