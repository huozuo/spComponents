'''
date: 21.11.04
author: pmy
function: 实现中位数列的expansion
note： 逻辑为： 挨个对比除自己的每列，如果相似度（相较自己，实际是包含自己的情况）大于50%，则记录下该索引
               之后将这些索引与初始矩阵进行相似度比较，将大于阈值的记录下来，并返回
location: spComponents
'''
import numpy as np

def compare(B1,X):
    '''
    比较B1和X向量的相似度
    即X向量包含了多少B1的向量
    :param B1:
    :param X:
    :return:
    '''
    sum = np.sum(B1)
    cnt = np.sum(B1*X)
    return cnt/sum

def expansionCol(M1,MAT,B1,B2,Thres):
    '''
    进行expansion 适用于列
    （不用排除自己，因为无所谓啊其实）
    :param M1: 残差矩阵
    :param MAT: 初始矩阵
    :param B1: 中位数列
    :param B2: 匹配情况
    :param Thres: 阈值
    :return: 匹配情况
    '''
    for col in range(M1.shape[1]):
        cmp = compare(B1,M1[:,col])
        if cmp < 0.5: continue
        elif cmp > Thres or compare(B1,MAT[:,col]) > Thres: B2[col] = 1
        # elif compare(B1,MAT[:,col]) > Thres: B2[col] = 1

def expansionRow(M1,MAT,B1,B2,Thres):
    '''
    进行expansion 适用于行
    :param M1:
    :param MAT:
    :param B1:
    :param B2:
    :param Thres:
    :return:
    '''
    for row in range(M1.shape[0]):
        cmp = compare(B2,M1[row,:])
        if cmp < 0.5: continue
        elif cmp > Thres or compare(B2,MAT[row,:])>Thres: B1[row] = 1
        # if compare(B2,MAT[row,:]) > Thres: B1[row] = 1