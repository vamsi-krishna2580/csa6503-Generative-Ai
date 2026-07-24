"""
Program 9: Generate text using a pre-trained GPT-2 model.
Downloads gpt2 model from Hugging Face on first run.
Run: python 09_gpt2_text_generation.py
"""
import subprocess, sys

def ensure(pkg, import_name=None):
    import_name = import_name or pkg
    try:
        __import__(import_name)
    except ImportError:
        print(f"Installing {pkg} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])

ensure("transformers")
ensure("torch")

from transformers import pipeline

print("Downloading/loading GPT-2 model from Hugging Face Hub ...")
generator = pipeline("text-generation", model="gpt2")

output = generator("Artificial Intelligence will", max_length=40, num_return_sequences=1)
print(output[0]['generated_text'])
