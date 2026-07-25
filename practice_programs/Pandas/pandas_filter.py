import pandas as pd

data = {"Name": ["A", "B", "C", "D"], "Marks": [90, 70, 85, 60]}

df = pd.DataFrame(data)

print(df[df["Marks"] > 75])
