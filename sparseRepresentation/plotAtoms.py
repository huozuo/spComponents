'''
date: 22.01.04
author: pmy
description: 画出某一路径下的所有原子图像
note: 1. plt.subplot(xyd),x 为行数，y为列数， d为多少个 每个数，最多不能超过10，超过10，就有歧义，没法识别简写模式
      2. 画图时，先nx.draw 来画结果，然后再画节点属性以及边属性，这些属性都要是字典形式，通过nx.get_attributes来获取
'''
import matplotlib.pyplot as plt
import networkx as nx
from ..tools import getFileName


def run(plotArrange=241,nodeLabel=True,edgeLabel=True):
    '''
    画所有图，只调用一次就好了
    :param plotArrange:
    :return:
    '''
    basePath = "data/"
    files = getFileName.showDir(basePath)
    for file in files:
        try:
            runOne(file,plotArrange,nodeLabel,edgeLabel)
        except:
            print(file+"plot failed")


def runOne(name,plotArrange,nodeLabel=True,edgeLabel=True):
    '''
    主方法
    :param name:
    :param plotArrange: 画图排列的方式 行数、列数、第几个，此处任意数字不能超过10
    :return:
    '''
    # 读取目录下的所有Atom_文件数量
    basePath = "data/"+name+"/"
    filePaths = getFileName.getSpecPaths(basePath,"Atom")
    if len(filePaths)==0: return
    print("plot "+name)
    atoms = readAtoms(filePaths)

    # 行数、列数
    row = plotArrange//100
    col = plotArrange//10 - 10*row
    total = row*col

    # 挨个的画图
    for i in range(len(atoms)):
        seq = i%total
        plotAtom(atoms[i],plotArrange+seq,nodeLabel,edgeLabel)
        if seq == total-1 or i==len(atoms)-1:
            f = plt.gcf()
            f.set_size_inches(18, 10) # 图像的尺寸
            plt.savefig(basePath+"atomFig_"+str(int(i//total))+".png",dpi=100)
            plt.close()
    # print("=====plot done=====")


def plotAtom(atom,id,nodeLabel=True,edgeLabel=True):
    '''
    绘制单个原子
    :param atom: networkx gexfs
    :param nodeLabel: 控制绘制节点标签
    :param edgeLabel: 控制绘制边标签
    :return:
    '''
    plt.subplot(id)
    # pos = nx.spring_layout(atom)
    pos = nx.kamada_kawai_layout(atom)
    plt.rcParams['figure.figsize']=(10,6)
    nx.draw(atom,pos,node_size=2000,edge_cmap=plt.cm.Blues)
    # nx.draw(atom,pos,node_size=12000,edge_cmap=plt.cm.Blues)
    if nodeLabel:
        node_labels = nx.get_node_attributes(atom, 'label')
        nx.draw_networkx_labels(atom, pos, labels=node_labels,font_color='w')
        # nx.draw_networkx_labels(atom, pos, labels=node_labels,font_size=80,font_color='w')
    if edgeLabel:
        edge_labels = nx.get_edge_attributes(atom, 'label')
        nx.draw_networkx_edge_labels(atom, pos, edge_labels=edge_labels)
        # nx.draw_networkx_edge_labels(atom, pos, edge_labels=edge_labels,font_size=50)
    plt.tight_layout(pad=0)


def readAtoms(paths):
    '''
    获取全部路径下的atoms
    :param paths: atom 路径列表
    :return:
    '''
    res = []
    for path in paths:
        try:
            res.append(nx.read_gexf(path))
        except:
            print("read "+path+" err")
    return res

def plotNetworks(atoms,plotArrange=241):
    '''
    主方法
    :param name:
    :param plotArrange: 画图排列的方式 行数、列数、第几个，此处任意数字不能超过10
    :return:
    '''
    # 行数、列数
    row = plotArrange//100
    col = plotArrange//10 - 10*row
    total = row*col

    # 挨个的画图
    for i in range(len(atoms)):
        seq = i%total
        plotAtom(atoms[i],plotArrange+seq)
        if seq == total-1 or i==len(atoms)-1:
            f = plt.gcf()
            f.set_size_inches(18, 10) # 图像的尺寸
            plt.savefig("data/"+"Fig_"+str(int(i//total))+".png",dpi=400,bbox_inches='tight', pad_inches=0.01)
            plt.close()
    print("=====plot done=====")

if __name__=="__main__":
    # runOne("wn18_1308")
    pass