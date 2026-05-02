import pandas as pd
df = pd.read_csv('UFC.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year
print(f"Total fights: {len(df)}")
df_2010 = df[df['year'] >= 2010]
print(f"Fights >= 2010: {len(df_2010)}")
df_pruned = df[df['year'] < 2010]
print(f"Fights < 2010: {len(df_pruned)}")
