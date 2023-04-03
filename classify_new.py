import pandas as pd
import numpy as np
import copy
def trans(Floor):
    if Floor==81:
        Floor=-1
    if Floor==82:
        Floor=-3
    if Floor==83:
        Floor=-4
    if Floor==84:
        Floor=-5
    if Floor==85:
        Floor=-7
    return Floor

def classify(user_signal):
    k=user_signal['mac']
    v=user_signal['rss']
    df = pd.read_csv('D:/vscode/mode3-server/mac_home.csv')
    #transfer usersignal into user
    BF_list=[]
    BF_scores=[]
    for i in range(len(user_signal)):
       for j in range(len(df['BuFloor'])):
           if k[i] in df['mac'][j]:
               BF=df['BuFloor'][j]
               BF_score=v[i]+105
               if len(BF_list)==0:
                   BF_list.append(BF)
                   BF_scores.append(BF_score)
               elif BF not in BF_list:
                   BF_list.append(BF)
                   BF_scores.append(BF_score)
               else:
                   for b in range(len(BF_list)):
                       if BF_list[b]==BF:
                          BF_scores[b]+=BF_score
    #print(BF_list)
    #print(BF_scores)
    t = copy.deepcopy(BF_scores)
    # 求m个最大的数值及其索引
    max_index = []
    for _ in range(3):
        number = max(t)
        index = t.index(number)
        t[index] = 0
        max_index.append(index)
    t = []
    C1=BF_list[max_index[0]]
    C2=BF_list[max_index[1]]
    C3=BF_list[max_index[2]]
    F1=trans(int(C1[-2:]))
    F2=trans(int(C2[-2:]))
    F3=trans(int(C3[-2:]))
    F=round((F1+F2+F3)/3)
    return C1[:-2],F

#user={'3412980C660A':-84.35897435897436,'00F82C1998C0':-74.0,'7018A714B420':-79.0,'00F82C1BFEA2':-74.92105263157895}    
#3
#user={'603A7C5C57CF':-80.0,'30E171AEB365':-77.0,'68CAE43A6B80':-64.0,'68CAE43A6B83':-64.0,'342387C1AB7D':-80.0,'68CAE43A6B82':-64.0,'B4750E666A97':-76.0,'68CAE43A6B81':-65.0}
#5
#user={'80E01D206742':-79.0,'B0AA779596B1':-79.0,'7018A7114BC0':-65.33333333333333,'D8B190E7E2B1':-75.2,'1CE6C74BB8F1':-65.66666666666667,'3D8B190E7E271':-72.18181818181819,'1CE6C74BB8F0':-66.0,'D8B190E7E272':-73.33333333333333,'1CE6C74BB8F2':-67.0,'D8B190E7E270':-72.33333333333333,'80E01D206741':-80.0,'7018A710ED00':-69.0,'0019BE000550':-73.0,'A89D21969D81':-82.0,'D4AD716B8160':-60.0,'D8B190E7E2B0':-76.5,'D4AD716B9640':-48.5,'AA6BAD4562CC':-84.5}
#7
#user={'C07BBCF00AB3':-67.0,'C07BBCF00AB0':-67.66666666666667,'84B802DE43B3':-46.5,'C07BBCF00AB1':-68.66666666666667,'C07BBCF00AB2':-68.66666666666667,'C07BBCF02023':-31.5,'84B802DE43B0':-47.0,'84B802DE43B2':-48.0,'C07BBCF02020':-32.0,'C07BBCF02022':-31.5,'D8B190FD32A0':-80.0,'70DB986DB180':-59.5,'70DB986DB181':-59.0,'70DB986DB183':-59.5,'0019BE000550':-87.33333333333333,'F80BCB3B9060':-72.66666666666667,'F80BCB3B9061':-73.33333333333333,'F80BCB3B9063':-74.0,'00F82C194501':-73.0,'00F82C194503':-73.0,'0029C2E1E600':-75.0,'0029C2E1E603':-75.0,'00F82C194500':-73.0,'0029C2E1E601':-75.0,'C07BBC366C33':-79.0,'C07BBCF02021':-30.0,'7640BB7CA74C':-88.0,'C07BBC366C32':-77.0}
#BuildFloor=classify(user)   
#print(BuildFloor)        

f= open("D:/DDM/RA/Document/wifiScanner.dat", "r")
def modify(f):
    AP_location=[]
    j=0
    for x in f:
        j=j+1
        i=0
        for w in x.split("{"):
            w
            i=i+1
            du=[j]
            if i>1:
                du.append('\''+str(w[7:19])+'\'')
                du.append(int(w[27:30]))
                AP_location.append(du)
    user=pd.DataFrame(AP_location)
    user.columns=['id','mac','rss']
    return user
user=modify(f)
f.close()

user_classes=[]
j_0=0
for i in range(len(user['id'])-1):
    if user['id'][i+1] != user['id'][i]:
        j_1=i
        user_signal=user[j_0:j_1+1].reset_index()
        user_class=[user_signal['id'][0]]
        Build,Floor=classify(user_signal)
        user_class.append(Build)
        user_class.append(Floor)
        user_classes.append(user_class)
        j_0=i+1
    if i==len(user['id'])-2:
        j_1=i
        user_signal=user[j_0:j_1+1].reset_index()
        user_class=[user_signal['id'][0]]
        Build,Floor=classify(user_signal)
        user_class.append(Build)
        user_class.append(Floor)
        user_classes.append(user_class)
c=pd.DataFrame(user_classes)
c.column=['userid','build','floor']
print(c)
        
       

    
    


