'''
date: 21.11.04
author: pmy
function: 输入网络节点列表，以及原始网络G
            实现一阶邻居和二阶邻居之间，分别进行排序，排序标准是度从高到低
location: spComponents
'''
import networkx as nx


def transformNetwork(nodesList,G):
    '''
    输入网络节点列表，以及原始网络G
            实现一阶邻居和二阶邻居之间，分别进行排序，排序标准是度从高到低
            (看插入的位置，不考虑0的情况)
    :param nodesList: 节点列表
    :param G: 原始网络，networkx
    :return: 返回排序之后的nodesList
    '''

    if len(nodesList) ==0: return nodesList
    # 传入Nei_i没有一阶邻居和二阶邻居的分界点，需要通过（中心点，当前节点）确定
    # 统计度（遍历呗，确定（当前点，其他点的个数））
    firstNei = {}
    secondNei = {}
    for node in nodesList:
        if node == nodesList[0]: continue
        deg = 0
        for nei in nodesList:
            if (node,nei) in G.edges(): deg += 1
        if (node,nodesList[0]) in G.edges(): firstNei[node] = deg
        else: secondNei[node] = deg
    # 分别进行排序，然后组合, 按照val进行排序
    firstNei = sorted(firstNei.items(),key = lambda x:x[1],reverse = True) # 得到的是元组
    secondNei = sorted(secondNei.items(), key=lambda x: x[1], reverse=True)
    # 获取排序之后的节点序号
    firstNei = [node for node,deg in firstNei]
    secondNei = [node for node, deg in secondNei]
    nodesList = [nodesList[0]] + firstNei + secondNei

    return nodesList


if __name__ == "__main__":
    G = nx.Graph()  # for test
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(3, 4)
    G.add_edge(3, 5)
    G.add_edge(4, 5)
    nodesList = [1, 2, 3, 4, 5]
    print(transformNetwork(nodesList, G))