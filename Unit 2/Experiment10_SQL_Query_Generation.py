from google import genai

client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

requirement = input("Enter Requirement: ")

schema = """
Database: College

Student(StudentID, Name, Department)
Marks(StudentID, Subject, Marks)
"""

prompt = f"""
Database Schema:
{schema}

Requirement:
{requirement}

Generate only the SQL query.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print(response.text)
