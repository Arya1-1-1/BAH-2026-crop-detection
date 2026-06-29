import pandas as pd 
df = pd.read_csv('crop_data.csv')
print(df.head(152))
print(df['crop_health_label'].value_counts())
df['soil_moisture_pct'] = df['soil_moisture_pct'].fillna(df['soil_moisture_pct'].mean())
df['rainfall_mm'] = df['rainfall_mm'].fillna(df['rainfall_mm'].mean())
df_encoded = pd.get_dummies(df,columns=['crop_type'])
X = df_encoded.drop(columns=['field_id','crop_health_label'])
Y = df_encoded['crop_health_label']

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=42)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train,Y_train)

Y_pred = model.predict(X_test)

from sklearn.metrics import accuracy_score
accuracy = accuracy_score (Y_test,Y_pred)
print("Accuracy:",accuracy)


