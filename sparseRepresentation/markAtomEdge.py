'''
date:22.03.28
author:pmy
description: 标记原网络中原子所涉及的边
             不考虑每个原子具体对应网络中的哪些结构，而是直接考虑原子对应了哪些边
             具体逻辑为，
                获取原子与字典的映射关系，将所涉及的字典列向量以及其对应的稀疏编码行向量保留下来
                按照稀疏表征的方式生成部分恢复网络
                将部分恢复网络与原恢复网络进行对比，将边进行标记
             输出经过边标记的原恢复网络
'''
from spComponents.sparseRepresentation import networkInfo,recover
import networkx as nx
import numpy as np


def run(name,atoms):
    '''
    根据指定的原子序号，从网络中选出这些原子相关的边，在原图上通过不同的labels展示出来
    并打印出占比
    :param name:
    :param atoms:
    :return:
    '''
    # 获取 字典矩阵，稀疏编码矩阵，原始恢复网络，原子与对应关系，indexs等
    ni = networkInfo.NetworkInfo(name)

    # 将所涉及的字典列向量以及其对应的稀疏编码行向量保留下来
    save = set()
    for atom in atoms:
        ds = ni.atom2dict[atom]
        for d in ds:
            save.add(d)
    for i in range(np.shape(ni.dict)[1]):
        if i not in save:
            ni.dict[:,i] = 0 # 全部置零

    # 新的恢复矩阵
    recMatrix = recover.genRecMatrix(ni.dict,ni.coef)
    recG = recover.transformMatrix2gexf(recMatrix,ni.index)

    G = nx.read_gexf("data/gexfs/"+name+".gexf")
    cnt = 0 # 边数
    for u,v in recG.edges():
        u,v = str(u),str(v)
        if (u,v) in G.edges():
            G.add_edge(u,v,labels=1) # 进行标记
            cnt += 1

    nx.write_gexf(G,"data/"+name+".gexf")

    print(cnt/G.number_of_edges())


if __name__=="__main__":
    atoms = [1,3,4,5,7,9,10,12,14]
    name = "ntp-ChicagoRegional"
    run(name,atoms)

