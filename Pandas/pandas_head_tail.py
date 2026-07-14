import pandas as pd

data = {"Number": [1, 2, 3, 4, 5, 6]}

df = pd.DataFrame(data)

print("Head")
print(df.head())

print("Tail")
print(df.tail())
