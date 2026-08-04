from google import genai

client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

problem = input("Enter Programming Problem: ")

prompt = f"""
You are an expert Python programmer.

Task:
{problem}

Requirements:
1. Write Python code.
2. Add comments.
3. Explain the logic.
4. Show sample input and output.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print(response.text)
