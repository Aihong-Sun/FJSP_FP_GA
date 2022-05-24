import argparse
from Instance.base_instance import *
from Instance.Instance_extraction import Instance
n,m,PT,MT,ni=Instance(R'C:\Users\Administrator\PycharmProjects\Shop_Floor_Sheduling\Instance\Fuzzy_Instance\Fuzzy_Ins'+"/LEI_1.pkl")
parser = argparse.ArgumentParser()

#params for FJSPF:
parser.add_argument('--n',default=n,type=int,help='job number')
parser.add_argument('--m',default=m,type=int,help='Machine number')
parser.add_argument('--O_num',default=ni,type=list,help='Operation number of each job')
parser.add_argument('--Machine_Info',default=Machine_Info,type=list,help='Information of processing Machine ')
parser.add_argument('--Processing_Machine',default=MT,type=list,help='processing machine of operations')
parser.add_argument('--Processing_Time',default=PT,type=list,help='fuzzy processing machine of operations')

#Params for GA
parser.add_argument('--pop_size',default=100,type=int,help='Population size of the genetic algorithm')
parser.add_argument('--gene_size',default=100,type=int,help='generation size of the genetic algorithm')
parser.add_argument('--pc',default=0.8,type=float,help='Crossover rate')
parser.add_argument('--pm',default=0.05,type=float,help='mutation rate')
parser.add_argument('--N_elite',default=10,type=int,help='Elite number')
args = parser.parse_args()

