'''
date: 21.12.31
author: pmy
description:
字典 * 稀疏码 = 恢复采样矩阵
字典 = 异质字典 + 同质字典
稀疏码 = 异质稀疏码 + 同质稀疏码
生成恢复采样矩阵，每次 按列 来对结果矩阵进行合并
'''
import numpy as np

def mergeMatrixs(recMatrix,addMatrix):
    '''
    合并两个矩阵
    合并规则为
    rec     add
        1+1 = 1
        1+0 = 1
        1+2 = 1
        这个可以归纳于 是否至少有一个为0
    :param recMatrix:
    :param addMatrix:
    :return:
    '''
    m,n = np.shape(recMatrix)
    if m!=np.shape(addMatrix)[0] or n!=np.shape(addMatrix)[1]: return

    for i in range(m):
        for j in range(n):
            if recMatrix[i][j] != addMatrix[i][j]:
                if recMatrix[i][j]==0 or addMatrix[i][j]==0:
                    recMatrix[i][j] += addMatrix[i][j]
                else:
                    recMatrix[i][j] = 0
