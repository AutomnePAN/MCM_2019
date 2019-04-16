import pandas as pd
import numpy as np
import sklearn as sk
from sklearn.preprocessing import minmax_scale

def Listify_df(df, col_name):
    res = []
    for i in range(df.shape[0]):
        res.append(df[col_name][i])
    return res

def find_County_from_FIPS(FIPS):
    res = []
    for i in range(0, County.shape[0]):
        if County['FIPS_com'][i] == FIPS:
            res.append(County['County'][i])
            res.append(County['State'][i])
            return res


#Import data
Profile = []
for i in range(2010, 2017):
    Profile.append( pd.read_csv("Drug_Class_1/Network_final_%d.csv"%i) )

#Import factors data
Para = []
for i in range(2010, 2017):
    Para.append( pd.read_csv("ACS_%d_COOKED.csv"%(i-2000)) )


#establish the label data (class)
Label = []
for k in range(0, len(Profile)):
    for i in range(0, Profile[k].shape[0]):
        flag = 1
        Profile_1 = []
        Profile_1.append(Profile[k]['FIPS'][i])
        fips = Profile[k]['FIPS'][i]
        if flag == 1:
            C = find_County_from_FIPS(fips)
            Profile_1.append(C[0])
            Profile_1.append(C[1])
            if C[1] == 'OH':
                Profile_1.append(0)
            elif C[1] == 'PA':
                Profile_1.append(1)
            elif C[1] == 'KY':
                Profile_1.append(2)
            elif C[1] == 'VA':
                Profile_1.append(3)
            else:
                Profile_1.append(4)
            Profile_1.append(Profile[k]['Year'][i])
            Profile_1.append(Profile[k]['Degree'][i])
            Profile_1.append(Profile[k]['Drug_Use_Rank'][i] )
            Label.append(Profile_1)


#establish the factor data
P = []
for i in range(0, Label_df.shape[0]):
    fips = Label_df['FIPS'][i]
    year = Label_df['Year'][i]
    P_1  = []
    for j in range(0, Para[year - 2010].shape[0]):
        if Para[year - 2010]['FIPS'][j] == fips:
            for k in range(2, len(Factors)):
                P_1.append(Para[year - 2010][Factors[k]][j])
    if len(P_1) < 20:
        print(fips)
    P.append(P_1)    
factors = ['HC01_VC21', 'HC01_VC53', 'HC01_VC54',
       'HC01_VC55', 'HC01_VC56', 'HC01_VC57', 'HC01_VC161', 'HC01_VC172',
       'HC01_VC175', 'HC01_VC176', 'HC01_VC178', 'HC01_VC185', 'HC01_VC187',
       'HC01_VC193', 'HC01_VC196', 'HC01_VC198', 'HC01_VC203', 'HC01_VC204',
       'HC01_VC206', 'HC01_VC208', 'HC01_VC209']
F = pd.DataFrame(P, columns = factors)   

Data = pd.merge(Label_df, F, left_index= True, right_index= True, how='outer')

from sklearn.tree import DecisionTreeClassifier

#Vectorlization the data
X = np.array(Data[  ['Year', 'State_n','HC01_VC21', 'HC01_VC53', 'HC01_VC54',
       'HC01_VC55', 'HC01_VC56', 'HC01_VC57', 'HC01_VC161', 'HC01_VC172',
       'HC01_VC175', 'HC01_VC176', 'HC01_VC178', 'HC01_VC185', 'HC01_VC187',
       'HC01_VC193', 'HC01_VC196', 'HC01_VC198', 'HC01_VC203', 'HC01_VC204',
       'HC01_VC206', 'HC01_VC208', 'HC01_VC209'] ])

 y = np.array(Data['Rank'])

#Decision Tree training
cl = DecisionTreeClassifier(criterion='entropy',max_depth= 20, max_leaf_nodes = 200)
cl.fit(X, y)
FI = cl.feature_importances_
print(FI)


#print the tree
def print_decision_Tree(estimator):
    n_nodes = estimator.tree_.node_count
    children_left = estimator.tree_.children_left
    children_right = estimator.tree_.children_right
    feature = estimator.tree_.feature
    threshold = estimator.tree_.threshold
    node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
    is_leaves = np.zeros(shape=n_nodes, dtype=bool)
    stack = [(0, -1)]  # seed is the root node id and its parent depth
    while len(stack) > 0:
        node_id, parent_depth = stack.pop()
        node_depth[node_id] = parent_depth + 1
        # If we have a test node
        if (children_left[node_id] != children_right[node_id]):
            stack.append((children_left[node_id], parent_depth + 1))
            stack.append((children_right[node_id], parent_depth + 1))
        else:
            is_leaves[node_id] = True
    print("The binary tree structure has %s nodes and has "
          "the following tree structure:"
          % n_nodes)
    for i in range(n_nodes):
        if is_leaves[i]:
            print("%snode=%s leaf node." % (node_depth[i] * "\t", i))
        else:
            print("%snode=%s test node: go to node %s if X[:, %s] <= %s else to "
                  "node %s."
                  % (node_depth[i] * "\t",
                     i,
                     children_left[i],
                     feature[i],
                     threshold[i],
                     children_right[i],
                     ))
    print()
    node_indicator = estimator.decision_path(X_test)
    leave_id = estimator.apply(X_test)
    sample_id = 0
    node_index = node_indicator.indices[node_indicator.indptr[sample_id]:
                                        node_indicator.indptr[sample_id + 1]]
    print('Rules used to predict sample %s: ' % sample_id)
    for node_id in node_index:
        if leave_id[sample_id] == node_id:
            continue
        if (X_test[sample_id, feature[node_id]] <= threshold[node_id]):
            threshold_sign = "<="
        else:
            threshold_sign = ">"
        print("decision id node %s : (X_test[%s, %s] (= %s) %s %s)"
              % (node_id,
                 sample_id,
                 feature[node_id],
                 X_test[sample_id, feature[node_id]],
                 threshold_sign,
                 threshold[node_id]))
    # For a group of samples, we have the following common node.
    sample_ids = [0, 1]
    common_nodes = (node_indicator.toarray()[sample_ids].sum(axis=0) ==
                    len(sample_ids))
    common_node_id = np.arange(n_nodes)[common_nodes]
    print("\nThe following samples %s share the node %s in the tree"
          % (sample_ids, common_node_id))
    print("It is %s %% of all nodes." % (100 * len(common_node_id) / n_nodes,))

print_decision_Tree(cl)