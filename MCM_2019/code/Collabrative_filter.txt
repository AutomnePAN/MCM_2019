import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale


class Cf():
    def __init__(self,lbd=0.01,itr=100,cls=3,alpha=0.3): 
        self.lbd=lbd
        self.itr=itr 
        self.cls=cls 
        self.alpha=alpha 
        self.cost=np.zeros(itr) 
        self.year=[] 
        self.feature=[]
        
    def fit(self,x): 
        self.year=np.random.rand(x.shape[1],self.cls) 
#         print(self.year)
        self.feature= np.random.rand(x.shape[0],self.cls)
#         print(self.feature)
        
        for i in range(self.itr): 
            self.cost[i]=self.cost_fun(self.year,self.feature,x) 
            print(self.cost[i])
            print(i)
            if i > 0:
                if(self.cost[i] > self.cost[i-1]< 0.001):
                    return
            for ny in range(self.year.shape[0]):
                for nf in range(self.feature.shape[0]):
#                     print(ny, nf)
                    self.year[ny,:] -= self.alpha * (np.dot(self.feature[nf,:].transpose(),self.year[ny,:]) - x[nf,ny]) * self.year[ny,:]
            for nf in range(self.feature.shape[0]):
                for ny in range(self.year.shape[0]):
#                     print(ny, nf)
                    self.feature[nf,:]-=self.alpha * np.dot( np.dot(self.feature[nf,:].transpose(),self.year[ny,:]) - x[nf,ny] , self.feature[nf,:])
        
        
                                                                 
    def cost_fun(self,year,feature,x):
        y = np.dot(feature,year.transpose())
#         print(y)
#         print(x)
#         print(y-x)
        Cost  = (y-x)**2
        cost=1/2*sum(sum(Cost))
#         print(Cost)
#         print(cost)
        return cost


def score_county_with_cf(year):
    name='%d'%year
    year = year
    ct=pd.read_csv('%s.csv'%name)
    ct_np=np.array(ct)[0:,1:]
    
    ct.columns = ['County', 'Propoxyphene', 'Morphine', 'Methadone', 'Heroin',
       'Hydromorphone', 'Oxycodone', 'Oxymorphone', 'Dextropropoxyphene',
       'Buprenorphine', 'Hydrocodone', 'Meperidine', 'Fentanyl',
       'Dihydromorphone', 'Methorphan', 'Codeine', 'Tramadol', 'Pethidine',
       'Dihydrocodeine', 'Opiates', 'Opium', 'Pentazocine', 'Alphaprodine',
       'Acetylcodeine', 'Thebaine', 'Butorphanol', 'Nalbuphine', 'ANPP',
       'Desmethylprodine ', 'Remifentanil', 'Mitragynine',
       'Acetyldihydrocodeine', 'Hydrocodeinone', 'MT-45', 'Levorphanol',
       'Acetyl fentanyl', 'Butyryl fentanyl', 'Furanyl fentanyl',
       'p-Fluorobutyryl fentanyl', 'cis-3-methylfentanyl', 'Valeryl fentanyl',
       'Carfentanil', 'Acryl fentanyl', 'U-47700', '3-Methylfentanyl',
       '4-Fluoroisobutyryl fentanyl', 'trans-3-Methylfentanyl',
       'p-methoxybutyryl fentanyl', 'Tetrahydrofuran fentanyl',
       'p-Fluorofentanyl', 'o-Fluorofentanyl', '3-Fluorofentanyl',
       'Fluorofentanyl', 'Fluoroisobutyryl fentanyl',
       'Fluorobutyryl fentanyl ', 'Furanyl/3-Furanyl fentanyl',
       'Cyclopropyl fentanyl', 'Methoxyacetyl fentanyl', 'Phenyl fentanyl',
       'Benzylfentanyl', 'U-48800', 'U-49900', 'Crotonyl fentanyl',
       '3,4-Methylenedioxy U-47700', 'U-51754',
       'Cyclopropyl/Crotonyl Fentanyl', 'Isobutyryl fentanyl',
       'Cyclopentyl fentanyl', '4-Methylfentanyl', 'Metazocine']
    County = Listify_DataFrame(ct, 'County')
    County_List = ct.columns
    
    max = 0
    for i in range(2, len(County_List)):
        if ct.describe()[County_List[i]]['max'] > max:
            max = ct.describe()[County_List[i]]['max']
    ct_np_sc = ct_np/max
    
    cf = Cf(itr = 200, alpha=0.3)
    cf.fit(ct_np_sc)
    Point_drug = np.sqrt(max)*cf.year
    Point_County = np.sqrt(max)*cf.feature
    
    Profile = []

    
     #Learning the scores of each county
     for i in range(0, Point_County.shape[0]):
        Profile_1 = []
        Profile_1.append(County[i])
        Profile_1.append(year)
        for j in range(0, Point_County.shape[1]):
            Profile_1.append(Point_County[i][j])
        Profile.append(Profile_1)
    Profile = pd.DataFrame(Profile)
    Profile.columns = ['FIPS', 'Year', 'Score_County_1', 'Score_County_2', 'Score_County_3']
    pd.DataFrame(Profile).to_csv("Profile_County_%d.csv"%year)
    
    Profile = []

    Learning the scores of each drug
    for i in range(0, Point_drug.shape[0]):
        Profile_1 = []
        Profile_1.append(Drug_List[i])
        Profile_1.append(year)
        for j in range(0, Point_drug.shape[1]):
            Profile_1.append(Point_drug[i][j])
        Profile.append(Profile_1)
    Profile = pd.DataFrame(Profile)
    Profile.columns = ['Drug', 'Year', 'Score_Drug_1', 'Score_Drug_2', 'Score_Drug_3']
    pd.DataFrame(Profile).to_csv("Profile_Drug_%d.csv"%year)


