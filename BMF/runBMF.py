'''
date: 21.11.05
author: pmy
function: 运行布尔矩阵分解
'''

from .BMF import BMF
from ..tools.getFileName import showDir
from ..tools.errorTools import *
from ..tools.loadTools import *
from ..tools.saveTools import *


def factorization(matrix,proNum,Thres=0.95,DIM=150):
    '''
    输入矩阵
    进行布尔矩阵分解
    返回分解得到的字典以及稀疏码
    并且进行误差的评估
    :param matrix: 矩阵
    :param proNum: 进程数
    :param Thres: expansion的阈值
    :return: 字典矩阵，稀疏码矩阵，并打印误差结果
    '''
    dict,coef = BMF(Thres,proNum,matrix,DIM=DIM)
    # error(matrix,dict,coef)
    return dict,coef

def runOne(name,Thres,proNum):
    '''
    输入name，阈值，运行MBF方法
    存储MBF返回的字典矩阵和稀疏码矩阵
    :param name:
    :param Thres:
    :return:
    '''
    matrix = loadSample(name)
    dict,coef = factorization(matrix=matrix,proNum=proNum,Thres=Thres)
    #存储dict，coef
    save(name,dict,coef)

    # print("##########分解完毕##########")

def run(Thres=0.95,proNum=6):
    '''
    runAll
    :param filename:
    :return:
    '''
    for name in showDir("data/"):
        if name =="gexfs":continue
        print("########" + name + "########")
        runOne(name, Thres,proNum)
    print("done")



if __name__=="__main__":
    # matrix = np.array(6
    #     [[1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0],
    #      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, ],
    #      [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, ], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    #      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0]])
    # BMF(matrix,0.85)
    # name = "ca-AstroPh2"
    # print(name)
    # run(name,0.92)
    # name = "roadNet-CA2"
    # run(name,0.95)
    run()


