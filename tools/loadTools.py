'''
date: 22.01.03
author: pmy
description: tools for load
'''

import numpy as np


def loadIndexs(name):
    '''
    读取一般性 Index文件
    :param name: 网络名
    :return: indexs 列表
    '''
    file = open("data/"+name+"/Index_"+name+".txt","r")
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
    matrix = np.loadtxt("data/"+name+"/Sample_"+name+".txt")
    matrix = matrix.T # 进行转置，看需求
    return matrix


def loadDict(name):
    '''
    同质字典
    :param name:
    :return:
    '''
    return np.loadtxt("data/"+name+"/dic_Sample.txt")


def loadCoef(name):
    '''
    同质稀疏码
    :param name:
    :return:
    '''
    return np.loadtxt("data/" + name + "/coef_Sample.txt")

def loadDictH(name):
    '''
    异质字典
    :param name:
    :return:
    '''
    return np.loadtxt("data/"+name+"/dic_Sampleh.txt")

def loadCoefH(name):
    '''
    异质稀疏码
    :param name:
    :return:
    '''
    return np.loadtxt("data/" + name + "/coef_Sampleh.txt")


def loadSampleRec(name):
    '''
    采样恢复矩阵
    :param name:
    :return:
    '''
    matrix = np.loadtxt("data/" + name + "/Sample_Recovery.txt")
    matrix = matrix.T  # 进行转置，看需求
    return matrix