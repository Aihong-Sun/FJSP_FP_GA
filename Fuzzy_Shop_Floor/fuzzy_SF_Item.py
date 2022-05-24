'''
Code Time: 2022/5/4 10:35
by: Aihong-Sun
use for: Job describe
'''
from Flexible_Job_Shop.Job import Job
from Flexible_Job_Shop.Machine import Machine
from Fuzzy_Shop_Floor.Fuzzy_time_operator import *

class Job_fuzzy(Job):
    def __init__(self,idx,processing_machine,processing_time):
        super(Job_fuzzy, self).__init__(idx,processing_machine,processing_time)
        self.end=[0,0,0]

class Machine_fuzzy(Machine):
    def __init__(self, idx):
        super(Machine_fuzzy, self).__init__(idx)

    def update(self,s,e,Job):
        self.start.append(s)
        self.start.sort(key=lambda u:u[1])
        self.end.append(e)
        self.end.sort(key=lambda u:u[1])
        idx=self.start.index(s)
        self._on.insert(idx,Job)

    def find_start(self,s,o_pt):
        if self.end==[]: return s
        else:
            if Measure(s,self.end[-1]):return s
            else:
                o_s=self.end[-1]
                l = len(self.end) - 2
                while l>=0:
                    if Measure(add(s,o_pt),self.start[l+1]):
                        break
                    if Measure(self.end[l],s) and Measure(self.start[l+1],add(self.end[l],o_pt)):
                        o_s=self.end[l]
                    elif  Measure(s,self.end[l]) and Measure(self.start[l+1],add(s,o_pt)):
                        o_s=s
                    l-=1
                return o_s