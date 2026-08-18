from llm_client import call_llm

try:
    result = call_llm('Return only this JSON: {"status":"connected"}')
    print(result)
except Exception as e:
    print("ERROR:", type(e).__name__)
    print("MESSAGE:", e)