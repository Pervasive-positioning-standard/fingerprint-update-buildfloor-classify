from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import math
import os
from scipy.optimize import minimize
import copy
import pandas as pd
class GPR:

    def __init__(self, optimize=True):
        self.is_fit = False
        self.train_X, self.train_y = None, None
        self.params = {"a": -70, "b": 20,'lap0':2500,'lap1':1600,'d':10,'sigma_n':40,'sigma_f':10}
        self.optimize = optimize
   
    def fit(self, X, y):
        # store train data
        self.train_X = np.asarray(X)
        self.train_y = np.asarray(y)

         # hyper parameters optimization
        def negative_log_likelihood_loss(params):
            self.params["d"],self.params["sigma_f"] ,self.params["sigma_n"]= params[0], params[1],params[2]
            Kff = self.kn(self.train_X, self.train_X) 
            Kyy = Kff + self.params["sigma_n"] * np.eye(len(self.train_X))
            return 0.5 * self.train_y.T.dot(np.linalg.inv(Kyy)).dot(self.train_y) + 0.5 * np.linalg.slogdet(Kyy)[1] + 0.5 * len(self.train_X) * np.log(2 * np.pi)
        def Square(params2):
            self.params["a"],self.params["b"] ,self.params["lap0"],self.params["lap1"]= params2[0], params2[1],params2[2],params2[3]
            E=0
            for i in range(len(self.train_X)):
                E+=(self.kernel2(self.train_X[i])-self.train_y[i])**2
            return E
        if self.optimize:
            res = minimize(negative_log_likelihood_loss, [self.params["d"], self.params["sigma_f"],self.params["sigma_n"]],
                   bounds=((1e-5, 1e5), (1e-3, 1e3),(1e-5,1e+5)),
                   method='L-BFGS-B')
            self.params["d"], self.params["sigma_f"],self.params["sigma_n"]= res.x[0], res.x[1],res.x[2]
            res2 = minimize(Square, [self.params["a"], self.params["b"],self.params["lap0"],self.params["lap1"]],
                   bounds=((-1e3, 1e3), (-1e3, 1e3),(1e+1,1e+4),(1e+1,1e+4)),
                   method='L-BFGS-B')
            self.params["a"], self.params["b"],self.params["lap0"],self.params["lap1"]= res2.x[0], res2.x[1],res2.x[2],res2.x[3]
        self.is_fit = True
    def predict(self, X):
        if not self.is_fit:
            print("GPR Model not fit yet.")
            return

        X = np.asarray(X)
        Kff = self.kn(self.train_X, self.train_X)  # (N, N)
        Kyy = self.kn(X, X)  # (k, k)
        Kfy = self.kn(self.train_X, X)  # (N, k)
        Km = self.kn2(X)
        Kff_inv = np.linalg.inv(Kff + (self.params['sigma_n'])**2 * np.eye(len(self.train_X)))  # (N, N)
        o=np.dot(Kfy.T,Kff_inv)
        k=self.kn2(self.train_X)
        minus=self.train_y-k
        mu = Km+np.dot(o,minus)
        cov = Kyy - Kfy.T.dot(Kff_inv).dot(Kfy)
        return mu, cov

    def kernel(self, x1, x2
               ):
        dist_matrix=np.dot((x1-x2).T,(x1-x2))
        return self.params["sigma_f"] ** 2 * np.exp(-0.5 / self.params["d"] ** 2 * dist_matrix)
    def kn(self,x1,x2):
        A=np.zeros((len(x1),len(x2)))
        for i in range(len(x1)):
            for j in range(len(x2)):
                A[i,j]=self.kernel(x1[i],x2[j])
        return A
    def kernel2(self, x1
               ):
        dis =   ((x1[0]-self.params['lap0'])**2+(x1[1]-self.params['lap1'])**2)**(1/2)
        return self.params["a"]+self.params['b']* math.log(dis,10)
    def kn2(self,x1):
        B=np.zeros(len(x1))
        for i in range(len(x1)):
            B[i]=self.kernel2(x1[i])
        B=B.reshape(-1,1)
        return B
def ap_inf(data,ap):
    X=[]
    Y=[]
    data_1=data[data.ap==ap].reset_index()
    for indexs in data_1.index:
        ap= data_1[['rp_0','rp_1']].loc[indexs].tolist()
        rva=data_1[['rss']].loc[indexs].tolist()
        X.append(ap) #
        Y.append(rva)
    return X,Y
def finger_ori(floor):
    dir_path = 'D:/vscode/mode3-server/fingerprint/'+floor+'/fingerprint.txt'
    #file_names = os.listdir(dir_path)
    f= open(dir_path, "r")
    AP_location=[]
    for x in f:
            i=0
            for w in x.split(" "):
                i=i+1
                if i>1:
                    j=0
                    du=copy.deepcopy(du1)
                    for y in w.split(','):
                        j=j+1
                        if j==1:
                            du.append(y)
                        if j==2:
                            du.append(float(y))
                    AP_location.append(du)
                else:
                    du1=[]
                    for y in w.split(','):
                        du1.append(float(y))
    data=pd.DataFrame(AP_location)
    data.columns=['rp_0','rp_1','ap','rss']
    f.close()
    return data
def model(da,floor,ap):
    data=finger_ori(floor)
    x,y=ap_inf(da,ap)
    X,Y=ap_inf(data,ap)
    le=len(x)
    tra=le//10
    train_X = x[:tra]
    train_Y = y[:tra]
    if len(X)>0:
        test_X=X
        test_Y=Y
    else:
        test_X=x
        test_Y=y
    gpr = GPR(optimize=True)
    gpr.fit(train_X, train_Y)
    mu_1,cov_1=gpr.predict(test_X)
    z_1=mu_1
    plt.plot(train_Y,'r',label='real')
    plt.plot(z_1,'b',label='predict')
    plt.legend()
    plt.show()
    z_1=np.array(z_1)
    test_Y=np.array(test_Y)
    Var=np.sum((z_1-test_Y)**2)/len(z_1)
    print(Var)
#update
    if any(data.ap==ap) is False:
        for i in da.index:
            da.iloc[i,3]=z_1[i]
        data=pd.concat([data, da])
        data=data.reset_index()
    else:
        j=0
        for i in data.index:
            if  data[['ap']].loc[i].tolist() == [ap]:
                data.iloc[i,3]=z_1[j]
                j=j+1
            if j==len(z_1):
                break
    dir_path = 'D:/vscode/mode3-server/fingerprint_update/'+floor+'/fingerprint.txt'
    #file_names = os.listdir(dir_path)
    fw= open(dir_path, "w")
    l=data.shape[0]
    rp=list(range(l))
    ap=list(range(l))
    rss=list(range(l))
    for i in data.index:
        if i==0:
            rp[i]=data[['rp_0','rp_1']].iloc[i] 
            ap[i]=data[['ap']].iloc[i].tolist() 
            rss[i]=data[['rss']].iloc[i].tolist()   
            fw.write(str(rp[i][0])+','+str(rp[i][1])+' '+str(ap[i][0])+','+str(rss[i][0])+' ')    # 将字符串写入文件中
        else:
            rp[i]=data[['rp_0','rp_1']].iloc[i]
            ap[i]=data[['ap']].iloc[i].tolist()  
            rss[i]=data[['rss']].iloc[i].tolist() 
            if rp[i][0]==rp[i-1][0] and rp[i][1]==rp[i-1][1]:
                fw.write(str(ap[i][0])+','+str(rss[i][0])+' ')
            else:
                fw.write("\r\n")    # 换行
                fw.write(str(rp[i][0])+','+str(rp[i][1])+' '+str(ap[i][0])+','+ str(rss[i][0])+' ') 
            i=i+1
    fw.close()

    
