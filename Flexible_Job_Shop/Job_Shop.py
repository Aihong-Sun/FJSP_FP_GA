from Flexible_Job_Shop.Job import Job
from Flexible_Job_Shop.Machine import Machine


class Job_shop:
    def __init__(self,args):
        self.n= args.n
        self.m=args.m
        self.O_num=args.O_num
        self.PM = args.Processing_Machine
        self.PT = args.Processing_Time

    def reset(self):
        self.C_max = 0
        self.Jobs=[]
        for i in range(self.n):
            Ji=Job(i,self.PM[i],self.PT[i])
            self.Jobs.append(Ji)
        self.Machines=[]
        for j in range(self.m):
            Mi=Machine(j)
            self.Machines.append(Mi)

    def decode(self,Job,Machine):
        Ji=self.Jobs[Job]
        o_pt, s,M_idx = Ji.get_next_info(Machine)
        Mi=self.Machines[M_idx-1]
        start=Mi.find_start(s,o_pt)
        end=start+o_pt
        Ji.update(end)
        Mi.update(start,end,[Ji.idx,Ji.cur_op])
        if end>self.C_max:
            self.C_max=end