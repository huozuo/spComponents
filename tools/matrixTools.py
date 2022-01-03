'''
date: 21.11.12
author: pmy
func: 矩阵处理相关tools
note:
    进行sample - dict*coef的误差计算，非零的统计，除以sample中1的个数
    载入txt矩阵到np中
    保存dict矩阵和coef矩阵到txt中
version: v2
location: spComponents
'''
import numpy as np
import spComponents

# 同质
def errBetweenMatrix(aMatrix,bMatrix):
    '''
    计算两矩阵差值比例
    以a为基
    返回两者相差比例
    :param aMatrix: 基矩阵
    :param bMatrix: 比较矩阵
    :return:
    '''
    orginalE = np.sum(aMatrix)
    res = aMatrix - bMatrix
    res = np.maximum(res,-res) # 该方法是在两个矩阵中取元素的最大值，一正一负，那么必然是绝对值
    curE = np.sum(res)
    return curE / orginalE


def matrixSum(matrix):
    '''
    返回当前matrix的元素和
    :param matrix:
    :return:
    '''
    return np.sum(matrix)


def absError(sampleMatrix,dict,coef):
    '''
    返回误差绝对值
    :param sampleMatrix:
    :param dict:
    :param coef:
    :return:
    '''
    sampleMatrix[sampleMatrix>0] = 1
    originalEng = np.sum(sampleMatrix)
    reconstruction_matrix = np.dot(dict, coef)
    # 用于浮点数矩阵的情况
    reconstruction_matrix[reconstruction_matrix >= 0.5] = 1
    reconstruction_matrix[reconstruction_matrix < 0.5] = 0
    # reconstruction_matrix[reconstruction_matrix > 1] = 1 # 布尔矩阵，包括知识图谱的情况
    # print("初始能量为：",originalEng)
    error_matrix = sampleMatrix - reconstruction_matrix
    error_matrix[error_matrix != 0] = 1
    errorEng = np.sum(error_matrix)
    return errorEng


def calcSum(matrix):
    '''
    统计异质（同质）矩阵的非零个数
    :param matrix:
    :return:
    '''
    matrixCopy = matrix.copy()
    matrixCopy[matrixCopy!=0] = 1
    return np.sum(matrixCopy)

def error(sampleMatrix,dict,coef):
    '''
    计算并打印误差信息
    误差百分比
    :param sampleMatrix: 初始矩阵
    :param dict: 分解得到的字典矩阵
    :param coef: 分解得到的稀疏码矩阵
    :return: None
    '''
    # sampleMatrix[sampleMatrix > 0] = 1
    originalEng = calcSum(sampleMatrix)
    print("原本矩阵的能量：" + str(originalEng))
    reconstruction_matrix = np.dot(dict, coef)
    # reconstruction_matrix[reconstruction_matrix > 1] = 1
    error_matrix = sampleMatrix - reconstruction_matrix
    error_matrix[error_matrix != 0] = 1
    errorEng = calcSum(error_matrix)
    err = errorEng / originalEng
    print("误差是：" + str(errorEng))
    print("误差率为：" + str(err))
    return err


def errorCalc(name):
    '''
    输入name，直接计算，这样方便
    这里计算的是sample和recover的差值
    这里可以统计异质矩阵的
    :param name: 文件名
    :return:
    '''
    sample = spComponents.tools.loadTools.loadSample(name)
    sampleRec = spComponents.tools.loadTools.loadSampleRec(name)
    originalEng = np.sum(sample)
    print("原本矩阵的能量：" + str(originalEng))
    error_matrix = sample - sampleRec
    error_matrix[error_matrix != 0] = 1
    errorEng = np.sum(error_matrix)
    err = errorEng / originalEng
    print("最终误差是：" + str(errorEng))
    print("误差率为：" + str(err))
    return err


############## 异质 结尾带H####################
def matrixsErrH(matrixA,matrixB):
    '''
    异质矩阵误差
    以matrixA为基准
    默认都是整数
    :param matrixA: 建议放置采样矩阵
    :param matrixB:
    :return:
    '''
    preErr = np.sum(matrixA)

    errMatrix = matrixA - matrixB
    errMatrix[errMatrix!=0] = 1
    curErr = np.sum(errMatrix)

    return curErr/preErr

def nameErrH(name):
    '''
    根据name 计算异质网络表征恢复误差
    :param name:
    :return:
    '''
    sampleMatrix = spComponents.tools.loadTools.loadSample(name)
    recMatrix = spComponents.tools.loadTools.loadSampleRec(name)

    return matrixsErrH(sampleMatrix,recMatrix)


def dcErrH(dict,coef,sampleMatrix):
    '''
    根据 dict，coef，计算误差
    :param dict:
    :param coef:
    :param sampleMatrix:
    :return:
    '''
    recMatrix = spComponents.sparseRepresentation.recover.run(dict,coef)
    return matrixsErrH(sampleMatrix,recMatrix)





