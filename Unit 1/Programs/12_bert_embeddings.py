"""
Program 12: Load a pre-trained BERT model and generate contextual embeddings.
Downloads bert-base-uncased model from Hugging Face on first run.
Run: python 12_bert_embeddings.py
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

from transformers import BertTokenizer, BertModel
import torch

print("Downloading/loading BERT model from Hugging Face Hub ...")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

sentence = "Machine learning enables computers to learn from data."
inputs = tokenizer(sentence, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

embeddings = outputs.last_hidden_state
print("Embedding shape:", embeddings.shape)
print("First token embedding vector (first 10 values):")
print(embeddings[0][0][:10])
