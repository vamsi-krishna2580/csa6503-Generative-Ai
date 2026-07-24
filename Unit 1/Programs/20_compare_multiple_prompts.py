
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

prompts = [
    "The best way to learn programming is",
    "Climate change is a global issue because",
    "Space exploration will help humanity by"
]

for prompt in prompts:
    output = generator(prompt, max_length=40, num_return_sequences=1, do_sample=True)
    print(f"Prompt: {prompt}")
    print(f"Generated: {output[0]['generated_text']}")
    print("-" * 80)
