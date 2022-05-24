
import numpy as np
import random
import copy

from Algorithm.FJSP.Params import args
from Flexible_Job_Shop.Job_Shop import Job_shop


class GA:
    def __init__(self,args):
        self.args=args
        self.N_elite=args.N_elite
        self.Pop_size=args.pop_size
        self.gene_size=args.gene_size
        self.pc=args.pc
        self.pm=args.pm
        self.Chromo_setup()
        self.Best_JS=None
        self.Best_Cmax=9999
        self.C_end=[]

    def create_Shop_Floor(self):
        self.JS=Job_shop(self.args)

    def Chromo_setup(self):
        self.os_list = []
        for i in range(len(self.args.O_num)):
            self.os_list.extend([i for _ in range(self.args.O_num[i])])
        self.half_len_chromo=len(self.os_list)
        self.ms_list=[]
        self.J_site=[]      #方便后面的位置查找
        for i in range(len(self.args.Processing_Machine)):
            for j in range(len(self.args.Processing_Machine[i])):
                self.ms_list.append(len(self.args.Processing_Machine[i][j]))
                self.J_site.append((i,j))

    def random_initial(self):
        self.create_Shop_Floor()
        self.Pop=[]
        for i in range(self.Pop_size):
            Pop_i=[]
            random.shuffle(self.os_list)
            Pop_i.extend(copy.copy(self.os_list))
            ms=[]
            for i in self.ms_list:
                ms.append(random.randint(0,i-1))
            Pop_i.extend(ms)
            self.Pop.append(Pop_i)

    #POX:precedence preserving order-based crossover
    def POX(self,CHS1, CHS2):
        Job_list = [i for i in range(self.JS.n)]
        random.shuffle(Job_list)
        r = random.randint(2, self.JS.n - 1)
        Set1 = Job_list[0:r]
        new_CHS1 = list(np.zeros(self.half_len_chromo, dtype=int))
        new_CHS2 = list(np.zeros(self.half_len_chromo, dtype=int))
        for k, v in enumerate(CHS1):
            if v in Set1:
                new_CHS1[k] = v + 1
        for i in CHS2:
            if i not in Set1:
                Site = new_CHS1.index(0)
                new_CHS1[Site] = i + 1

        for k, v in enumerate(CHS2):
            if v not in Set1:
                new_CHS2[k] = v + 1
        for i in CHS2:
            if i in Set1:
                Site = new_CHS2.index(0)
                new_CHS2[Site] = i + 1
        new_CHS1 = list(np.array([j - 1 for j in new_CHS1]))
        new_CHS2 = list(np.array([j - 1 for j in new_CHS2]))
        return new_CHS1, new_CHS2

    #交换变异
    def swap_mutation(self,p1):
        D = len(p1)
        c1 = p1.copy()
        r = np.random.uniform(size=D)
        for idx1, val in enumerate(p1):
            if r[idx1] <= self.pm:
                idx2 = np.random.choice(np.delete(np.arange(D), idx1))
                c1[idx1], c1[idx2] = c1[idx2], c1[idx1]
        return c1

    def Crossover_Machine(self, CHS1, CHS2):
        T_r = [j for j in range(self.half_len_chromo)]
        r = random.randint(1, self.half_len_chromo)  # 在区间[1,T0]内产生一个整数r
        random.shuffle(T_r)
        R = T_r[0:r]  # 按照随机数r产生r个互不相等的整数
        # 将父代的染色体复制到子代中去，保持他们的顺序和位置
        for i in R:
            K, K_2 = CHS1[i], CHS2[i]
            CHS1[i], CHS2[i] = K_2, K
        return CHS1, CHS2

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
                if pt_find>pt[k]:
                    pt_find=pt[k]
                    m=k
                k+=1
            CHS[i]=m
        return CHS

    def Elite(self):
        Fit=dict(enumerate(self.Fit))
        Fit=list(sorted(Fit.items(),key=lambda x:x[1]))
        idx=[]
        for i in range(self.N_elite):
            idx.append(Fit[i][0])
        return idx

    # 选择
    def Select(self):
        idx1=self.Elite()
        Fit = []
        for i in range(len(self.Fit)):
            fit = 1 / self.Fit[i]
            Fit.append(fit)
        Fit = np.array(Fit)
        idx = np.random.choice(np.arange(len(self.Fit)), size=len(self.Fit)-self.N_elite, replace=True,
                               p=(Fit) / (Fit.sum()))
        Pop=[]
        idx=list(idx)
        idx.extend(idx1)
        for i in idx:
            Pop.append(self.Pop[i])
        self.Pop=Pop

    def decode(self,CHS):
        self.JS.reset()
        for i in range(self.half_len_chromo):
            O_num=self.JS.Jobs[CHS[i]].cur_op
            m_idx=self.J_site.index((CHS[i],O_num))
            self.JS.decode(CHS[i],CHS[m_idx+self.half_len_chromo])
        if self.Best_Cmax>self.JS.C_max:
            self.Best_Cmax=self.JS.C_max
            self.Best_JS=copy.copy(self.JS)
        return self.JS.C_max

    def fitness(self):
        self.Fit=[]
        for Pi in self.Pop:
            self.Fit.append(self.decode(Pi))

    def crossover_operator(self):
        random.shuffle(self.Pop)
        Pop1,Pop2=self.Pop[:int(self.Pop_size/2)],self.Pop[int(self.Pop_size/2):]
        for i in range(len(Pop1)):
            if random.random()<self.pc:
                p1,p2=self.POX(Pop1[i][0:self.half_len_chromo],Pop2[i][0:self.half_len_chromo])
                p3, p4 =self.Crossover_Machine(Pop1[i][self.half_len_chromo:], Pop2[i][self.half_len_chromo:])
                p1.extend(p3)
                p2.extend(p4)
                Pop1[i],Pop2[i]=p1,p2
        self.Pop=Pop1+Pop2

    def mutation_operator(self):
        for i in range(len(self.Pop)):
            if random.random()<self.pm:
                p1=self.swap_mutation(self.Pop[i][0:self.half_len_chromo])
                p2=self.Mutation_Machine(self.Pop[i][self.half_len_chromo:])
                p1.extend(p2)
                self.Pop[i]=p1

    def main(self):
        Fit_best=[]
        self.random_initial()
        self.fitness()
        Best_Fit=min(self.Fit)
        self.Best_JS = self.JS
        for i in range(self.gene_size):
            self.Select()
            self.crossover_operator()
            self.mutation_operator()
            self.fitness()
            Min_Fit=min(self.Fit)

            if Min_Fit<Best_Fit:
                Best_Fit=Min_Fit
            Fit_best.append(Best_Fit)
        # Fuzzy_Gantt(self.Best_JS)
        x=[_ for _ in range(self.gene_size)]
        # plt.plot(x,Fit_best)
        # plt.show()
        # plt.xlabel("step")
        # plt.ylabel("makespan")
        print('----->>>最小完工时间', Best_Fit, '----->>>平均完工时间', sum(self.Fit) / len(self.Fit))
        return self.Best_JS

if __name__=="__main__":
    import time
    t1=time.time()
    ga=GA(args)
    Best_JS=ga.main()
    t2=time.time()
    print('-->> CPU(s):',t2-t1)
    # Fuzzy_Gantt(Best_JS)
