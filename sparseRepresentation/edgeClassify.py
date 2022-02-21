'''
date:22.02.19
author:pmy
description: 用于对原子表征的重复边进行分类
            - 之前有写，边重复有三类
            - 思路是排除法，分别看该边重复是不是1or3，从而确定是2
            - 首先是3的判定
                - 这是由于矩阵分解时的叠加带来的误差
                - 将字典矩阵与稀疏码矩阵乘积（1+1=2），就能得到重复边
                - 将矩阵中大于1的全部统计，翻译成边，然后把它们归为第一类
                - 之后将重复边集合中所有的边都分别减去其3类型的数目，排除3类型的边
            - 然后是1的判定
                - 遍历 重复边集合中所有边
                - 根据边的两端点，找到以端点为中心点的自我中心网络
                - 如果两个自我中心网络都含有这条边，那么它就是1类型的边，将其加入1类型集合
                - 之后将重复边集合中所有的边都分别减去其1类型的数目，排除1类型的边
            - 剩下的都是2类型的边
            - 三种类型之间可能会存在交集，这很正常

            ==当是ksvd表征时，是没有第三种类型的；而布尔时，需要加上type="boolean"参数==


            重复边出现的原因：
                - 首先，采样大小设为s，一般是要保证至少大于网络平均度的（为了不丢失边）
                - 采样网络数目为N，至少包含的边为：中心节点--一阶邻居
                - 除此之外，可能存在于一阶邻居之间的连边（对于我们所用的**传播网络**，基本很少、甚至不存在一阶邻居的连边）。因此总边数的区间是 [|E|，s-1 *N+x]，由于s大于平均度，那么必定是大于原始网络边数目的，即使出现两个大度点相邻的情况丢失边，也基本成立，且当网络中节点度均匀时，区间可近似为 [2|E|,s-1 * N + x]；然后上限是没有虚拟节点的情况，且加上一阶邻居间的连边数X（不确定值，可能为0）
                - 因此，本身在我们进行采样之后，其中有相当多的边，被分别以该边两端节点为中心节点采样时，采样了两次。于是大部分边就已经**重复了一次**。
                - 除此之外，会存在某条边被重复采样，举这样的例子，某条边的两个端点为1,2。这两个节点分别是a、b、c、d四个节点的一阶邻居，且这四个节点度不大。那么分别以abcd为中心点来进行采样，都会将1、2采样进来，那么在这里边 (1,2)就会被采样四次。**从而重复了多次**
                - 除此之外，在进行矩阵分解时，为了构建矩形，可能会把这个矩形中的少数0变成1。当然，这是在每轮迭代中都可能发生的，此时对于这些由0变1的元素，它们实际就是边，每变一次，**就会重复一次**
                - 以上是重复边出现的三个原因
'''
from spComponents.sparseRepresentation.networkInfo import NetworkInfo
from spComponents.sparseRepresentation.edgeFreq import edgeFreq
import numpy as np


def classify(name,type="ksvd"):
    '''
    边分类
    :param name: 网络名称
    :return: 返回3个类别的字典{edge:freq}
    '''
    # 获取networkInfo
    networkInfo = NetworkInfo(name)
    #获取edgeFreq
    edges = edgeFreq(name,networkInfo) # 重复边集
    #类别3的判定
    type3 = typeThree(networkInfo,type)
    #将类型3的边从集合中删除对应边数（为0则清除键）
    edges = removeEdge(edges,type3)
    #类别1的判定
    type1 = typeOne(edges,networkInfo)
    #将类型1的边从集合中删除对应边数
    edges = removeEdge(edges, type1)
    #分别将 type1 edges type3输出即可
    return type1, edges, type3

def typeThree(networkInfo,type):
    '''
    寻找类别3的边
    :param networkInfo:
    :return:
    '''
    res = {}
    if type =="ksvd":
        recMatrix = genRecMatrix(networkInfo.dict,networkInfo.coef) # ksvd
    else:
        recMatrix = np.dot(networkInfo.dict,networkInfo.coef) # 布尔型

    m,n = np.shape(recMatrix)
    for i in range(m):
        for j in range(n):
            if recMatrix[i][j] > 1:
                # 找到第j个自我中心网络
                nodes = networkInfo.index[j]
                # 确定是哪两个点
                u = i//networkInfo.sampleSize
                v = i%networkInfo.sampleSize
                u, v = nodes[int(u)], nodes[int(v)]  # 转换成实际节点
                if u=="0" or u=="-1" or v=="0" or v=="-1": continue # 排除实际节点不存在的情况 其实下面if已经过滤了
                u,v = (v,u) if u>v else (u,v) # 使得edgeStr对应edge唯一 字典序排序
                edgeStr = str(u) + "_" + str(v)
                if edgeStr not in res.keys(): res[edgeStr] = 0
                res[edgeStr] += recMatrix[i][j]-1
    return res

def typeOne(edges,networkInfo):
    '''
    寻找类别1的边
    :param edges:
    :param networkInfo:
    :return:
    '''
    res = {}
    node2index = realNode2index(networkInfo.index)
    for edge,freq in edges.items():
        u,v = edge.split("_")
        u,v = int(u),int(v)
        flag = 2
        index = node2index[u]
        if v in index: flag -= 1
        index = node2index[v]
        if u in index: flag -= 1
        if flag == 0:
            res[edge] = 1
    return res

def realNode2index(indexs):
    '''
    生成{实际节点：index}
    每个节点采样一次，自我中心网络唯一
    :param indexs:
    :return:
    '''
    res = {}
    for index in indexs:
        centralNode = index[0]
        res[centralNode] = index
    return res

def removeEdge(edges,type):
    '''
    将已经找到类型的边删除
    :return:
    '''
    res = edges.copy()
    for e,freq in edges.items():
        if e in type.keys():
            edges[e] -= type[e]
            if edges[e]<1:
                del res[e]
    return res

def genRecMatrix(dict,coef):
    '''
    生成恢复矩阵
    适用于ksvd
    如果是布尔矩阵，直接np.dot就可以了
    :param dict:
    :param coef:
    :return:
    '''
    recMatrix = np.dot(dict,coef)
    m,n = np.shape(recMatrix)
    for i in range(m):
        for j in range(n):
            if recMatrix[i][j] > 0.5:
                recMatrix[i][j] = 1
            else:
                recMatrix[i][j] = 0
    return recMatrix



if __name__=="__main__":
    res1,res2,res3 = classify("cora")
    print(res1)
    print(res2)
    print(res3)

