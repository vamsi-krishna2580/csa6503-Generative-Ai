"""
Program 10: Load a pre-trained transformer model using the Hugging Face pipeline() API
and perform sentiment analysis.
Downloads distilbert-base-uncased-finetuned-sst-2-english from Hugging Face on first run.
Run: python 10_sentiment_analysis_multi.py
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
sentiment_pipeline = pipeline("sentiment-analysis")

sentences = [
    "This course is extremely helpful.",
    "I did not enjoy the workshop at all."
]

results = sentiment_pipeline(sentences)
for s, r in zip(sentences, results):
    print(f"Sentence: {s}\nResult: {r}\n")
