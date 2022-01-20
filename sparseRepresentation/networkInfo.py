'''
date:22.01.20
author:pmy
description:根据名称获取字典、稀疏码矩阵、采样矩阵、indexs矩阵、字典与原子的映射
'''
from ..tools import getFileName
from numpy import *
import networkx as nx
import numpy as np

class NetworkInfo:
    def __init__(self,name):
        '''
        data/name
        要求其中有index，dict，coef
        :param name:
        '''
        # 读取字典矩阵，稀疏码矩阵
        self.dict = self.getMatrix("data/" + name + "/dic_Sample.txt")
        self.coef = self.getMatrix("data/" + name + "/coef_Sample.txt")
        self.index = self.getIndex(name)
        self.atom2dict = self.getAtom2dict(name) # {原子序号：字典向量序号}
        self.name = name
        self.atomNum = self.getAtomNum()
        self.atoms = self.getAtoms()


    def getAtomNum(self):
        '''
        获得指定目录下的原子个数
        :return:
        '''
        fileList = getFileName.showDir("data/" + self.name + "/")
        cnt = getFileName.calcFileNums(fileList, 'Atom_\w+.gexfs')
        return cnt

    def getAtoms(self):
        '''
        获得指定目录下的所有原子网络
        :return:
        '''
        atoms = []
        for i in range(1,self.atomNum+1):
            atomName = "data/" + self.name + "/Atom_" + str(i) + ".gexfs"
            atoms.append(nx.read_gexf(atomName))
        return atoms

    def getMatrix(self,filename):
        return np.loadtxt(filename)

    def getIndex(self,name):
        '''
        根据name，获取实际的ego-network的节点情况
        :param name:
        :return:
        '''
        filename = "data/" + name + "/Index_" + name + ".txt"
        index = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                names = line.strip('\n').split(',')
                names.remove('')
                names = [int(name) for name in names]
                index.append(names)
        f.close()
        return index

    def getAtom2dict(self,name):
        '''
        根据字典矩阵来获取atom-dict的映射 {atom : dict}
        :param name:
        :return:
        '''
        f = open("data/" +name+ "/dic_Sample.txt")  # 字典文件的路径
        line = f.readline()
        G = []  # 存储字典的值
        # Num_Atom = 200  #字典矩阵的列数 即原子的个数
        # Atom_Len = subnet_size   #字典矩阵的行数的开平方 即原子的size
        dic_matrix = self.dict
        Atom_Len = int(sqrt(dic_matrix.shape[0]))
        Num_Atom = dic_matrix.shape[1]  # 直接覆盖

        atom2Dict = {}
        for i in range(Num_Atom):
            atom2Dict[i + 1] = []  # 初始化，最多这么多个

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
        for i in range(len(G)):  # 对每个列向量进行遍历，分别生成原子
            Sample = self.dict2atom(G[i])
            # 进行存储
            In_F = False
            if Sample_Set == []:  # 第一个原子直接存储
                Sample_Set.append(Sample)
                atom2Dict[len(Sample_Set)].append(i)  # 第一个向量就是1号原子
                continue
            # 去同构
            for j in range(len(Sample_Set)):
                element = Sample_Set[j]
                if nx.is_isomorphic(Sample, element):
                    atom2Dict[j + 1].append(i)  # 第i个列向量放到第j+1个原子里去
                    In_F = True
            if not In_F:
                Sample_Set.append(Sample)
                atom2Dict[len(Sample_Set)].append(i)  # 当前第j个原子加入i

        # 删去为空的原子
        atom2DictCopy = atom2Dict.copy()
        for key in atom2DictCopy:
            if len(atom2Dict[key]) == 0:
                atom2Dict.pop(key)


        return atom2Dict

    def dict2atom(self,dict):
        '''
        将dict转换成atom，这样适合进行比对
        :param dict: 字典向量
        :return:
        '''
        Atom_Len = int(sqrt(len(dict)))
        g = nx.Graph()
        for j in range(Atom_Len):
            # for k in range(j + 1, Atom_Len):
            for k in range(Atom_Len):  ## 问题出在这
                if j == k: continue
                t = Atom_Len * j + k
                if dict[t] > 0.01:  # 这里要改的 TODO
                    g.add_edge(j, k)

        return g