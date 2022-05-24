'''
Code Time: 2022/5/10 10:49
by: Aihong-Sun
use for: Job describe
'''

class Job:
    def __init__(self,idx,processing_machine,processing_time):
        self.idx=idx
        self.processing_machine=processing_machine
        self.processing_time=processing_time
        self.end=0
        self.cur_op=0
        self.cur_pt=None

    def get_next_info(self,Machine):
        m_idx=self.processing_machine[self.cur_op][Machine]
        self.cur_pt=self.processing_time[self.cur_op][Machine]
        return self.processing_time[self.cur_op][Machine],self.end,m_idx

    def update(self,e):
        self.end=e
        self.cur_op+=1