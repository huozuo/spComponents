'''
date: 21.11.11
author: pmy
func: 统计atom与实际网络的匹配程度
note：
计算稀疏表征的原子匹配率
首先读取原始网络，作为边的判别
然后读取原子网络，读取原子对应的实际节点
遍历所有的原子边，将其翻译成实际节点的边，判断实际节点便是否在原网络中存在
如果存在，则cnt++
最终打印出cnt/总的原子数
version：v0
location：spComponents
'''
import networkx as nx
from spComponents.list2Lists import *

class CalcAtomMathc:
    def __init__(self,name,size):
        self.name = name
        self.size = size  # 原子的大小
        self.G = self.loadNetwork("data\\原始网络\\"+name+".gexf")
        self.nodes = {}
        self.readAtom2nodes("data\\"+name+"\\atom2nodes.txt")

    def readAtom2nodes(self,name):
        '''
        读取atom2nodes文件
        每两行，第一行是原子，第二行是节点list
        :return:
        '''
        f = open(name,'r',encoding="utf-8")
        while True:
            line1 = f.readline()
            line2 = f.readline()
            if not line2: break
            atomNum = int(line1.strip("\n").split(" ")[1])
            nodesStr = line2.strip("\n").split(": ")[1]
            nodes = nodesStr.split(" ")
            nodes = list_of_groups(nodes,self.size)
            self.nodes[str(atomNum)] = nodes

        f.close()

    def loadNetwork(self,name):
        '''
        读取nx的网络
        :return:
        '''
        return nx.read_gexf(name)

    def match(self,realNodes,g):
        '''
        根据原子来看边是否存在
        :param realNodes: 当前原子所对应的实际节点, list
        :param g: 当前原子网络
        :return: 是否匹配
        '''
        for start,end in g.edges:
            start = realNodes[int(start)]
            end = realNodes[int(end)]
            if (start,end) not in self.G.edges: return False

        return True

    def run(self):
        cnt = 0
        totalCnt = 0
        for atomNum in self.nodes.keys():
            nodes = self.nodes[atomNum]
            g = self.loadNetwork("data\\"+self.name+"\\Atom_"+atomNum+".gexf")
            for node in nodes:
                if len(node)<self.size: continue
                if self.match(node,g): cnt += 1
                totalCnt += 1
        # print(cnt,totalCnt)
        return cnt/totalCnt #匹配率


