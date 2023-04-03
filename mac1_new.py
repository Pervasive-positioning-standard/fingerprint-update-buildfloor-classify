import pymongo
import numpy as np
from pymongo.database import Database
from jproperties import Properties
from cryptography.fernet import Fernet
import pandas
import hashlib
 
 
# Helper function
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def mongodb_init():
    #connect to mongodb
    configs = Properties()
    with open('app-config.properties', 'rb') as config_file:
        configs.load(config_file)

    enc_key = str(configs["ENC_KEY"].data)
    enc_pwd = str(configs["ENC_PWD"].data)
    cipher_suite = Fernet(bytes(enc_key, 'utf-8'))
    bpassword = cipher_suite.decrypt(bytes(enc_pwd, 'utf-8'))
    password = bytes(bpassword).decode("utf-8")
    # print("decrypted ",password)
    password=hashlib.md5(password.encode('utf-8')).hexdigest()

    # password=hashlib.md5(str(configs["DB_PWD"].data).encode('utf-8')).hexdigest()
    mongo = pymongo.MongoClient(host='16.162.42.168',port=27017,username="root",password=password,authSource='admin')
    print('数据库当前的databases: ', mongo.list_database_names())#abdf3b75696725dfd2aa94907ddc3890
    return mongo


def get_db(mongo, db_name):
    db = Database(name = db_name, client=mongo)
    print('获取/创建库：', db.name)
    return db


mongo = mongodb_init()
db = get_db(mongo,'loc_db_v2')
Loc=db.LocSetting.find()
t=1  ## 记录第几个SourceCode
##遍历SourceCode
data=[]
for code in Loc:
    #code=code
    print (t,code)
    t+=1  
    Bu=code['BuildingID']
    Grid_list=[]
    for i in range(len(code['SiteSignalGridID'])):
        flo=code['SiteSignalGridID'][i][-21:]
        if i==0:
           Grid_list.append(code['SiteSignalGridID'][i])
        if len(code['SiteSignalGridID'])==1:
           data.append([code['SiteSignalGridID'][i-1][-21:],Grid_list])
        elif flo is not code['SiteSignalGridID'][i-1][-21:]:
           data.append([code['SiteSignalGridID'][i-1][-21:],Grid_list])
           Grid_list=[str(code['SiteSignalGridID'][i])]
        else:
           Grid_list.append(str(code['SiteSignalGridID'][i]))
df = pandas.DataFrame(data,columns=['BuFloor','Grid'],dtype=float)
df['rp']=0
df['mac']=0
print(df)

for i in range(len(df['Grid'])):
    raw=db.Grid.find_one({'GridID':df['Grid'][i][0]})
    rps=raw['RPIDList']
    df['rp'][i]=rps
print(df)

for i in range(len(df['Grid'])):
    W=[]
    if len(df['rp'][i]) != 0:
        raw=db.Fingerprint.find({'RPID': {"$in": df['rp'][i]}})
        for r in raw:
            wifi=r['WIFIRssVector']
            for j in range(len(wifi)):
                num=float(wifi[j][13:])
                wifi[j]=wifi[j][:12]
                W.append(wifi[j])
        #dict = {}
        #for key in W:
         #  dict[key] = dict.get(key, 0) + 1
        #E=[]
        #for d in dict.keys():
           #if dict[d]> len(df['rp'][i])//3*2:
         #   E.append(d)
                #if num<-85:
                #   wifi[j]='0'
        df['mac'][i]=W
    if len(df['rp'][i]) == 0:
        df['mac'][i]=[0]

df.to_csv('D:/vscode/mode3-server/mac_home.csv')
        
