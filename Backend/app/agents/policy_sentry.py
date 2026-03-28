import json
from app.services.openai_service import ask_llm

class PolicySentry:
    def __init__(self):
        self.system_prompt = """
        You are the 'Policy Sentry Agent'. Output MUST be JSON.
        Key: "report" (string, Markdown formatted).
        Analyze the current job market and policy trends for international students.
        """

    def get_report(self, context: str) -> dict:
        result = ask_llm(self.system_prompt, f"Context: {context}")
        try:
            data = json.loads(result)
            return {"report": data.get("report", "Market report unavailable.")}
        except Exception:
            return {"report": "Policy update error."}