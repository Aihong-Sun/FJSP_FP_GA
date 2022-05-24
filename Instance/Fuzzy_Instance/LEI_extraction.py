import os
import re
import pickle
import numpy as np

file=r'C:\Users\Administrator\PycharmProjects\Shop_Floor_Sheduling\Instance\Fuzzy_Instance'
files=os.listdir(file)
for f in files:
    if '.txt' in f:
        new_f=f.split('.')[0]
        file_path=os.path.join(file,f)
        Instance=[]
        PT = []
        MT = []
        ni=[]
        with open(file_path,'r') as data:
            List=data.readlines()
            PT_i = []
            MT_i=[]
            while List!=[]:
                line_new=List[0].split()
                PT_ii = []
                if len(line_new)==1:
                    if PT_i!=[]:
                        ni.append(len(PT_i))
                        PT.append(PT_i)
                        MT.append(MT_i)
                    PT_i = []
                    MT_i=[]
                else:
                    for ln in line_new:
                        pat = r'\d+'
                        result = re.findall(pat, ln)
                        li = [int(ri) for ri in result]
                        if len(li)<3:
                            print(f)
                            print(List[0])
                        PT_ii.append(li)
                    PT_i.append(PT_ii)
                    MT_i.append([_+1 for _ in range(10)])
                del List[0]
            ni.append(len(PT_i))
            PT.append(PT_i)
            MT.append(MT_i)
        n=len(PT)
        m=10
        FJSP_Instance={'n':n,'m':m,'processing_time':PT,'Processing machine':MT,'Jobs_Onum':ni}
        if not os.path.exists(r'Fuzzy_Ins'):
            os.makedirs(r'Fuzzy_Ins')
        with open(os.path.join(r'Fuzzy_Ins', new_f + ".pkl"), "wb") as f1:
            pickle.dump(FJSP_Instance, f1, pickle.HIGHEST_PROTOCOL)