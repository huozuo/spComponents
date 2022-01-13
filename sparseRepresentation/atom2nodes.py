'''
date: 2021-11-11
author: pmy
func: convert atom to nodes
modification：将一个原子与多个向量之间的同构考虑进来，使得最终获得的实际节点顺序完全正确
修改在于dict2vnodes这个方法
version: v4
location: spComponents
'''
from numpy import *
import networkx as nx
import numpy as np
from ..tools import getFileName


class Atom2Nodes():

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
        self.curNum = 0

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

    def dict2vnodes(self,dict):
        '''
        根据dict向量，确定虚拟节点的序号
        不存在的虚拟节点序号为-1，下面的方法自动忽略
        modification：根据原子来定义顺序，之前的虚拟节点不变，然后通过映射关系来修改vnodes
        :param dict:
        :return:
        '''
        n = int(sqrt(len(dict))) # 自我中心网络的size
        atomNx = self.atoms[self.curNum-1] # 获取当前的nx network
        nodes = list(atomNx.nodes)
        nodes = sorted([int(node) for node in nodes])
        # 将-1放到4和7之间，比如这个就放两个
        ans = []
        for i in range(0, len(nodes)):
            # print(i) # for test
            dVal = nodes[0] - 0 if i==0 else nodes[i] - nodes[i - 1] - 1
            for j in range(dVal): ans.append(-1)
            ans.append(nodes[i])
        if len(nodes)>0:
            for i in range(n-nodes[len(nodes)-1]-1): ans.append(-1) # 将最后的补齐

        # 获取映射关系
        dictNum = len(self.atom2dict[self.curNum])

        if dictNum >1: # 当原子对应字典数量只有1时，不用同构映射, 即不用任何修改
            dictNx = self.dict2atom(dict)
            GM = nx.isomorphism.GraphMatcher(atomNx,dictNx)
            if not GM.is_isomorphic():# 必须要先is_isomorphic 再获取mapping，不然没有结果
                print("error: dict doesnt match with atom")
            mapping = GM.mapping # 原子中的id是str，所以这里需要针对性的str一下

            mapping["-1"] = -1 #将-1纳入，这样下面就不用再进行if判断了

            # 进行替换
            for i in range(len(ans)): ans[i] = mapping[str(ans[i])] # 注意这里的键是str

        return ans

    def vnodes2nodes(self,vnodes,i):
        '''
        根据index[i]来获取vnodes对应的实际节点
        这里不用++，因为不用和实际节点对应，只是和
        :param vnodes:
        :return:
        '''
        nodes = []
        index = self.index[i]
        for vnode in vnodes:
            if vnode==-1: nodes.append(-1) # -1跳过
            else: nodes.append(index[vnode])

        return nodes

    def coef2egoNetworks(self,coef):
        '''
        根据coef确定ego-networks
        :param coef:
        :return:
        '''
        res = np.nonzero(coef)[0] #列不为0的位置

        return res

    def dict2nodes(self,i):
        '''
        根据传入的dict向量的索引，找到对应的稀疏码
        并根据当前的字典向量情况，确定虚拟节点情况
        根据稀疏码找到对应的ego-network
        根据ego-network找对应index，确定实际节点情况
        :param index:
        :return:
        '''
        dict = self.dict[:,i] #当前字典向量 改好了
        coef = self.coef[i,:] #当前稀疏码向量
        vnodes = self.dict2vnodes(dict) #确定当前虚拟节点
        networks = self.coef2egoNetworks(coef) #确定涉及哪些ego-networks
        nodes = []
        for network in networks:
            nodes += self.vnodes2nodes(vnodes,network)

        return nodes

    def atom2nodes(self,atomIndex):
        '''
        根据atom的序号，确定nodes的情况
        :param atomIndex:
        :return:
        '''
        nodes = []
        dictIndexs = self.atom2dict[atomIndex]
        for dictIndex in dictIndexs:
            nodes += self.dict2nodes(dictIndex)

        return nodes

    def getAllnodes(self):
        '''
        在num范围内，获取所有atom与nodes的映射关系
        :param num:
        :return:
        '''
        res = {}
        for i in range(1,self.atomNum+1):
            # if i == 97: continue
            # print(i)
            self.curNum = i # 将当前的curNum设置成atomNum 这样就可以用的上
            res[i] = self.atom2nodes(i)
        # self.curNum = 97
        # res = self.atom2nodes(97)
        #存储结果
        self.saveData(res)

    def saveData(self,data):
        '''
        将nodes存储起来
        :param data:
        :return:
        '''
        # print("开始存储")
        fileName = "data/" + self.name + "/atom2nodes.txt"
        f = open(fileName, 'w', encoding="UTF-8")
        for key in data.keys():
            f.write("atom:" + str(key) + "\n")
            f.write("node:")
            for each in data[key]:
                f.write(str(each) + " ")
            f.write("\n")
        f.close()
        # print("存储完毕")

def run():
    # atom2nodes = Atom2Nodes(name)
    # atom2nodes.getAllnodes()
    fileList = getFileName.showDir("data/")
    for file in fileList:
        if file == "gexfs": continue
        print(file)
        Atom2Nodes(file).getAllnodes()
    print("done")

if __name__=="__main__":
    name = "roadNet-CA2"
    print(name)
    test = Atom2Nodes(name)
    test.getAllnodes()


