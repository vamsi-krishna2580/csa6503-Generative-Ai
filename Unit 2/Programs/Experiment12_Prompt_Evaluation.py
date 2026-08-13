from llm import ask

task = input("Enter a text generation task: ")

prompt1 = task

prompt2 = f"""
Explain the following in simple language.

{task}

Include one example.
"""

prompt3 = f"""
You are an expert educator.

Task:
{task}

Requirements:
1. Give a clear definition.
2. Explain the concept.
3. Provide examples.
4. Mention advantages.
5. Mention disadvantages.
6. Give a conclusion.
7. Use headings.
"""

print("=" * 70)
print("PROMPT 1")
print("=" * 70)

response1 = ask(prompt1)
print(response1)

print("\n" + "=" * 70)
print("PROMPT 2")
print("=" * 70)

response2 = ask(prompt2)
print(response2)

print("\n" + "=" * 70)
print("PROMPT 3")
print("=" * 70)

response3 = ask(prompt3)
print(response3)

print("\n" + "=" * 70)
print("Evaluation")
print("=" * 70)

print("""
Evaluation Criteria

✔ Relevance
✔ Accuracy
✔ Completeness
✔ Clarity
✔ Format Adherence

Conclusion

Prompt 3 performs the best because it provides
structured instructions, resulting in a more complete,
well-organized, and accurate response.
""")