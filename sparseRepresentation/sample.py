'''
date: 21.11.04
author: pmy
function: 进行采样
note: 在原版的基础上增加排序的功能
        对一阶邻居，按照自我中心网络中的度进行排序；对二阶邻居，也是一样
        从而将能量集中，尽量促使形成矩形
location: spComponents
version: v1
'''
import networkx as nx
import numpy as np
import os
from spComponents.tools.getFileName import showDir
from spComponents.sparseRepresentation.transformNetwork import transformNetwork


def get_average_degree_of_network(G):
    return 2 * G.number_of_edges() / G.number_of_nodes()


def mkdir(filename):
    '''
    创建文件夹
    :param filename:  文件夹名
    :return:
    '''
    isExists = os.path.exists(filename)
    if not isExists:
        os.mkdir(filename)
        # print("目录创建完成")
    else:
        pass
        # print("目录已存在")

def gexf_to_edgelist(gexfname):
    '''
    将gexf图转换为edgelist文本，并且从1开始序列化节点，注意不能从0开始
    :param gexfname:
    :return: txt文件 格式是 node \t node
    '''
    G = nx.read_gexf(gexfname)
    edges = G.edges()
    nodes = list(G.nodes())
    fd = open("../../../../../教研室/6_29/Netwrok_Sparse_Code/out.txt", 'w')
    fd.write("{}\t{}\n".format(len(nodes), len(edges)))
    for edge in edges:
        fd.write('{}\t{}\n'.format(nodes.index(edge[0]) + 1, nodes.index(edge[1]) + 1))
    fd.close()


def serialize_graph(G):
    '''
    序列化graph，将G中的节点名字改为1开始的数字，注意不能从0开始
    :param G:
    :return:新的G
    '''
    new_G = nx.Graph()
    nodes = list(G.nodes())
    edges = list(G.edges())
    for edge in edges:
        new_G.add_edge(nodes.index(edge[0]) + 1, nodes.index(edge[1]) + 1)
    return new_G


def Creat_Random_Picture(Name):
    '''
    读取txt文件边并创建网络
    :param Name:
    :return:
    '''
    G = nx.Graph()
    f = open(Name)
    # a = f.readline()

    if ("%" in f.readline()):
        f.readline()
        # print(f.readline())

    edge = f.readline()
    k = 0
    while edge != '':
        edge = edge.replace('\n', '')
        if('\t' in  edge):
            edge = edge.split('\t') #无权图读取方式
        else:
            edge = edge.split(" ") #有权图读取方式 直接忽略权重

        node1 = int(edge[0])
        node2 = int(edge[1])
        G.add_edge(node1, node2)
        edge = f.readline()
        k = k + 1

    f.close()
    return G


def sample(graph_path, name, subnet_size):
    """
    采样
    :param graph_path: 图路径
    :param name: 生成文件的名字标记
    :param subnet_size: 原子最大大小
    :return:
    """
    store_filename =  "data\\"+ name + "\\"
    mkdir(store_filename)

    if '.txt' in graph_path:
        G = Creat_Random_Picture("E:\\教研室\\实验室\\原始网络们\\" + graph_path)
    elif '.gexf' in graph_path:
        G = nx.read_gexf(graph_path)
        # G = serialize_graph(G)  #直接给注释掉，然后看一看呢 除了进行边预测，平常也不会影响其实
    else:
        return

    Subnet_Size = subnet_size  # 子图大小

    ks = 1
    f = open(store_filename + "\\Sample_{}.txt".format(name), 'w',encoding='utf-8')  # 每一行都是邻接矩阵（egonetwork）
    f2 = open(store_filename + "\\Index_{}.txt".format(name), 'w')  # 每一行都是该节点的邻接节点

    print("点数是：",G.number_of_nodes()) #for test

    for i in G.nodes():
        ks = ks + 1

        G_neighbor = list(G.neighbors(i))
        Nei_i = [i] + G_neighbor  # 包含自身的list
        # if len(Nei_i) < Subnet_Size:  # 如果邻居数不够subnet_size, 添加二级邻居 注释掉啦，暂时弃用
        #     for nei in G.neighbors(i):
        #         Nei_i = Nei_i + list(G.neighbors(nei))

        Nei_i = Nei_i[:subnet_size]# 提前进行截断，反着之前也只是用的前20个
        ## 插入transfromNetwork进行排序
        Nei_i = transformNetwork(Nei_i,G)

        if len(Nei_i) < Subnet_Size:  # 如果还是不够，添加虚拟节点 0
            t = Subnet_Size - len(Nei_i)
            for j in range(t):
                Nei_i.append(0)


        # 如果len(Nei_i)>Subnet_Size怎么办呢，看下面感觉就是把0-Subnet_size之外的删去了     第二个问题
        Sample = np.zeros((Subnet_Size, Subnet_Size), np.int)  # 邻接矩阵
        for j in range(Subnet_Size):
            f2.write(str(Nei_i[j]) + ',')
            for k in range(Subnet_Size):  # 生成所有的边，然后直接判断有没有这个边，有就加进去，没有就算了，够暴力
                edge = (Nei_i[j], Nei_i[k])
                if edge in G.edges():  # 注意，在无向图中，edge in G.edges() 为true 而不管edge中的节点顺序，但是转换成list后就不行
                    Sample[j][k] = 1

        f2.write('\n')
        for line in Sample:
            for element in line:
                f.write(str(element))
                f.write(' ')
        f.write('\n')

    # print('Number of Atoms: ', ks)  # 多少个点，多少个ego-network  这里是多写了一个，matlab跑的时候要-1
    f.close()
    f2.close()
    print("行数",ks)

def run(size=20):
    '''
    采样data/原始网络们/ 目录下所有
    :param size: 采样网络大小
    :return:
    '''
    base_filename = "data\\原始网络们\\"
    file_list = showDir(base_filename)
    count = 0
    for each in file_list:
        filename = each
        name = filename.strip(".txt").strip(".gexf")
        filename = base_filename + filename
        print(name)
        sample(filename, name, size)
        count += 1
        print("进度完成{}/{}".format(str(count), str(len(file_list))))


if __name__ == '__main__':
    base_filename = "data\\原始网络们\\"
    file_list = showDir(base_filename)
    count = 0
    for each in file_list:
        filename = each
        name = filename.strip(".txt").strip(".gexf")
        filename = base_filename + filename
        print(name)
        sample(filename, name, 20)
        count += 1
        print("进度完成{}/{}".format(str(count),str(len(file_list))))

