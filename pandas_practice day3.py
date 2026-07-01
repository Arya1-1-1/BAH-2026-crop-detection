import pandas as pd
df = pd.read_csv('crop_data.csv')  #read the data 
print(df.head(152))                 #read no. of columns and rows
print(df['crop_health_label'].value_counts())          #count the no. of values in the column of healthy,moderate and stressed
df['soil_moisture_pct'] = df['soil_moisture_pct'].fillna(df['soil_moisture_pct'].mean())    #this replaces the missing values in the column with 
df['rainfall_mm'] = df['rainfall_mm'].fillna(df['rainfall_mm'].mean())                       #with the mean of the column
df_encoded = pd.get_dummies(df,columns=['crop_type'])                                       #this turn crop type 0-1 
X = df_encoded.drop(columns=['field_id','crop_health_label'])                         #x= everything that model uses to predict the crop health 
Y = df_encoded['crop_health_label']                                                  #y = what we are trying to predict

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=42)   #this holds back 20% data on test 

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(random_state=42)                              #actual training step 
model.fit(X_train,Y_train)

Y_pred = model.predict(X_test)                          #it guesses the crop health based on the test data 

from sklearn.metrics import accuracy_score
accuracy = accuracy_score (Y_test,Y_pred)
print("Accuracy:",accuracy)                          #accuracy score is calculated by comparing the predicted values with the actual values 


