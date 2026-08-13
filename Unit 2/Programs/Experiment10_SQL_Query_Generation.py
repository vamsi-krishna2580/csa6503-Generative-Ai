from llm import ask

schema = """
Database: College

Student(
    StudentID INT,
    Name VARCHAR(50),
    Department VARCHAR(30)
)

Course(
    CourseID INT,
    CourseName VARCHAR(50)
)

Marks(
    StudentID INT,
    CourseID INT,
    Marks INT
)
"""

requirement = input("Enter the query requirement: ")

prompt = f"""
You are an SQL expert.

Database Schema:

{schema}

Requirement:
{requirement}

Instructions:
1. Generate only the SQL query.
2. Use ANSI SQL.
3. Use JOIN wherever necessary.
4. Optimize the query.
"""

print("\nGenerated SQL:\n")
print(ask(prompt))