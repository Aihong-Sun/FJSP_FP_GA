'''

Code Time: 2022/5/10 13:48
by: Aihong-Sun
use for: Genetic algorithm for FJSP with fuzzy operation times
'''
import random
from Algorithm.FJSP.GA_for_FJSP import GA
import matplotlib.pyplot as plt
from Algorithm.Fuzzy_FJSP.Params import args
from Fuzzy_Shop_Floor.Job_Shop import Job_shop as Fuzzy_JS
from Fuzzy_Shop_Floor.Fuzzy_time_operator import *

class GA_Fuzzy(GA):
    def __init__(self,args):
        super(GA_Fuzzy, self).__init__(args)

    def create_Shop_Floor(self):
        self.JS=Fuzzy_JS(self.args)

    def Mutation_Machine(self,CHS):
        T_r = [j for j in range(self.half_len_chromo)]
        r = random.randint(1, self.half_len_chromo)  # 在区间[1,T0]内产生一个整数r
        random.shuffle(T_r)
        R = T_r[0:r]  # 按照随机数r产生r个互不相等的整数
        for i in R:
            O_site=self.J_site[i]
            pt=self.args.Processing_Time[O_site[0]][O_site[1]]
            pt_find=pt[0]
            len_pt=len(pt)-1
            k,m=1,0
            while k<len_pt:
                if Measure(pt_find,pt[k]):
                    pt_find=pt[k]
                    m=k
                k+=1
            CHS[i]=m
        return CHS



if __name__=="__main__":
    from Gantt import Fuzzy_Gantt
    import time
    for i in range(10):
        print('----------------start----------------')
        t1=time.time()
        ga=GA_Fuzzy(args)
        Best_JS=ga.main()
        t2=time.time()
        print('best Makespan-->>>:', Best_JS.C_end,'-->> CPU(s):',t2-t1)
        Fuzzy_Gantt(Best_JS)
