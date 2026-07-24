
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

from transformers import BertTokenizer, BertModel
import torch

print("Downloading/loading BERT model from Hugging Face Hub ...")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

sentence = "The bank approved the loan application."
inputs = tokenizer(sentence, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

cls_embedding = outputs.last_hidden_state[0][0]
print("CLS token embedding shape:", cls_embedding.shape)
print("First 10 values:", cls_embedding[:10])
