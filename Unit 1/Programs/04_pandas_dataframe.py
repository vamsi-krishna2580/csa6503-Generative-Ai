
import subprocess, sys

def ensure(pkg, import_name=None):
    import_name = import_name or pkg
    try:
        __import__(import_name)
    except ImportError:
        print(f"Installing {pkg} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])

ensure("pandas")

import pandas as pd

data = {
    "Student": ["Vamsi", "Anjali", "Ravi", "Priya", "Karthik"],
    "Grade": ["A", "B", "A", "C", "B"]
}

df = pd.DataFrame(data)
print(df)
