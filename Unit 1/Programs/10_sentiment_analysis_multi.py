
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
