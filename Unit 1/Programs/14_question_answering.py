
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

print("Downloading/loading QA model from Hugging Face Hub ...")
qa_pipeline = pipeline("question-answering")

context = 

question = "What is Python known for?"

result = qa_pipeline(question=question, context=context)
print("Answer:", result['answer'])
print("Score:", result['score'])
