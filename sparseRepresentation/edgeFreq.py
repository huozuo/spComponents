'''
date:22.01.27
author:pmy
description:
    aim:    找到原子对应的实际节点，将它们的原子连边选出来，然后全部放进dict中进行统计频次
    realization:
        - dict的key不能放元组，因为不能hash，所以解决方法将节点转成字符串，用 u_v 方式进行表示，u < v
        - 使用spComponents中的相应的工具类，读取原子，读取atom2nodes
        - 按序遍历原子，得到原子的结构
'''

from spComponents.tools.readAtom2nodes import *
from spComponents.sparseRepresentation.networkInfo import NetworkInfo
from spComponents.tools import loadTools


def run(name,sampleSize):
    '''
    统计 原始网络中，每条边在所有原子的出现的频次
    :param name: 网络名称
    :param sampleSize: 采样大小
    :return: {"u_v":freq}
    '''
    edgeFreq = {}
    G = loadTools.loadGexf(name)
    networkInfo = NetworkInfo(name)
    atom2nodes = readAtom2nodes(name,sampleSize)
    for atomId in atom2nodes.keys():
        nodess = atom2nodes[atomId]
        atom = networkInfo.atoms[atomId-1] # atomId从1开始，atoms是列表
        for nodes in nodess:
            for u,v in atom.edges(): # edge is tuple
                u,v = nodes[int(u)],nodes[int(v)] # 转换成实际节点
                if u=="0" or u=="-1" or v=="0" or v=="-1": continue # 排除实际节点不存在的情况 其实下面if已经过滤了
                u,v = (v,u) if u>v else (u,v) # 使得edgeStr对应edge唯一 字典序排序
                if (u,v) in G.edges():
                    edgeStr = str(u)+"_"+str(v)
                    if edgeStr not in edgeFreq.keys(): edgeFreq[edgeStr] = 0
                    edgeFreq[edgeStr] += 1

    return edgeFreq





if __name__=="__main__":
    print(run("cora", 10))
