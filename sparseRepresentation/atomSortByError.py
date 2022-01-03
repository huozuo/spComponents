'''
date: 21.12.03
author: pmy
func: 按照原子生成给sample矩阵带来的误差下降进行排序
      返回原子排序，并打印出50%，80%，90%的原子序号
version：v2
'''

from spComponents.sparseRepresentation import atom2nodes
from spComponents.tools import getFileName, errorTools
import numpy as np


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
    # 加载矩阵
    sampleMatrix = matrixTools.loadSample(name) # 获取采样矩阵
    dictMatrix = matrixTools.loadDict(name) #获取字典
    coefMatrix = matrixTools.loadCoef(name) #获取稀疏码
    #获得原子和字典的映射
    atom2nodesTool = atom2nodes.Atom2Nodes(name)
    atom2dict = atom2nodesTool.atom2dict # 原子与字典的映射关系
    # 计算每个原子的误差下降情况
    atomError = {}
    calcAtomError(sampleMatrix,dictMatrix,coefMatrix,atom2dict,atomError)
    # 对结果进行排序
    atomError = sorted(atomError.items(),key=lambda item:item[1],reverse=True)
    #打印50%，80%，90%分别是哪一个原子
    getSpecialAtom(sampleMatrix,dictMatrix,coefMatrix,atom2dict,atomError)
    # 返回结果
    res = [atom for atom,rate in atomError] # 将误差率下降删除，只返回顺序
    return res


def calcAtomError(sampleMatrix,dictMatrix,coefMatrix,atom2dict,atomError):
    '''
    遍历atom2dict，计算每个原子对应的误差下降
    :param sampleMatrix: 采样矩阵
    :param dictMatrix: 字典矩阵
    :param coefMatrix: 稀疏码矩阵
    :param atom2dict: 原子与字典的映射
    :param atomError: 原子误差下降，作为结果的存储
    :return:
    '''
    originalSum = np.sum(sampleMatrix)
    # 遍历atom2dict
    for atomIndex,dictIndexs in atom2dict.items():
        # 误差会有重叠，还是应该进行组合成矩阵
        dict = np.empty([np.shape(sampleMatrix)[0],0])
        coef = np.empty([0,np.shape(sampleMatrix)[1]])
        for dictIndex in dictIndexs:
            dictVec = dictMatrix[:,dictIndex]
            coefVec = coefMatrix[dictIndex,:]
            dict = np.concatenate((dict,dictVec.reshape((np.shape(dictVec)[0],1))),axis=1)
            coef = np.concatenate((coef,coefVec.reshape((1,np.shape(coefVec)[0]))),axis=0)
            # dict = np.concatenate((dict, dictVec), axis=1)
            # coef = np.concatenate((coef, coefVec), axis=0)

        # 这里有可能是有负数的，不过也无所谓，
        curError = matrixTools.absError(sampleMatrix, dict, coef)

        errRate = 1 - curError/originalSum

        atomError[atomIndex] = errRate # 最终放入的还是比例



def getSpecialAtom(sampleMatrix,dictMatrix,coefMatrix,atom2dict,atomError):
    '''
    打印50%，80%，90%分别是哪一个原子
    :param sampleMatrix:
    :param dictMatrix:
    :param coefMatrix:
    :param atom2dict:
    :return:
    '''
    originalSum = np.sum(sampleMatrix)
    dict = np.empty([np.shape(sampleMatrix)[0], 0])
    coef = np.empty([0, np.shape(sampleMatrix)[1]])
    flag = 0 # 打印标志位
    for atomIndex,error in atomError:
        for dictIndex in atom2dict[atomIndex]:
            dictVec = dictMatrix[:, dictIndex]
            coefVec = coefMatrix[dictIndex, :]
            dict = np.concatenate((dict, dictVec.reshape((np.shape(dictVec)[0], 1))), axis=1)
            coef = np.concatenate((coef, coefVec.reshape((1, np.shape(coefVec)[0]))), axis=0)
        curError = matrixTools.absError(sampleMatrix, dict, coef)
        errRate = curError/originalSum
        # 只打印一次 用1,2,4来进行划分，使得只被打印一次
        if flag<4 and errRate <=0.1:
            flag += 4
            print("###90%",atomIndex)
        elif flag<2 and errRate <=0.2:
            flag += 2
            print("###80%",atomIndex)
        elif flag<1 and errRate <=0.5:
            flag += 1
            print("###50%",atomIndex)
