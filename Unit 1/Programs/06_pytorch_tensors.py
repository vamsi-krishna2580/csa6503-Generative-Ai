"""
Program 6: Create tensors using PyTorch and perform basic mathematical operations.
Run: python 06_pytorch_tensors.py
"""
import subprocess, sys

def ensure(pkg, import_name=None):
    import_name = import_name or pkg
    try:
        __import__(import_name)
    except ImportError:
        print(f"Installing {pkg} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])

ensure("torch")

import torch

a = torch.tensor([1, 2, 3])
b = torch.tensor([4, 5, 6])

print("Tensor a:", a)
print("Tensor b:", b)
print("Addition:", a + b)
print("Subtraction:", a - b)
print("Multiplication:", a * b)
print("Division:", a / b)
print("Dot Product:", torch.dot(a, b))

m = torch.arange(1, 10).reshape(3, 3)
print("Matrix:\n", m)
print("Matrix Transpose:\n", m.T)
