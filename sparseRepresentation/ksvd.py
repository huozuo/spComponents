'''
date: 21.12.04
author: pmy
func: 浮点数矩阵分解
note：自动读取data目录下的sample，进行分解
      引用matrixTools中的误差计算
version: v3
'''
import numpy as np
from sklearn import linear_model
import os
from ..tools import errorTools


def get_filename(base_filename):
    '''
    获取当前目录下的所有文件
    :param base_filename:
    :return:
    '''
    list = os.listdir(base_filename)
    try:
        list.remove("gexfs")
    except:
        pass
    return list

class KSVD(object):


    def __init__(self, n_components, max_iter=2,n_nonzero_coefs=None):
        """
        稀疏模型Y = DX，Y为样本矩阵，使用KSVD动态更新字典矩阵D和稀疏矩阵X
        :param n_components: 字典所含原子个数（字典的列数）
        :param max_iter: 最大迭代次数
        :param tol: 稀疏表示结果的容差
        :param n_nonzero_coefs: 稀疏度
        """
        self.dictionary = None
        self.sparsecode = None
        self.max_iter = max_iter
        self.n_components = n_components
        self.n_nonzero_coefs = n_nonzero_coefs

    def _initialize(self, y):
        """
        初始化字典矩阵
        """
        u, s, v = np.linalg.svd(y)
        self.dictionary = u[:, :self.n_components]

    def transformPos(self,d,x,index,thres=0.01):
        '''
        保证字典向量中正数大于负数
        :param d: 字典矩阵
        :param x: 稀疏码矩阵
        :param index: 索引
        :return:
        '''
        pos = 0
        neg = 0
        m = np.shape(d)[0]
        for i in range(m):
            if d[i][index] > thres: pos += 1
            elif d[i][index] <-1*thres: neg += 1

        if neg > pos: # 若字典中 有效负数大于有效正数
            d[:,index] = -d[:,index]
            x[index,:] = -x[index,:]


    def _update_dict(self, y, d, x):
        """
        使用KSVD更新字典的过程
        """
        print("original err",np.sum(y))
        for i in range(self.n_components):
            index = np.nonzero(x[i, :])[0]  #返回非0元素的索引，计数规则从0开始
            if len(index) == 0:
                continue

            d[:, i] = 0   #将字典d的第i列全部设为0
            r = (y - np.dot(d, x))[:, index]  #计算误差矩阵（为了保证编码矩阵稀疏，只选择编码中非0的索引）
            # e = np.linalg.norm(y - np.dot(d, x))
            e = errorTools.absError(y, d, x)
            print("err：" + str(e))  # for test
            u, s, v = np.linalg.svd(r, full_matrices=False)  #用svd的方法，来更新第i列字典和第i行的稀疏矩阵 这里会不收敛，用scipy来试一试 删去full_matrix试试
            # u,s,v = scipy.linalg.svd(r)

            # d[:, i] = (u[:, 0].T)  * s[0]# 使用左奇异矩阵的第一个列向量来更新di（这里为什么要转置呢，是不是有问题，不加转置也行）
            # x[i, index] = v[0, :]   # 奇异值第一个乘右奇异矩阵的第一个行向量来更新xi 这里进行了修改，将特征值移到了字典中

            ##test##
            # 这里实际没有任何的意义，就是将能量放在了稀疏码上，除此之外，没啥意义，所以无所谓运行哪一个
            # 使用左奇异矩阵的第0列更新字典
            d[:, i] = u[:, 0]
            # 使用第0个奇异值和右奇异矩阵的第0行的乘积更新稀疏系数矩阵
            for j, k in enumerate(index):
                x[i, k] = s[0] * v[0, j]
            ## test

            self.transformPos(d,x,i) # 进行正负转换

            # d[:, i] = (u[:, 0].T)  #使用左奇异矩阵的第一个列向量来更新di（这里为什么要转置呢，是不是有问题，不加转置也行）
            # x[i, index] =  v[0, :]*s[0]  #奇异值第一个乘右奇异矩阵的第一个行向量来更新xi 这里进行了修改，将特征值移到了字典中



        return d, x

    def fit(self, y):
        """
        KSVD迭代过程
        """
        self._initialize(y)  #初始化字典矩阵
        for i in range(self.max_iter):
            print("iter: "+str(i))
            x = linear_model.orthogonal_mp(self.dictionary, y, n_nonzero_coefs=self.n_nonzero_coefs)  #稀疏编码 似乎是根据y=dx，已知y和d，直接求解出x
            #达到优化目标，则结束，否则最大迭代
            self._update_dict(y, self.dictionary, x) #更新字典和稀疏编码  (有问题，这里返回不用接受的嘛，怎么就直接更新了)这里不是引用传参，哦这个似乎是不影响的，因为只需要字典，所以他这里每次都算x

        self.sparsecode = linear_model.orthogonal_mp(self.dictionary, y, n_nonzero_coefs=self.n_nonzero_coefs) #最后求解一次稀疏编码
        return self.dictionary, self.sparsecode

def run(dictNum=200):
    '''
    运行ksvd
    :param dictNum: 指定的最大字典列向量数 默认为200，可以修改
    :return:
    '''
    fileList = get_filename("data/")
    for name in fileList:
        if name =="gexfs":continue
        print("######" + name + "######")
        # name = "ca-AstroPh2"
        filename = "data/" + name + "/Sample_" + name + ".txt"
        y = np.loadtxt(filename)
        y = y.T
        print(y.shape)
        ksvd = KSVD(dictNum)
        print("++init++")
        dictionary, sparsecode = ksvd.fit(y)
        print("++done++")
        dic_name = "data/" + name + "/dic_Sample.txt"
        coef_name = "data/" + name + "/coef_Sample.txt"
        np.savetxt(dic_name, dictionary, fmt="%4f")
        np.savetxt(coef_name, sparsecode, fmt="%4f")
        # print("存储完毕")



if __name__ == '__main__':
    # im_ascent = scipy.misc.ascent().astype(np.float)
    #im_ascent = [[0,1,1,1,1,1],[1,0,0,0,0,0],[1,0,0,0,0,0],[1,0,0,0,0,0],[1,0,0,0,0,0],[1,0,0,0,0,0]]
    #im_ascent = np.array(im_ascent)
    fileList = get_filename("data")
    for name in fileList:
        print("######"+name+"######")
        # name = "ca-AstroPh2"
        filename = "data/"+name+"/Sample_"+name+".txt"
        y = np.loadtxt(filename)
        y = y.T
        print(y.shape)
        ksvd = KSVD(200)
        print("初始化完毕")
        dictionary, sparsecode = ksvd.fit(y)
        print("训练完毕")
        dic_name = "E:\\教研室\\实验室\\"+name+"\\dic_Sample.txt"
        coef_name = "E:\\教研室\\实验室\\"+name+"\\coef_Sample.txt"
        np.savetxt(dic_name, dictionary,fmt="%4f")
        np.savetxt(coef_name, sparsecode,fmt="%4f")
        print("存储完毕")

