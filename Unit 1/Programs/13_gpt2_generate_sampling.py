
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

from transformers import GPT2LMHeadModel, GPT2Tokenizer

print("Downloading/loading GPT-2 model from Hugging Face Hub ...")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

prompt = "The future of technology is"
input_ids = tokenizer.encode(prompt, return_tensors="pt")

output = model.generate(input_ids, max_length=50, num_return_sequences=1, do_sample=True, top_k=50)
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

print(generated_text)
