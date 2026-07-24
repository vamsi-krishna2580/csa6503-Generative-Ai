"""
Program 16: Compare the tokenization outputs of BERT and GPT-2.
Downloads bert-base-uncased and gpt2 tokenizers from Hugging Face on first run.
Run: python 16_compare_bert_gpt2_tokenization.py
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

from transformers import BertTokenizer, GPT2Tokenizer

print("Downloading/loading BERT and GPT-2 tokenizers from Hugging Face Hub ...")
bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

sentence = "Tokenization differs across transformer models."

bert_tokens = bert_tokenizer.tokenize(sentence)
gpt2_tokens = gpt2_tokenizer.tokenize(sentence)

print("BERT Tokens:", bert_tokens)
print("Number of BERT tokens:", len(bert_tokens))
print()
print("GPT-2 Tokens:", gpt2_tokens)
print("Number of GPT-2 tokens:", len(gpt2_tokens))
