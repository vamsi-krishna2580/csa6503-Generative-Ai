
import subprocess, sys

def ensure(pkg, import_name=None):
    import_name = import_name or pkg
    try:
        __import__(import_name)
    except ImportError:
        print(f"Installing {pkg} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])

for pkg, imp in [("numpy", "numpy"), ("pandas", "pandas"), ("matplotlib", "matplotlib"),
                 ("scikit-learn", "sklearn"), ("torch", "torch"), ("transformers", "transformers")]:
    ensure(pkg, imp)

import numpy, pandas, matplotlib, sklearn

try:
    import torch
    torch_v = torch.__version__
except ImportError:
    torch_v = "Not installed"

try:
    import tensorflow as tf
    tf_v = tf.__version__
except ImportError:
    tf_v = "Not installed"

try:
    import transformers
    tr_v = transformers.__version__
except ImportError:
    tr_v = "Not installed"

print("NumPy:", numpy.__version__)
print("Pandas:", pandas.__version__)
print("Matplotlib:", matplotlib.__version__)
print("Scikit-learn:", sklearn.__version__)
print("PyTorch:", torch_v)
print("TensorFlow:", tf_v)
print("Transformers:", tr_v)
