import os
import json
import httpx
from openai import OpenAI
from dotenv import load_dotenv

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing. Check your .env file.")
    # 明確禁用代理，解決 Anaconda 環境常見的 proxies 報錯
    http_client = httpx.Client(proxies=None)
    return OpenAI(api_key=api_key, http_client=http_client)

def ask_llm(system_prompt: str, user_content: str) -> str:
    """
    確保回傳值為字串，滿足 json.loads 的類型要求。
    """
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            response_format={ "type": "json_object" }
        )
        content = response.choices[0].message.content
        return content if content is not None else "{}"
    except Exception as e:
        print(f"LLM Communication Error: {str(e)}")
        return "{}"