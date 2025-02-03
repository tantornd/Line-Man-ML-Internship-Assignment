import pandas as pd
df = pd.read_parquet("data/request.parquet")
df.to_json("data/request.json", orient="records")
