"""
Program 2: Install Scikit-learn and print its version.
Run: python 02_sklearn_version.py
"""
import subprocess, sys

def ensure(pkg, import_name=None):
    import_name = import_name or pkg
    try:
        __import__(import_name)
    except ImportError:
        print(f"Installing {pkg} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])

ensure("scikit-learn", "sklearn")

import sklearn
print("Scikit-learn version:", sklearn.__version__)
