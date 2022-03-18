'''
date:2022.02.04
author:pmy
function: 布尔矩阵分解
            实现多进程
            实现剪枝
            相比之前版本，运行速度降低99%
'''
from .expansion import *
from ..tools.processPool import ProcessPool
from ..tools.vecType import VecType
from .matrixEncode import MatrixEncode

def findMinErr(data):
    '''
    找到最小误差的数据，返回索引
    :param data:
    :return:
    '''
    min = 1000000
    minIndex = 0
    for j in range(len(data)):
        if min >= data[j][0]:
            min = data[j][0]
            minIndex = j
    return minIndex


def findMaxRect(MAT,M1,Thres,proPool,TEMP,vecType):
    '''
    寻找最大矩形
    :param MAT: 初始矩阵
    :param M1: 残差矩阵
    :param Thres: expansion的阈值
    :param proPool: 进程池
    :param TEMP: 中位向量索引
    :param vecType: 行向量or列向量
    :return:
    '''
    n = len(TEMP)
    args = [(MAT, M1, Thres, TEMP[j]) for j in range(n)]
    if vecType == VecType.row:
        res = list(proPool.run(findMaxRectByRow, args))
    else:
        res = list(proPool.run(findMaxRectByCol, args))

    # 找到误差最小的那一组数据
    i = findMinErr(res)
    e1 = res[i][0]  # 最小误差
    B1_use = res[i][1]  # 最小误差对应的字典向量
    B2_use = res[i][2]  # 最小误差对应的稀疏码向量
    return e1,B1_use,B2_use


def findMaxRectByCol(args):
    '''
    根据列来寻找最大全1矩形
    :param args:
    :return:
    '''
    MAT = args[0]
    M1 = args[1]
    Thres = args[2]
    k = args[3]

    B1 = M1[:, k]  # 基列
    B2 = np.zeros(np.shape(M1)[1])
    expansionCol(M1, MAT, B1, B2, Thres)
    e = error(M1, B1, B2)
    return (e,B1,B2) # 一股脑全部返回

def findMaxRectByRow(args):
    '''
    根据行来寻找最大全1矩形
    :param args:
    :return:
    '''
    MAT = args[0]
    M1 = args[1]
    Thres = args[2]
    k = args[3]

    B1 = np.zeros(np.shape(M1)[0])
    B2 = M1[k, :]
    expansionRow(M1, MAT, B1, B2, Thres)
    e = error(M1, B1, B2)
    return (e,B1,B2)

def error(residuMatrix, columnVector,rowVector):
    '''
    计算当前轮次之后的剩余误差，原残差矩阵-向量之积，然后计算矩阵之和（非绝对值）
    :param residuMatrix: 残差矩阵，不能修改
    :param columnVector: 列向量，patterns
    :param rowVector: 行向量 覆盖情况
    :return: int型的误差值
    '''
    e_matrix = residuMatrix - np.outer(columnVector,rowVector)
    e_matrix[e_matrix<0] =0 #将负数置0，因为我上面的减法就是这样操作的，需要和那个一样，不然就没有意义了
    e = np.sum(e_matrix)
    return e

def BMF(Thres,proNum,MAT,DIM=200,COVER=0.995,breakThres=0.01):
    '''
    :param Thres:  向量相似的阈值
    :param proNum: 进程数
    :param MAT: 输入的矩阵
    :param DIM:  patterns的个数 也是希望得到子矩阵的个数
    :param COVER: 迭代终止的误差条件
    :return:
    '''
    # 进程池
    proPool = ProcessPool(proNum)

    if min(np.shape(MAT))<DIM: #目标patterns的个数要小于矩阵的维度
        DIM=min(np.shape(MAT))

    m,n = np.shape(MAT)

    M1 = MAT #M1残差矩阵
    SUM = np.sum(MAT) #原矩阵的1的个数
    # MAT_B = np.empty([np.shape(MAT)[0],0]) #字典矩阵D
    MAT_B = np.empty([m,0]) #字典矩阵D
    MAT_C = np.empty([0, n]) #稀疏码矩阵
    # MAT_C = np.empty([0, np.shape(MAT)[1]]) #稀疏码矩阵

    # 循环条件：字典列向量数达到DIM，或者1的个数足够少（剩余1的个数达到（1-cover）*初始1的个数）
    while np.sum(M1)>(1-COVER)*SUM and min(MAT_B.shape)<DIM:#COVER值只在这里出现
        matrixCode = MatrixEncode(M1) # 矩阵编码

        e= np.sum(M1) # 本轮矩阵的1个数
        B1 = np.zeros(m) #对于MAT_B的列向量 初始化 全0
        B1_use = B1
        B2 = np.zeros(n) #对于MAT_C的行向量 初始化 全0
        B2_use = B2

        # print(e)

        COL = np.sum(M1, axis=0) #列和 是一个向量
        ROW = np.sum(M1, axis=1) #行和 也是一个向量

        e1 = e
        ### 寻找最大全1矩形
        ## start with col
        medianCol = np.median(COL[COL>0]) # 所有列和的中位数
        if medianCol>1: #从非零的列中找中位数值 （中位数都不大于1，就没有意义了）
            mCol = min(COL[COL>=medianCol]) # 找到最接近中位数的数的列和
            TEMP=np.argwhere(COL==mCol) #返回满足条件的索引 是个二维数组，第二维对于向量是一个元素
            TEMP = matrixCode.unique(TEMP,VecType.col) # 去重
            # 当前 中位列数过多，导致时间复杂度过高，则跳过
            if len(TEMP) < 500:
                e2,B1,B2 = findMaxRect(MAT,M1,Thres,proPool,TEMP,VecType.col)
                if e1 > e2:
                    B1_use = B1
                    B2_use = B2
                    e1 = e2

        ### start with row
        medianRow = np.median(ROW[ROW>0])
        if medianRow>1:
            mRow = min(ROW[ROW >= medianRow])
            TEMP = np.argwhere(ROW==mRow)
            TEMP = matrixCode.unique(TEMP, VecType.row) # 去重
            if len(TEMP)<500:
                e2,B1,B2 = findMaxRect(MAT, M1, Thres, proPool, TEMP, VecType.row)
                if e1 > e2:
                    B1_use = B1
                    B2_use = B2
                    e1 = e2

        #weak signal detection algorithm 在中位数行列expansion失效时执行
        if((e-e1)/e<breakThres):
            COL_order=np.argsort(COL)[::-1] #返回 按照sum和最大来排序的索引
            ROW_order=np.argsort(ROW)[::-1]
            B1 = np.zeros(m)
            B2 = np.zeros(n)

            ### start from COL
            B1[(M1[:,COL_order[0]]+M1[:,COL_order[1]]==2)]=1 #把1最稠密的两列给叠加起来，然后来构成新的pattern
            expansionCol(M1,MAT,B1,B2,Thres)
            e2 = error(M1,B1,B2)
            if e1>e2:
                B1_use = B1
                B2_use = B2
                e1 = e2

            ### start from ROW
            B1 = np.zeros(m)
            B2 = np.zeros(n)
            B2[(M1[ROW_order[0],] + M1[ROW_order[1],] == 2)] = 1
            expansionRow(M1, MAT, B1, B2, Thres)
            e2 = error(M1,B1,B2)
            if e1> e2:
                B1_use = B1
                B2_use = B2
                e1 = e2

        # 如果处理之后还等于0， 则直接brek
        if ((e-e1)/e<0.01):
            # print("无法误差下降啦")
            break
        else:#确实更新了，所以这里进行修正矩阵
            M1 = M1 - np.outer(B1_use,B2_use) #减去subMatrix
            M1[M1<0] = 0 #减法可能会造成-1，那么置零
            B1_use=B1_use.reshape(B1_use.shape[0],1)
            B2_use=B2_use.reshape(1,B2_use.shape[0])
            MAT_B = np.concatenate((MAT_B, B1_use), axis=1)#矩阵的拼接 所以前面是empty（0）就可以接受了
            MAT_C = np.concatenate((MAT_C, B2_use), axis=0)

    return MAT_B,MAT_C


