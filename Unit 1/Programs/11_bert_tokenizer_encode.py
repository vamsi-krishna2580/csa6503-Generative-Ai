"""
Program 11: Load the BERT tokenizer and tokenize a sentence.
Downloads bert-base-uncased tokenizer from Hugging Face on first run.
Run: python 11_bert_tokenizer_encode.py
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

sentence = "Deep learning models require large datasets."
encoded = tokenizer(sentence)

print("Tokens:", tokenizer.tokenize(sentence))
print("Encoded Input:", encoded)
