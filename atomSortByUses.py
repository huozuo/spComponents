'''
date: 21.12.08
author: pmy
func: 将原子按照原子的使用次数进行排序
      本py直接就按照最终的个数
version: v0
location: spComponents
'''


from spComponents import matrixTools
from spComponents import atom2nodes
from spComponents import getFileName
import numpy as np
from dalib.util.utils_pmy.IO_utils import IO_utils

def run():
    '''
    运行所有
    :return:
    '''
    # atom2nodes = Atom2Nodes(name)
    # atom2nodes.getAllnodes()
    fileList = getFileName.get_filename("data//")
    for file in fileList:
        if file == "原始网络们": continue
        print(file)
        print(runOne(file))
    print("done")

def runOne(name):
    '''
    主运行函数
    :param name:
    :return:
    '''
    ioUtil = IO_utils()
    # 加载矩阵
    sampleMatrix = matrixTools.loadSample(name) # 获取采样矩阵
    dictMatrix = matrixTools.loadDict(name) #获取字典
    coefMatrix = matrixTools.loadCoef(name) #获取稀疏码
    #获得原子和字典的映射
    atom2nodesTool = atom2nodes.Atom2Nodes(name)
    atom2dict = atom2nodesTool.atom2dict # 原子与字典的映射关系
    # 计算每个原子的使用次数
    atomUses = {}
    calcAtomUses(coefMatrix,atom2dict,atomUses)
    # 对结果进行排序
    atomUses = sorted(atomUses.items(),key=lambda item:item[1],reverse=True)
    # 存储结果
    storePath = "data//"+name+"//原子使用次数.txt"
    ioUtil.save_tupleList_txt(atomUses,storePath)
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

