import pandas as pd
import numpy as np
import sklearn as sk
from sklearn.preprocessing import minmax_scale
from sklearn.tree import DecisionTreeClassifier


# find the proportion of each class in dataset
def find_Proportion(y):
    Res = [0,0,0,0]
    for i in range(0, len(y) ):
        for k in range(4):
            if y[i] == k:
                Res[k] = Res[k]+1
    S = sum(Res)
    for k in range(4):
        Res[k] = Res[k]/S
    return Res


Data = pd.read_csv("Data.csv")

X = np.array(Data[  ['Year', 'State_n','HC01_VC21', 'HC01_VC53', 'HC01_VC54',
       'HC01_VC55', 'HC01_VC56', 'HC01_VC57', 'HC01_VC161', 'HC01_VC172',
       'HC01_VC175', 'HC01_VC176', 'HC01_VC178', 'HC01_VC185', 'HC01_VC187',
       'HC01_VC193', 'HC01_VC196', 'HC01_VC198', 'HC01_VC203', 'HC01_VC204',
       'HC01_VC206', 'HC01_VC208', 'HC01_VC209'] ])
y = np.array(Data_2016['Rank'])

#training with all the data
cl = DecisionTreeClassifier(criterion='entropy',max_depth= 20, max_leaf_nodes = 200)
cl.fit(X, y)

#select the data of 2016
Data_2016 = Data[Data['Year'] == 2016]
Data_2016 = Data_2016.reset_index()
X_2016 = np.array(Data_2016[  ['Year', 'State_n','HC01_VC21', 'HC01_VC53', 'HC01_VC54',
       'HC01_VC55', 'HC01_VC56', 'HC01_VC57', 'HC01_VC161', 'HC01_VC172',
       'HC01_VC175', 'HC01_VC176', 'HC01_VC178', 'HC01_VC185', 'HC01_VC187',
       'HC01_VC193', 'HC01_VC196', 'HC01_VC198', 'HC01_VC203', 'HC01_VC204',
       'HC01_VC206', 'HC01_VC208', 'HC01_VC209'] ])
y_2016 = np.array(Data_2016['Rank'])

def strategy_modify(X,y,per_1, per_2):
    X_res = X
    for i in range(X.shape[0]):
        if y[i] == 3:
            for j in range(X.shape[1]):
                if j == 20:
                    print(j)
                    print(X_res[i][j])
                    X_res[i][j] = X_res[i][j]*(1- per_2)
                    print(X_res[i][j])
                if j == 13:
                    X_res[i][j] = X_res[i][j]*(1- per_2/2)
                if j == 14:
                    X_res[i][j] = X_res[i][j]*(1- per_2/3)
                if j == 10:
                    X_res[i][j] = X_res[i][j]*(1- per_2/4)
                if j == 3:
                    X_res[i][j] = X_res[i][j]*(1- per_2/5)
        elif y[i] == 2:
            for j in range(X.shape[1]):
                if j == 20:
                    X_res[i][j] = X_res[i][j]*(1- per_1)
                if j == 13:
                    X_res[i][j] = X_res[i][j]*(1- per_1/2)
                if j == 14:
                    X_res[i][j] = X_res[i][j]*(1- per_1/3)
                if j == 10:
                    X_res[i][j] = X_res[i][j]*(1- per_1/4)
                if j == 3:
                    X_res[i][j] = X_res[i][j]*(1- per_1/5)
    return X_res

X_2017 = strategy_modify(X_2016,y_2016,0.01,0.02)
y_2017 = cl.predict(X_2017)
P = find_proportion(y_2017)
P = pd.DataFrame(P)

P.columns = ['good', 'normal', 'critical', 'severe']
pd.DataFrame(P).to_csv("Predict.csv")