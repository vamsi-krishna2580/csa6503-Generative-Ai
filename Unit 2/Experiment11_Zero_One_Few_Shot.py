from google import genai

client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

task = "Write a Python function to check whether a number is prime."

prompts = {
    "Zero-shot": task,
    "One-shot": f"""
Example:
Input: Add two numbers
Output:
def add(a,b):
    return a+b

Now:
{task}
""",
    "Few-shot": f"""
Example 1:
Input: Add two numbers
Output:
def add(a,b):
    return a+b

Example 2:
Input: Find square
Output:
def square(x):
    return x*x

Now:
{task}
"""
}

for name, prompt in prompts.items():
    print("\n"+name)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    print(response.text)
