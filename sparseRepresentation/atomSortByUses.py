'''
date: 21.12.08
author: pmy
func: 将原子按照原子的使用次数进行排序
      本py直接就按照最终的个数
version: v0
location: spComponents
'''

from . import atom2nodes
from ..tools import getFileName, errorTools,loadTools
import numpy as np



def run():
    '''
    运行所有
    :return:
    '''
    # atom2nodes = Atom2Nodes(name)
    # atom2nodes.getAllnodes()
    fileList = getFileName.showDir("data/")
    for file in fileList:
        if file == "gexfs": continue
        print(file)
        atomUses = runOne(file)
        # 存储结果
        storePath = "data/" + file + "/atomUses.txt"
        save_tupleList_txt(atomUses, storePath)
    print("done")

def save_tupleList_txt(data,filename):
    with open(filename,'a',encoding='utf-8') as f:
        for key1,key2 in data:
            f.write(str(int(key1)))
            f.write(" , ")
            f.write(str(int(key2)))
            f.write('\n')
    f.close()

def runOne(name):
    '''
    主运行函数
    :param name:
    :return:
    '''
    # 加载矩阵
    sampleMatrix = loadTools.loadSample(name) # 获取采样矩阵
    dictMatrix = loadTools.loadDict(name) #获取字典
    coefMatrix = loadTools.loadCoef(name) #获取稀疏码
    #获得原子和字典的映射
    atom2nodesTool = atom2nodes.Atom2Nodes(name)
    atom2dict = atom2nodesTool.atom2dict # 原子与字典的映射关系
    # 计算每个原子的使用次数
    atomUses = {}
    calcAtomUses(coefMatrix,atom2dict,atomUses)
    # 对结果进行排序
    atomUses = sorted(atomUses.items(),key=lambda item:item[1],reverse=True)
    print("done")
    # res = [atom for atom, rate in atomUses]  # 将误差率下降删除，只返回顺序
    return atomUses


def calcAtomUses(coefMatrix,atom2dict,atomUses):
    '''
    统计原子的使用次数
    :param coefMatrix:
    :param atom2dict:
    :param atomUses:
    :return:
    '''
    # 遍历atom2dict
    for atomIndex, dictIndexs in atom2dict.items():
        uses = 0
        for dictIndex in dictIndexs:
            uses += np.sum(coefMatrix[dictIndex,:])
        atomUses[atomIndex] = uses

    return atomUses

