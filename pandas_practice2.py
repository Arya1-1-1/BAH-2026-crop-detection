import pandas as pd 
s = pd.Series(["prachi","aditi","shreya","aanchal"])
print(s)
data = {'colour':['red','blue','green','yellow'], 'value':[167,245,275,786]}
df= pd.DataFrame(data)
print(df)
df=pd.read_csv('sample.csv')
df.head()
df.head(10)
df.describe
