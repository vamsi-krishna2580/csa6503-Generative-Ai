"""
Program 18: Compare contextual embeddings generated for two semantically
similar sentences.
Downloads bert-base-uncased model from Hugging Face on first run.
Run: python 18_compare_embeddings_similarity.py
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
from torch.nn.functional import cosine_similarity

print("Downloading/loading BERT model from Hugging Face Hub ...")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

def get_embedding(sentence):
    inputs = tokenizer(sentence, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

sentence1 = "The weather is very pleasant today."
sentence2 = "Today the climate feels really nice."

emb1 = get_embedding(sentence1)
emb2 = get_embedding(sentence2)

similarity = cosine_similarity(emb1, emb2)
print(f"Sentence 1: {sentence1}")
print(f"Sentence 2: {sentence2}")
print("Cosine Similarity:", similarity.item())
