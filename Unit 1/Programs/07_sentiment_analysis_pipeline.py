"""
Program 7: Load a Pre-trained Transformer Model using Hugging Face and perform sentiment analysis.
Downloads distilbert-base-uncased-finetuned-sst-2-english from Hugging Face on first run.
Run: python 07_sentiment_analysis_pipeline.py
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

from transformers import pipeline

print("Downloading/loading model from Hugging Face Hub ...")
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

result = classifier("I really love how simple and powerful this library is!")
print(result)
