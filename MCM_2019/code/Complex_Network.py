import pandas as pd
import numpy as np
import pyecharts as pc

#Definition of used functions

def Listify_df(df, col_name):
    res = []
    for i in range(df.shape[0]):
        res.append(df[col_name][i])
    return res

def Count_Neignbor_County(FIPS, distance):
    L = Listify_df(Distance, FIPS)
    count = 0
    for i in range(0, len(L)):
        if(L[i]<= distance):
            count = count + 1
    return count-1

def min_index_n(List, n):
    res = []
    size = 0
    for k in range(0, n):
        index = 0
        while(is_in_list(res, index) == 1):
            index = index + 1
        for i in range(0, len(List)):
            if List[i] <= List[index] :
                if (is_in_list(res, i) == 0):
                    index = i
        res.append(index)
        size = size +1
    return res

def Find_Nearest_n_County(FIPS, n):
    L = Listify_df(Distance, "%d"%FIPS)
    CL = min_index_n(L,n)
    res = []
    for i in range(len(CL)):
        res.append(Distance["FIPS"][CL[i]])
    return res

def find_County_index(FIPS):
    L = Listify_df(Profile_County[0], 'FIPS')
    for i in range(0, len(L)):
        if L[i] == FIPS:
            return i


Profile_County = []
for i in range(2010, 2018):
    Profile_County.append(pd.read_csv("Profile_County_%d.csv"%i))


#establish basic network

def establish_Network_year(year):
    P = Profile_County[year - 2010]
    #determine the degrees
    degree = []
    for i in range(0, P.shape[0]):
        degree.append(1+ int(P['Score_County_1'][i]))
    Degree = pd.DataFrame(degree, columns = ['Degree'])
    P_1 = pd.merge(P, Degree, left_index= True, right_index= True, how= 'outer')
    #determine the neighbor counties
    NC = []
    for i in range(0, P_1.shape[0]):
        nc = Count_Neignbor_County('%d'%P_1['FIPS'][i], 50000)
        NC.append(nc)
    NC = pd.DataFrame(NC, columns = ['Neignbor_County_Num'])
    P_2 = pd.merge(P_1, NC, left_index= True, right_index= True, how= 'outer')
    l1 = P_2['Degree'].describe()['25%']
    l2 = P_2['Degree'].describe()['50%'] 
    l3 = P_2['Degree'].describe()['75%']
    Condition_Drug_Use = []
    for i in range(P_2.shape[0]):
        if P_2['Degree'][i]>= l3:
            Condition_Drug_Use.append("Severe")
        elif P_2['Degree'][i] >= l2:
                Condition_Drug_Use.append("Critical")
        elif P_2['Degree'][i] >= l1:
            Condition_Drug_Use.append("Normal")
        else:
            Condition_Drug_Use.append("Good")        
    CDU = pd.DataFrame(Condition_Drug_Use, columns = ['Drug_Use_Condition'])
    P_3 = pd.merge(P_2, CDU, left_index= True, right_index= True, how= 'outer')
    Condition_Drug_Use = []
    for i in range(0, P_2.shape[0]):
        if P_2['Degree'][i]>= l3:
            Condition_Drug_Use.append(3)
        elif P_2['Degree'][i] >= l2:
            Condition_Drug_Use.append(2)
        elif P_2['Degree'][i] >= l1:
            Condition_Drug_Use.append(1)
        else:
            Condition_Drug_Use.append(0)
    CDU = pd.DataFrame(Condition_Drug_Use, columns = ['Drug_Use_Rank'])
    P_4 = pd.merge(P_3, CDU, left_index= True, right_index= True, how= 'outer')
    pd.DataFrame(P_4).to_csv("Drug_Class_1/Network_%d.csv"%year)
    return P_4

#find variation of the scores for each counties

def find_Network_tend(year):
    P = Network[year - 2010]
    P_next = Network[year - 2009]
    vary  = []
    for i in range(0, P.shape[0]):
        sta = P_next['Drug_Use_Rank'][i] - P['Drug_Use_Rank'][i]
        vary.append(sta)
    Vary = pd.DataFrame(vary, columns = ['Rank_Var'])
    P_1 = pd.merge(P, Vary, left_index= True, right_index= True, how= 'outer')
    vary  = []
    for i in range(0, P.shape[0]):
        sta = P_next['Degree'][i] - P['Degree'][i]
        vary.append(sta)
    Vary = pd.DataFrame(vary, columns = ['Degree_Var'])
    P_2 = pd.merge(P_1, Vary, left_index= True, right_index= True, how= 'outer')
    l1 = P_2['Degree_Var'].describe()['std']/20
    l2 = P_2['Degree_Var'].describe()['std']/10
    l3 = P_2['Degree_Var'].describe()['std']
    CDU = []
    for i in range(P_2.shape[0]):
        if  P_2['Degree_Var'][i] >= l3:
            CDU.append("Extremely_Increase")
        elif P_2['Degree_Var'][i] >= l2:
            CDU.append("Increase")
        elif P_2['Degree_Var'][i] >= l1:
            CDU.append("Lightly_Increase")
        elif P_2['Degree_Var'][i] >=  - l1:
            CDU.append("Stable")
        elif P_2['Degree_Var'][i] >=  - l2:
            CDU.append("Lightly_Decrease")
        elif P_2['Degree_Var'][i] >=  - l3:
            CDU.append("Decrease")
        else:
            CDU.append("Extremely_Decrease")
    CDU = pd.DataFrame(CDU, columns = ['Drug_Use_Var'])
    P_3 = pd.merge(P_2, CDU, left_index= True, right_index= True, how= 'outer')
    CDU = []
    for i in range(P_2.shape[0]):
        if  P_2['Degree_Var'][i] >= l3:
            CDU.append(3)
        elif P_2['Degree_Var'][i] >= l2:
            CDU.append(2)
        elif P_2['Degree_Var'][i] >= l1:
            CDU.append(1)
        elif P_2['Degree_Var'][i] >=  - l1:
            CDU.append(0)
        elif P_2['Degree_Var'][i] >=  - l2:
            CDU.append(-1)
        elif P_2['Degree_Var'][i] >=  - l3:
            CDU.append(-2)
        else:
            CDU.append(-3)
    CDU = pd.DataFrame(CDU, columns = ['Drug_Use_Var_n'])
    P_4 = pd.merge(P_3, CDU, left_index= True, right_index= True, how= 'outer')
    pd.DataFrame(P_4).to_csv("Drug_Class_1/Network_tend_%d.csv"%year)
    return P_4

#find the possible sources

def find_Potentiel_Source(year):
    threshold = 1
    _is_source_potentiel = []
    P = Network_tend[year-2010]
    for i in range(0, P.shape[0]):
        count = 0
        for j in range(0, len(NC[i])):
            index = find_County_index(NC[i][j])
            count = count + P['Drug_Use_Var_n'][index]/2
        potentiel = 100 * count / len(NC[i])
        _is_source_potentiel.append(potentiel)
    CDU = pd.DataFrame(_is_source_potentiel, columns = ['Source_Potentiel'])
    P_1 = pd.merge(P, CDU, left_index= True, right_index= True, how= 'outer')
    l1 = 0
    l2 = P_1['Source_Potentiel'].describe()['75%'] + P_1['Source_Potentiel'].describe()['std']
    _is_source = []
    source_count = 0
    for i in range(0, P_1.shape[0]):
        source_1 = []
        if P_1['Source_Potentiel'][i] > l2:
            source_1.append("Highly_Possible")
            source_1.append(2)
            source_count = source_count + 1
        elif P_1['Source_Potentiel'][i] > l1:
            source_1.append("Possible")
            source_1.append(1)
#             source_count = source_count + 0.5
        else:
            source_1.append("Not_Likely")
            source_1.append(0)
        _is_source.append(source_1)
    CDU = pd.DataFrame(_is_source, columns = ['is_Source','is_Source_Rank'])
    P_2 = pd.merge(P_1, CDU, left_index= True, right_index= True, how= 'outer')
    pd.DataFrame(P_2).to_csv("Drug_Class_1/Potentiel_Source_%d.csv"%year)    
    return source_count
    

#find sources in future

#determine if the node is surrounded by possible sources
def find_is_surrounded(year):
    P = pd.read_csv('Drug_Class_1/Potentiel_Source_%d.csv'%year)
    _is_surounded = []
    for i in range(0, P.shape[0]):
        count = 0
        for j in range(0, len(NC[i])):
            index = find_County_index(NC[i][j])
            if P['is_Source_Rank'][index] == 2:
                count = count + 1
            elif P['is_Source_Rank'][index] == 1:
                count = count + 0.5
        potentiel =100 * count / len(NC[i])
        _is_surounded.append(potentiel)
    CDU = pd.DataFrame(_is_surounded, columns = ['is_Surrounded'])
    P_1 = pd.merge(P, CDU, left_index= True, right_index= True, how= 'outer')
    pd.DataFrame(P_1).to_csv('Drug_Class_1/Surrounded_by_Source_%d.csv'%year)
    return P_1




Network = []
for year in range(2010, 2018):
    Network.append(establish_Network_year(year))

Network_tend = []
for year in range(2010, 2017):
    Network_tend.append(find_Network_tend(year))

for year in range(2010, 2017):
    find_Potentiel_Source(year)

Surrounded = []
for year in range(2010, 2017):
    Surrounded.append(find_is_surrounded(year))

for k in range(0, 7):
    Tomorrow_Source_Potentiel = []
    for i in range(0, Surrounded[k].shape[0]):
        Potentiel = []
        if Surrounded[k]['is_Surrounded'][i] > l2:
            Potentiel.append("Highly_Possible")
            Potentiel.append(2)
        elif Surrounded[k]['is_Surrounded'][i] > l1:
            Potentiel.append("Possible")
            Potentiel.append(1)
        else:
            Potentiel.append("Not_Likely")
            Potentiel.append(0)
        Tomorrow_Source_Potentiel.append(Potentiel)
    CDU = pd.DataFrame(Tomorrow_Source_Potentiel, columns = ['Future_Source_Potentiel','Future_Source_Rank'])
    P= pd.merge(Surrounded[k], CDU, left_index= True, right_index= True, how= 'outer')
    pd.DataFrame(P).to_csv("Drug_Class_1/Network_final_%d.csv"%(2010+k))