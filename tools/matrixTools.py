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

def loadIndexs(name):
    '''
    读取一般性 Index文件
    :param name: 网络名
    :return: indexs 列表
    '''
    file = open("data//"+name+"//Index_"+name+".txt","r")
    indexs = []
    for line in file.readlines():
        if line == "": continue
        line = line.strip("\n").split(",")
        line = line[:len(line)-1]
        line = [int(each) for each in line]
        indexs.append(line)
    return indexs


def loadSample(name):
    '''
    输入位于本层目录下data里的文件名,返回矩阵
    :param name:
    :return:
    '''
    matrix = np.loadtxt("data\\"+name+"\\sample_"+name+".txt")
    matrix = matrix.T # 进行转置，看需求
    return matrix

def loadDict(name):
    return np.loadtxt("data\\"+name+"\\dic_Sample.txt")

def loadCoef(name):
    return np.loadtxt("data\\" + name + "\\coef_Sample.txt")

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

def loadSampleRec(name):
    '''
    采样恢复矩阵
    :param name:
    :return:
    '''
    matrix = np.loadtxt("data\\" + name + "\\Sample_Recovery.txt")
    matrix = matrix.T  # 进行转置，看需求
    return matrix


def errorCalc(name):
    '''
    输入name，直接计算，这样方便
    这里计算的是sample和recover的差值
    这里可以统计异质矩阵的
    :param name: 文件名
    :return:
    '''
    sample = loadSample(name)
    sampleRec = loadSampleRec(name)
    originalEng = np.sum(sample)
    print("原本矩阵的能量：" + str(originalEng))
    error_matrix = sample - sampleRec
    error_matrix[error_matrix != 0] = 1
    errorEng = np.sum(error_matrix)
    err = errorEng / originalEng
    print("最终误差是：" + str(errorEng))
    print("误差率为：" + str(err))
    return err



def save(name,dict,coef,add=""):
    '''
    将传入dict矩阵和coef矩阵按照name来进行存储
    存储的路径在data下
    :param name:
    :param dict:
    :param coef:
    :return:
    '''
    dic_name = "data\\"+name+"\\dic_Sample"+add+".txt"
    coef_name = "data\\"+name+"\\coef_Sample"+add+".txt"
    np.savetxt(dic_name, dict, fmt="%d")
    np.savetxt(coef_name, coef, fmt="%d")