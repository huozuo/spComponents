'''
date: 22.01.27
author: pmy
description: 读取atom2nodes.txt
                返回dict{原子序号:[[对应节点],[对应节点]]}
input: name, sampleSize
'''
import itertools
from spComponents.tools import list2Lists

def readAtom2nodes(name,sampleSize):
    '''
    读取atom2nodes.txt 获得原子在原图中的实际对应的节点集合
    :param name:
    :param sampleSize:
    :return: 返回dict{原子序号:[[对应节点],[对应节点]]}
    '''
    if sampleSize ==0 : return None
    res = {}
    path = "data/"+name+"/atom2nodes.txt"
    f = open(path,"r",encoding="UTF-8")
    for line1,line2 in itertools.zip_longest(*[f]*2):
        id = int(line1.strip("\n").split(" ")[1])
        nodes = line2.strip("\n").strip(" ").split(" ")[1:]
        nodes = list2Lists.splitList(nodes,sampleSize)
        res[id] = nodes
    f.close()
    return res



if __name__=="__main__":
    readAtom2nodes("cora",10)