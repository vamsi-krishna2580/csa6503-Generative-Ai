from google import genai

client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

prompt = input("Enter Prompt: ")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print(response.text)
