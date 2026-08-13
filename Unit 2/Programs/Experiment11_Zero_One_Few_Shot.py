from llm import ask

task = input("Enter the task: ")

zero_shot = f"""
Task:
{task}
"""

one_shot = f"""
Example

Task:
Find factorial

Answer:

def factorial(n):
    if n==0:
        return 1
    return n*factorial(n-1)

Now perform this task:

{task}
"""

few_shot = f"""
Example 1

Task:
Find factorial

Answer:

def factorial(n):
    if n==0:
        return 1
    return n*factorial(n-1)

Example 2

Task:
Find Fibonacci

Answer:

def fibonacci(n):
    if n<=1:
        return n
    return fibonacci(n-1)+fibonacci(n-2)

Now perform this task:

{task}
"""

print("=" * 70)
print("ZERO-SHOT")
print("=" * 70)
zero_response = ask(zero_shot)
print(zero_response)

print("\n" + "=" * 70)
print("ONE-SHOT")
print("=" * 70)
one_response = ask(one_shot)
print(one_response)

print("\n" + "=" * 70)
print("FEW-SHOT")
print("=" * 70)
few_response = ask(few_shot)
print(few_response)

print("\n" + "=" * 70)
print("Comparison")
print("=" * 70)

print("""
Criteria

1. Relevance
2. Accuracy
3. Consistency
4. Completeness
5. Code Quality

Observation:
• Zero-shot provides a direct solution.
• One-shot follows the example style.
• Few-shot produces the most consistent and structured output.
""")