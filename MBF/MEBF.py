'''
author:pmy
time:2020-10-16-9:40
last-edit:2021-11-05
function: 布尔矩阵分解
note: 在v0版本的基础上进行了1+1=1的改进，期望使得整体的误差更小
version:v1
location: spComponents
'''
from .expansion import *
from ..tools.processPool import ProcessPool
from ..tools.vecType import VecType


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
    n = np.shape(TEMP)[0]
    args = [(MAT, M1, Thres, j) for j in range(n)]
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

    B1 = M1[:, k]  # TEMP[j,0]是第j个数的行？这里不应该是列么，mark一下，感觉不大对，我咋感觉应该是1呢，我真感觉是1 #和上面的区别
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

def MEBF(Thres,proNum,MAT,DIM=200,COVER=0.995):
    '''
    :param Thres:  论文中的t，作为衡量是否能够覆盖的阈值 高了则会覆盖过少，低了则会覆盖过多
    :param proNum: 进程数
    :param MAT: 输入的矩阵
    :param DIM:  patterns的个数 也是希望得到子矩阵的个数
    :param COVER: 这个我暂时没看懂啥意思
    :return:
    '''
    # 进程池
    # cpuCores = int(os.cpu_count()/2)
    # print("start process ",cpuCores)
    # pool = ProcessPoolExecutor(cpuCores)
    proPool = ProcessPool(proNum)

    if min(np.shape(MAT))<DIM: #目标patterns的个数一定要小于矩阵的维度，这个显然
        DIM=min(np.shape(MAT))

    M1 = MAT #M1作为residual matrix
    SUM = np.sum(MAT) #计算一下原矩阵的1的个数

    MAT_B = np.empty([np.shape(MAT)[0],0]) #论文中的A*
    MAT_C = np.empty([0, np.shape(MAT)[1]])#给定shape，返回一个多元数组 然后进行修改添加？
    e = np.sum(M1)  # 本轮矩阵的1个数
    # print("初始误差为："+str(e)) #

    # 循环条件：字典列向量数达到DIM，或者1的个数足够少（剩余1的个数达到（1-cover）*初始1的个数）
    while np.sum(M1)>(1-COVER)*SUM and min(MAT_B.shape)<DIM:#COVER值只在这里出现
        e= np.sum(M1) # 本轮矩阵的1个数
        B1 = np.zeros(np.shape(M1)[0]) #对于MAT_B的列向量 初始化 全0
        B1_use = B1
        B2 = np.zeros(np.shape(M1)[1]) #对于MAT_C的行向量 初始化 全0
        B2_use = B2

        COL = np.sum(M1, axis=0) #列和 是一个向量
        ROW = np.sum(M1, axis=1) #行和 也是一个向量

        e1 = e
        ### start with column
        medianCol = np.median(COL[COL>0]) # 所有列和的中位数
        if medianCol>1: #从非零的列中找中位数值 （中位数都不大于1，就没有意义了）
            mCol = min(COL[COL>=medianCol]) # 找到最接近中位数的数的列们
            TEMP=np.argwhere(COL==mCol) #返回满足条件的索引 是个二维数组，第二维对于向量是一个元素
            e2,B1,B2 = findMaxRect(MAT,M1,Thres,proPool,TEMP,VecType.col)
            if e1 > e2:
                B1_use = B1
                B2_use = B2
                e1 = e2

        ### start with row  这里的逻辑应该一样，和上面差不多 只是这里用的是ROW
        medianRow = np.median(ROW[ROW>0])
        if medianRow>1:
            mRow = min(ROW[ROW >= medianRow])
            TEMP = np.argwhere(ROW==mRow)
            e2,B1,B2 = findMaxRect(MAT, M1, Thres, proPool, TEMP, VecType.row)
            if e1 > e2:
                B1_use = B1
                B2_use = B2
                e1 = e2

        #weak signal detection algorithm 在中位数行列expansion失效时执行
        if((e-e1)/e<0.01):
            COL_order=np.argsort(COL)[::-1] #返回 按照sum和最大来排序的索引
            ROW_order=np.argsort(ROW)[::-1]

            B1 = np.zeros(np.shape(M1)[0])
            B2 = np.zeros(np.shape(M1)[1])

            ### start from COL
            B1[(M1[:,COL_order[0]]+M1[:,COL_order[1]]==2)]=1 #把1最稠密的两列给叠加起来，然后来构成新的pattern
            expansionCol(M1,MAT,B1,B2,Thres)
            e2 = error(M1,B1,B2)

            if e1>e2:
                B1_use = B1
                B2_use = B2
                e1 = e2

            ### start from ROW
            B1 = np.zeros(np.shape(M1)[0])
            B2 = np.zeros(np.shape(M1)[1])
            B2[(M1[ROW_order[0],] + M1[ROW_order[1],] == 2)] = 1
            expansionRow(M1, MAT, B1, B2, Thres)
            e2 = error(M1,B1,B2)

            if e1> e2:
                B1_use = B1
                B2_use = B2
                e1 = e2

        # 如果处理之后还等于0， 则直接brek
        if e1==np.sum(M1):
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


