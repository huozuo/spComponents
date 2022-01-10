'''
date: 22.01.04
author: pmy
description: 画出某一路径下的所有原子图像
note: 1. plt.subplot(xyd),x 为行数，y为列数， d为多少个 每个数，最多不能超过10，超过10，就有歧义，没法识别简写模式
      2. 画图时，先nx.draw 来画结果，然后再画节点属性以及边属性，这些属性都要是字典形式，通过nx.get_attributes来获取
'''
import matplotlib.pyplot as plt
import networkx as nx
import spComponents
from tqdm import tqdm

def run(plotArrange=241):
    '''
    画所有图，只调用一次就好了
    :param plotArrange:
    :return:
    '''
    basePath = "data/"
    files = spComponents.tools.getFileName.showDir(basePath)
    for file in tqdm(files):
        try:
            runOne(file,plotArrange)
        except:
            print(file+": 绘制失败")


def runOne(name,plotArrange):
    '''
    主方法
    :param name:
    :param plotArrange: 画图排列的方式 行数、列数、第几个，此处任意数字不能超过10
    :return:
    '''
    # 读取目录下的所有Atom_文件数量
    basePath = "data/"+name+"/"
    filePaths = spComponents.tools.getFileName.getSpecPaths(basePath,"Atom")
    if len(filePaths)==0: return
    print("开始绘制："+name)
    atoms = readAtoms(filePaths)

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
            plt.savefig(basePath+"atomFig_"+str(int(i//total))+".png",dpi=100)
            plt.close()
    print("=====绘制完成=====")


def plotAtom(atom,id):
    '''
    绘制单个原子
    :param atom: networkx gexf
    :return:
    '''
    plt.subplot(id)
    pos = nx.spring_layout(atom)
    nx.draw(atom,pos)
    node_labels = nx.get_node_attributes(atom, 'label')
    nx.draw_networkx_labels(atom, pos, labels=node_labels)
    edge_labels = nx.get_edge_attributes(atom, 'label')
    nx.draw_networkx_edge_labels(atom, pos, edge_labels=edge_labels)


def readAtoms(paths):
    '''
    获取全部路径下的atoms
    :param paths: atom 路径列表
    :return:
    '''
    res = []
    for path in paths:
        res.append(nx.read_gexf(path))
    return res


if __name__=="__main__":
    runOne("wn18_1308")
