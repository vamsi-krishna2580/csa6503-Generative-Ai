from llm import ask

problem = input("Enter the computational problem: ")

prompt = f"""
You are an expert Python programmer.

Generate a complete Python program for the following problem.

Problem:
{problem}

Requirements:
1. Write clean Python code.
2. Add meaningful comments.
3. Explain the algorithm.
4. Mention time complexity.
5. Show sample input and output.
6. Follow Python best practices.
"""

print("Generating Python code...\n")
print(ask(prompt))