import pandas as pd

data = {"Name": ["A", "B", "C"], "Marks": [90, 80, 70]}

df = pd.DataFrame(data)

df.to_csv("students.csv", index=False)

print("CSV file created.")
