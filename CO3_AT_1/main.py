import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


# ============================================================
# Configuration
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

# Parameters used for generation
TEMPERATURE = 0.3
MAX_OUTPUT_TOKENS = 100
REQUEST_TIMEOUT_MS = 15000


# ============================================================
# Input validation
# ============================================================

def validate_student(student):
    """Validate student name, marks and attendance."""

    required_fields = [
        "name",
        "math",
        "science",
        "english",
        "attendance"
    ]

    # Check for missing fields
    for field in required_fields:
        if field not in student:
            raise ValueError(f"Missing required field: {field}")

    # Check student name
    if not isinstance(student["name"], str) or not student["name"].strip():
        raise ValueError("Student name cannot be empty.")

    # Validate subject marks
    subjects = ["math", "science", "english"]

    for subject in subjects:
        mark = student[subject]

        if not isinstance(mark, (int, float)):
            raise ValueError(f"{subject} mark must be a number.")

        if mark < 0 or mark > 100:
            raise ValueError(
                f"{subject} mark must be between 0 and 100."
            )

    # Validate attendance
    attendance = student["attendance"]

    if not isinstance(attendance, (int, float)):
        raise ValueError("Attendance must be a number.")

    if attendance < 0 or attendance > 100:
        raise ValueError("Attendance must be between 0 and 100.")


# ============================================================
# Gemini client
# ============================================================

def create_client():
    """Create and return the Gemini API client."""

    if not API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add it to the .env file."
        )

    return genai.Client(
        api_key=API_KEY,
        http_options=types.HttpOptions(
            timeout=REQUEST_TIMEOUT_MS
        )
    )


# ============================================================
# Prompt creation
# ============================================================

def create_prompt(student):
    """Create the prompt sent to Gemini."""

    return f"""
Generate a personalized school report-card comment.

Student information:
Name: {student["name"]}
Mathematics: {student["math"]}/100
Science: {student["science"]}/100
English: {student["english"]}/100
Attendance: {student["attendance"]}%

Requirements:
1. Write exactly TWO sentences.
2. Use a professional and supportive school-report tone.
3. Mention academic performance and attendance when relevant.
4. Identify areas where the student can improve.
5. If the student has failing marks, remain constructive and encouraging.
6. Never insult, shame, label, or negatively judge the student.
7. Do not include headings, bullet points, or explanations.
8. Return only the two-sentence report-card comment.
"""


# ============================================================
# Gemini API call
# ============================================================

def generate_comment(client, student):
    """Send student information to Gemini and return the comment."""

    prompt = create_prompt(student)

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=TEMPERATURE,
                max_output_tokens=MAX_OUTPUT_TOKENS,
                candidate_count=1
            )
        )

        comment = response.text.strip()

        if not comment:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return comment

    except Exception as error:
        error_text = str(error).lower()

        # Rate-limit / quota errors
        if (
            "429" in error_text
            or "rate limit" in error_text
            or "quota" in error_text
            or "resource exhausted" in error_text
        ):
            raise RuntimeError(
                "Gemini API rate limit or quota exceeded. "
                "Please try again later."
            )

        # Authentication errors
        if (
            "401" in error_text
            or "403" in error_text
            or "authentication" in error_text
            or "permission" in error_text
        ):
            raise RuntimeError(
                "Gemini API authentication/permission error. "
                "Check your API key."
            )

        # Timeout errors
        if (
            "timeout" in error_text
            or "timed out" in error_text
        ):
            raise RuntimeError(
                "Gemini API request timed out. "
                "Please check your internet connection and try again."
            )

        # Other API failures
        raise RuntimeError(
            f"Gemini API request failed: {error}"
        )


# ============================================================
# Process one student
# ============================================================

def process_student(client, student, number):
    """Validate a student and generate their report comment."""

    print("\n" + "=" * 60)
    print(f"STUDENT {number}")
    print("=" * 60)

    print(f"Name       : {student['name']}")
    print(f"Mathematics: {student['math']}/100")
    print(f"Science    : {student['science']}/100")
    print(f"English    : {student['english']}/100")
    print(f"Attendance : {student['attendance']}%")

    try:
        # Validate input
        validate_student(student)

        # Call Gemini
        comment = generate_comment(client, student)

        print("\nGenerated Report Comment:")
        print("-" * 60)
        print(comment)

    except ValueError as error:
        print(f"\nInput Error: {error}")

    except RuntimeError as error:
        print(f"\nError: {error}")


# ============================================================
# Main program
# ============================================================

def main():

    print("=" * 60)
    print("AI REPORT CARD COMMENT WRITER")
    print("=" * 60)

    try:
        client = create_client()
    except RuntimeError as error:
        print(f"\nConfiguration Error: {error}")
        return

    # --------------------------------------------------------
    # Test students required by the assessment
    # --------------------------------------------------------

    students = [
        {
            "name": "Rahul",
            "math": 85,
            "science": 90,
            "english": 88,
            "attendance": 96
        },
        {
            "name": "Priya",
            "math": 68,
            "science": 72,
            "english": 65,
            "attendance": 88
        },
        {
            # Failing-mark edge case
            "name": "Arjun",
            "math": 32,
            "science": 38,
            "english": 45,
            "attendance": 72
        }
    ]

    # Generate comments for all three students
    for number, student in enumerate(students, start=1):
        process_student(client, student, number)


# ============================================================
# Program entry point
# ============================================================

if __name__ == "__main__":
    main()