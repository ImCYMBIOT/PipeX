# app/transform.py
import pandas as pd

def transform_data():
    print("Data transformed!")
    # Example transformation:
    df = pd.DataFrame({"A": [1, 2, 3]})
    df["B"] = df["A"] * 2
    print(df)
