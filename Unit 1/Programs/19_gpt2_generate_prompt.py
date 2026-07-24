
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

prompt = "In the next ten years, artificial intelligence will"
result = generator(prompt, max_length=60, num_return_sequences=1, do_sample=True, temperature=0.8)

print(result[0]['generated_text'])
