from google import genai

client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

task = "Explain Artificial Intelligence."

prompts = [
    task,
    "Explain Artificial Intelligence in simple language with examples.",
    """Explain Artificial Intelligence.

Requirements:
1. Definition
2. Applications
3. Advantages
4. Disadvantages
5. Conclusion
"""
]

for i,prompt in enumerate(prompts,1):
    print(f"\nPrompt {i}")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    print(response.text)

print("""
Evaluation Criteria:
1. Relevance
2. Accuracy
3. Completeness
4. Clarity
5. Format Adherence

Best Prompt: Prompt 3
""")
