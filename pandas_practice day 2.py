import pandas as pd 
df = pd.read_csv('crop_data.csv')
print(df.head(152))
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())
