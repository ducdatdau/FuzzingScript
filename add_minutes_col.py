import pandas as pd

df = pd.read_csv('plot_data', skipinitialspace=True)

df.rename(columns={'# unix_time': 'unix_time'}, inplace=True)

# Convert 'unix_time' to numeric
df['minutes_run'] = (df['unix_time'] - df['unix_time'].iloc[0]) / 60.0
df['minutes_run'] = df['minutes_run'].round(2)

cols = df.columns.tolist()
cols = cols[:1] + ['minutes_run'] + cols[1:-1]
df = df[cols]

df.to_csv('plot_data_with_minutes.csv', index=False)
print("plot_data_with_minutes.csv has been created")