"""
Program 8: Tokenization using BERT Tokenizer.
Downloads bert-base-uncased tokenizer files from Hugging Face on first run.
Run: python 08_bert_tokenizer.py
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

from transformers import BertTokenizer

print("Downloading/loading BERT tokenizer from Hugging Face Hub ...")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

sentence = "Natural Language Processing is fascinating."
tokens = tokenizer.tokenize(sentence)
token_ids = tokenizer.convert_tokens_to_ids(tokens)

print("Tokens:", tokens)
print("Token IDs:", token_ids)
