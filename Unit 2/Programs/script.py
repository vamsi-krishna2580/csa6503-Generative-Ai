from pathlib import Path

# Ask for API Keys
gemini_key = input("Enter Gemini API Key: ").strip()
hf_key = input("Enter Hugging Face API Key (Press Enter to skip): ").strip()

# Create .env
env_content = f"""GEMINI_API_KEY={gemini_key}
HF_API_KEY={hf_key}
"""

Path(".env").write_text(env_content, encoding="utf-8")

print(".env created successfully.")

# Code to insert into Gemini programs
gemini_code = '''from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
'''

# Code to insert into Hugging Face program
hf_code = '''from dotenv import load_dotenv
import os

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
'''

# Update all Gemini experiments
gemini_files = [
    "Experiment06_OpenAI_TextGeneration.py",
    "Experiment07_Gemini_TextGeneration.py",
    "Experiment09_Python_Code_Generation.py",
    "Experiment10_SQL_Query_Generation.py",
    "Experiment11_Zero_One_Few_Shot.py",
    "Experiment12_Prompt_Evaluation.py",
]

for file in gemini_files:
    path = Path(file)
    if path.exists():
        text = path.read_text(encoding="utf-8")

        if "from dotenv import load_dotenv" not in text:
            text = text.replace(
                "from google import genai",
                "from google import genai\n" + gemini_code,
                1,
            )

        text = text.replace(
            'client = genai.Client(api_key="YOUR_GEMINI_API_KEY")',
            "client = genai.Client(api_key=GEMINI_API_KEY)"
        )

        path.write_text(text, encoding="utf-8")
        print(f"Updated {file}")

# Update Hugging Face experiment
hf_file = Path("Experiment08_HuggingFace_TextGeneration.py")

if hf_file.exists():
    text = hf_file.read_text(encoding="utf-8")

    if "from dotenv import load_dotenv" not in text:
        text = text.replace(
            "from huggingface_hub import InferenceClient",
            "from huggingface_hub import InferenceClient\n" + hf_code,
            1,
        )

    text = text.replace(
        'api_key="YOUR_HF_API_KEY"',
        "api_key=HF_API_KEY"
    )

    hf_file.write_text(text, encoding="utf-8")
    print(f"Updated {hf_file.name}")

print("\nAll programs updated successfully.")