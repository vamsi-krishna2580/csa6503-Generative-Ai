"""
Program 15: Tokenize a sentence using the BERT tokenizer and display the
generated tokens and token IDs.
Downloads bert-base-uncased tokenizer from Hugging Face on first run.
Run: python 15_bert_tokens_display.py
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

sentence = "Transformers have revolutionized NLP tasks."
tokens = tokenizer.tokenize(sentence)
token_ids = tokenizer.convert_tokens_to_ids(tokens)

print("Sentence:", sentence)
print("Tokens:", tokens)
print("Token IDs:", token_ids)
