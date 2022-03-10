'''
date:22.03.10
author:pmy
description: 用于统计表征结果中星型原子的占比
             需要实现进行网络稀疏表征
            # 读取网络信息
            # 获取原子信息，判断哪些原子是星型原子
            #   判断条件：节点数=边数+1、最大度是否为边数
            # 根据每个原子的使用次数，进行判断
'''
from spComponents.sparseRepresentation import networkInfo
from spComponents.tools import getFileName
import networkx as nx
from spComponents.sparseRepresentation import atomSortByUses


def isStar(atom):
    '''
    判断原子网络是否是星型网络
    :param atom:
    :return:
    '''
    nodeNum = atom.number_of_nodes()
    edgeNum = atom.number_of_edges()
    if nodeNum!=edgeNum+1:return False
    maxDeg = max(deg for node,deg in atom.degree) # 获取最大度
    if maxDeg!=edgeNum:return False
    return True


def runOne(name):
    ni = networkInfo.NetworkInfo(name)
    # 统计原子使用次数
    atomUses = {}
    atomSortByUses.calcAtomUses(ni.coef, ni.atom2dict, atomUses)
    # 分别统计星型原子使用次数与总原子使用次数
    sum = 0
    cnt = 0
    for id,use in atomUses.items():
        sum += use
        atom = ni.atoms[id-1]
        if isStar(atom):
            cnt += use
    return cnt/sum


def run():
    basePath = "data/"
    files = getFileName.showDir(basePath)
    for file in files:
        if ".gexf" in file: continue
        print("####"+file+"####")
        print(runOne(file))
        print(" ")


if __name__=="__main__":
    g = nx.Graph()
    # g.add_edge(1,2)
    # g.add_edge(4,2)
    # g.add_edge(1,3)
    g.add_edge(1,4)
    print(isStar(g))




