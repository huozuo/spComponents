'''
date: 22.01.03
author: pmy
description: 将dic、coef--recMatrix--gexf的过程重写
'''

import networkx as nx
import numpy as np
import mergeMatrixs
import spComponents
import tqdm


def run(dict,coef,name):
    '''
    进行网络恢复
    :param dict:
    :param coef:
    :param name:
    :return:
    '''
    recMatrix = genRecMatrix(dict,coef)
    G = transformMatrix2gexf(recMatrix,name)
    gexfPath = "data\\"+name+"\\"+name+".gexf"
    nx.write_gexf(G,gexfPath)


def genRecMatrix(dict,coef):
    '''
    生成 恢复采样矩阵
    读取每一列，对矩阵进行加法
    :param dict: 字典矩阵
    :param coef: 稀疏码矩阵
    :return: recMatrix
    '''
    n = np.shape(dict)[1]

    recMatrix = np.zeros((np.shape(dict)[0],np.shape(coef)[1])) # 我希望其中都是整型，不是浮点型 TODO

    for j in tqdm.tqdm(range(n)):
        d = np.reshape(dict[:,j],(np.shape(dict)[0],1))
        c = np.reshape(coef[j,:],(1,np.shape(coef)[1]))
        addMatrix = np.dot(d,c)
        mergeMatrixs.mergeMatrixs(recMatrix,addMatrix)

    return recMatrix


def transformMatrix2gexf(recMatrix,name):
    '''
    transform recMatrix to gexf
    :param recMatrix: 恢复采样矩阵
    :param name: 网络名称
    :return:
    '''
    indexs = spComponents.tools.loadTools.loadIndexs(name)
    G = nx.Graph()
    m,n = np.shape(recMatrix)
    sampleSize = len(indexs[0])
    # 读取indexs

    for j in range(n):
        curIndex = indexs[j]
        # 采样矩阵 每一列 是一个网络
        for i in range(m):
            if recMatrix[i][j] == 0: continue
            u = i // sampleSize # 整除
            v = i % sampleSize
            G.add_edge(curIndex[u],curIndex[v],label=int(recMatrix[i][j]))

    return G