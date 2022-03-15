'''
date: 22.03.07
author: pmy
description: 计算网络稀疏表征准确率与召回率
             根据网络的实际恢复情况进行计算，而不是根据矩阵分解
             以连边情况进行衡量，而不是节点
             因为连边会影响到连边
'''
import networkx as nx
from spComponents.tools import getFileName

def loadNetworks(name):
    '''
    获取原始网络与恢复网络
    :param name:
    :return:
    '''
    #原始网络
    initialG = nx.read_gexf("data/gexfs/"+name+".gexf")
    #恢复网络
    recG = nx.read_gexf("data/"+name+"/Network_recover.gexf")
    return initialG,recG

def intersection(G1,G2):
    '''
    计算G1,G2的公共边
    :param G1:
    :param G2:
    :return:
    '''
    cnt = 0
    for edge in G1.edges():
        if edge in G2.edges():
            try:
                cnt += 1 if G1.edges[edge]['label']==G1.edges[edge]['label'] else 0
            except(KeyError):
                cnt += 1
    return cnt

def accurate(name):
    '''
    准确率
    预测准确的正样本/预测出的正样本 = 正确的交集/恢复网络的边数
    :param name:
    :return:
    '''
    initialG, recG = loadNetworks(name)
    numerator = intersection(initialG,recG)
    denominator = recG.number_of_edges()
    return numerator/denominator

def recall(name):
    '''
    召回率
    预测准确的正样本/所有的正样本 = 正确的交集/原始网络的边数
    :param name:
    :return:
    '''
    initialG, recG = loadNetworks(name)
    numerator = intersection(initialG,recG)
    denominator = initialG.number_of_edges()
    return numerator/denominator


def runOne(name):
    '''
    生成当前py所有指标
    :param name:
    :return:
    '''
    print("####"+name+"####")
    print("precision: ",precision(name))
    print("recall: ",recall(name))
    print(" ")

def run():
    basePath = "data/"
    files = getFileName.showDir(basePath)
    for file in files:
        if ".xls" in file: continue
        runOne(file)