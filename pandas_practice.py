import pandas as pd 
s = pd.Series([10,20,30,40])
print(s)
data = {'crops': ['wheat', 'rice','maze'], 'yield kg' : [120,95,140]}
df = pd.DataFrame(data)
print(df)
df=pd.read_csv('sample.csv')
df.head()
df.head(10)
df.describe