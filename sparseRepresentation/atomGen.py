'''
date: 21.11.10
func: 原子生成
location: spComponents
version: v3
'''

from numpy import *
import networkx as nx
import os
import numpy as np

def Atom_Gen(base_name, name,sep = ""):
    '''
    生成原子，恢复网络，生成原子数据
    :param base_name: 每个网络的专属文件夹，其中要有dic_Sample文件，coef_Sample文件，Sample+name文件
    :param name: 网络的名称
    :param sep : 默认是""，即为不加，处理同质，可以选填"h"，来处理异质原子生成
    :return: 无返回，直接完成
    '''
    f = open(base_name + "/dic_Sample.txt")  # 字典文件的路径
    line = f.readline()
    G = []

    # Num_Atom = 200  #字典矩阵的列数 即原子的个数
    # Atom_Len = 20   #字典矩阵的行数的开平方 即原子的size
    dic_matrix = np.loadtxt(base_name + "/dic_Sample.txt")
    Atom_Len = int(sqrt(dic_matrix.shape[0]))
    Num_Atom = dic_matrix.shape[1] #直接覆盖

    #####去同构，获取原子
    # 读进来 获得G 包含字典的列表
    for i in range(Num_Atom):
        G.append([])
    while line != '':
        line = line.replace('\n', '')
        line = line.split(' ')
        k = 0
        for element in line:
            G[k].append(float(element))
            k = k + 1
        line = f.readline()
    f.close()

    Sample_Set = []
    Num_Sample = 1
    for i in range(len(G)):
        Sample = nx.Graph()
        for j in range(Atom_Len):
            # for k in range(j + 1, Atom_Len):
            for k in range(Atom_Len):  ## 问题出在这
                if j == k: continue
                t = Atom_Len * j + k
                t_2 = j + Atom_Len * k
                if G[i][t] >0.01:
                    Sample.add_edge(j, k,label=int(G[i][t]))
        In_F = False
        if Sample_Set == []:
            Sample_Set.append(Sample)
            nx.write_gexf(Sample, base_name + "/Atom_" + str(Num_Sample) + ".gexfs", encoding='utf-8')  # 书写原子的路径
            Num_Sample = Num_Sample + 1
        # 去同构
        for element in Sample_Set:
            GM = nx.isomorphism.GraphMatcher(Sample, element, edge_match=nx.isomorphism.categorical_edge_match(['label'], [-1]))
            if GM.is_isomorphic():
                In_F = True
            # if nx.is_isomorphic(Sample, element): # 同质同构方法
            #     In_F = True
        if not In_F:
            Sample_Set.append(Sample)
            nx.write_gexf(Sample, base_name + "/Atom_" + str(Num_Sample) + ".gexfs", encoding='utf-8')
            Num_Sample = Num_Sample + 1

    print('Number of Atom: ', len(Sample_Set))
    Atoms_Num = len(Sample_Set)

    # =============================Recover_Sample========================================================================#

    f = open(base_name + "/coef_Sample.txt")  # 读取稀疏码文件
    line = f.readline()
    Delta = []
    k = 0
    while line != '':
        Delta.append([])
        line = line.replace('\n', '')
        line = line.split(' ')
        for element in line:
            t = float(element)
            Delta[k].append(t)
        k = k + 1
        line = f.readline()
    f.close()

    f = open(base_name + "/dic_Sample.txt")  # 再次打开字典文件
    line = f.readline()
    Dict = []
    k = 0
    while line != '':
        Dict.append([])
        line = line.replace('\n', '')
        line = line.split(' ')
        for element in line:
            t = float(element)
            Dict[k].append(t)
        k = k + 1
        line = f.readline()
    f.close()

    Network_Set = []
    f = open(base_name+"/Sample_" + name + ".txt")  # 读取采样文件
    line = f.readline()
    k = 0
    while line != '':
        Network_Set.append([])
        line = line.replace('\n', '')
        line = line.split(' ')
        line.remove('')
        for element in line:
            Network_Set[k].append(int(element))
        k = k + 1
        line = f.readline()
    f.close()

    Dict = matrix(Dict)
    Delta = matrix(Delta)
    print('Dimonsion of Dict: ', Dict.shape)
    print('Dimonsion of Coe: ', Delta.shape)

    Rec_G = Dict * Delta

    Rec_G = Rec_G.T
    Rec_G = matrix.tolist(Rec_G)

    Rec_GT = []
    k = 0
    for line in Rec_G:
        Rec_GT.append([])
        for element in line:
            if element > 0.5:
                Rec_GT[k].append(1)
            else:
                Rec_GT[k].append(0)
        k = k + 1
    print('Number of Recover Networks: ', len(Rec_GT))
    print('Number of Sample Networks', len(Network_Set))
    k = 0
    for line in Rec_GT:
        if line in Network_Set:
            k = k + 1
    print('Number of Coverage：', k)

    f = open(base_name + "/Sample_Recovery.txt", 'w')
    for line in Rec_GT:
        for element in line:
            f.write(str(element))
            f.write(' ')
        f.write('\n')
    f.close()

    # =============================Recover_Network========================================================================#

    f_S = open(base_name + "/Sample_Recovery.txt")  # 打开采样恢复文件
    f_I = open(base_name+"/Index_" + name + ".txt")  # 打开index文件

    Sample = f_S.readline()
    Index = f_I.readline()
    k = 0
    G = nx.Graph()
    while Sample != '':
        #文件读取，从字符串变成列表
        Sample = Sample.replace('\n', '')
        Sample = Sample.split(' ') #变成列表
        Index = Index.replace('\n', '')
        Index = Index.split(',')
        Index.remove('')
        Sample_Size = len(Index)
        for i in range(Sample_Size):#将列表中的字符转换成int
            Index[i] = int(Index[i])
        for i in range(Sample_Size):
            for j in range(i + 1, Sample_Size):
                pos = i * Sample_Size + j
                if Sample[pos] == '1': #这里修改了 原本是=="1"
                    G.add_edge(Index[i], Index[j])
        k = k + 1
        Sample = f_S.readline()
        Index = f_I.readline()

    nx.write_gexf(G, base_name + "/Network_recover.gexfs", encoding='utf-8')  # 写入恢复网络
    f_S.close()
    f_I.close()

    # ============================Statistics_Atom========================================================================#
    Node_Num = []
    Edge_Num = []
    Average_Deg = []

    for i in range(1, Atoms_Num + 1):
        G = nx.read_gexf(base_name + '/Atom_' + str(i) + '.gexfs')  # 读取所有的原子网络
        node_num = len(G.nodes())
        edge_num = len(G.edges())
        Node_Num.append(node_num)
        Edge_Num.append(edge_num)
        if node_num != 0:
            Average_Deg.append(edge_num * 2 / node_num)

    f = open(base_name + "/Atom_Statistics.txt", 'w')  # 打开 atom_statistics
    f.write(str(Node_Num))  # 每个原子的节点数
    f.write(str(Edge_Num))  # 每个原子的边数
    f.write('\n')
    f.write(str(Average_Deg))  # 每个原子的平均度 由边数*2/节点数
    print("平均度：",sum(Average_Deg)/len(Average_Deg))
    f.close()


def get_filename(base_filename):
    '''
    获取当前目录下的所有文件
    :param base_filename:
    :return:
    '''
    list = os.listdir(base_filename)
    return list

def run():
    origin_filename = "data/"
    network_director_lsit = get_filename(origin_filename)
    count = 0
    for each in network_director_lsit:
        if each == "gexfs":
            continue
        filename = origin_filename + each  # 每个文件夹的文件
        print(each)
        Atom_Gen(filename, each)
        count += 1
        print("process{}/{}".format(count,len(network_director_lsit)))
