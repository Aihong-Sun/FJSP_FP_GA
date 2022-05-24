'''
Code Time: 2022/5/10 10:36
by: Aihong-Sun
use for: Job shop describe
'''
from Fuzzy_Shop_Floor.fuzzy_SF_Item import Job_fuzzy as Job
from Fuzzy_Shop_Floor.fuzzy_SF_Item import Machine_fuzzy as Machine
from Fuzzy_Shop_Floor.Fuzzy_time_operator import *

class Job_shop:
    def __init__(self,args):
        self.n= args.n
        self.m=args.m
        self.O_num=args.O_num
        self.PM = args.Processing_Machine
        self.PT = args.Processing_Time

    def reset(self):
        self.C_end=[0,0,0]
        self.C_max = 0
        self.Jobs=[]
        for i in range(self.n):
            Ji=Job(i,self.PM[i],self.PT[i])
            self.Jobs.append(Ji)
        self.Machines=[]
        for j in range(self.m):
            Mi=Machine(j)
            self.Machines.append(Mi)

    #Xu,,Ye,Wang,,Ling,Wang,,Sheng-yao,Liu,,& Min.(2015).An effective teaching-learning-based optimization algorithm
    # for the flexible job-shop scheduling problem with fuzzy processing time.NEUROCOMPUTING,148,260-268.
    def decode(self,Job,Machine):
        Ji=self.Jobs[Job]
        o_pt, s,M_idx = Ji.get_next_info(Machine)
        Mi=self.Machines[M_idx-1]
        start=Mi.find_start(s,o_pt)
        end=add(start,o_pt)
        Ji.update(end)
        Mi.update(start,end,[Ji.idx,Ji.cur_op])
        if Measure(end,self.C_end):
            self.C_end=end
            self.C_max=TFN_value(end)