'''
author:pmy
time:2020-10-16-9:40
last-edit:2021-11-05
function: 布尔矩阵分解
note: 在v0版本的基础上进行了1+1=1的改进，期望使得整体的误差更小
version:v1
location: spComponents
'''



import numpy as np
from expansion import *


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

def MEBF(Thres,MAT,DIM=200,COVER=0.995):
    '''

    :param Thres:  论文中的t，作为衡量是否能够覆盖的阈值 高了则会覆盖过少，低了则会覆盖过多
    :param MAT: 输入的矩阵
    :param DIM:  patterns的个数 也是希望得到子矩阵的个数
    :param COVER: 这个我暂时没看懂啥意思
    :return:
    '''
    if min(np.shape(MAT))<DIM: #目标patterns的个数一定要小于矩阵的维度，这个显然
        DIM=min(np.shape(MAT))

    M1 = MAT #M1作为residual matrix
    SUM = np.sum(MAT) #计算一下原矩阵的1的个数

    MAT_B = np.empty([np.shape(MAT)[0],0]) #论文中的A*
    MAT_C = np.empty([0, np.shape(MAT)[1]])#给定shape，返回一个多元数组 然后进行修改添加？
    e = np.sum(M1)  # 本轮矩阵的1个数
    print("初始误差为："+str(e)) #

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
        if np.median(COL[COL>0])>1: #从非零的列中找中位数值 （中位数都不大于1，就没有意义了）
            # t = np.median(COL[COL>0]) #for test
            TEMP=np.argwhere(COL==min(COL[COL>=np.median(COL[COL>0])])) #返回满足条件的索引 是个二维数组，第二维对于向量是一个元素
                                                                        #条件为：col= col中大于均值的的最小值（略大于中位数）
                                                                        #意为：找到最接近中位数的数的列们
            if np.shape(TEMP)[0]==1: #如果这个条件的只有1个数 这很正常
                B1=M1[:,TEMP[0,0]] #B1是中位数列
                # 计算M1矩阵中与B1相似超过阈值的列有多少
                # TODO 修改这里 1 在这里进行expansion，并进行阈值的衡量
                expansionCol(M1,MAT,B1,B2,Thres)
                #计算误差
                e2 = error(M1,B1,B2)

                if e1>e2: #如果B1，B2的1的数量更多，那么就更新B1_use和B2_use
                    B1_use=B1
                    B2_use=B2
                    e1=e2 #这个标准是逐渐提高的

                B1 = np.zeros(np.shape(M1)[0])
                B2 = np.zeros(np.shape(M1)[1]) #这里相当于初始化，来重新计算行的

            else: #中位数列不只一个
                f = np.shape(TEMP)[0]
                for j in range(f): #对每列进行遍历
                    B1=M1[:,TEMP[j,0]] #TEMP[j,0]是第j个数的行？这里不应该是列么，mark一下，感觉不大对，我咋感觉应该是1呢，我真感觉是1 #和上面的区别
                                       #上面也是0.···不知道为啥，可能得看算法
                    expansionCol(M1, MAT, B1, B2, Thres)
                    e2 = error(M1,B1,B2)

                    if e1 > e2:
                        B1_use = B1
                        B2_use = B2
                        e1 = e2

                    B1 = np.zeros(np.shape(M1)[0])
                    B2 = np.zeros(np.shape(M1)[1])

        #如此得到的是B1_use和B2_use ，然后C1也更新了

        ### start with row  这里的逻辑应该一样，和上面差不多 只是这里用的是ROW
        if np.median(ROW[ROW>0])>1:
            TEMP = np.argwhere(ROW == min(ROW[ROW >= np.median(ROW[ROW > 0])]))
            if np.shape(TEMP)[0] == 1:
                B2 = M1[TEMP[0,0],:]
                expansionRow(M1, MAT, B1, B2, Thres)
                e2 = error(M1,B1,B2)

                if e1 > e2:
                    B1_use = B1
                    B2_use = B2
                    e1 = e2

                B1 = np.zeros(np.shape(M1)[0])
                B2 = np.zeros(np.shape(M1)[1])
            else:
                for j in range(np.shape(TEMP)[0]):
                    B2 = M1[TEMP[j, 0], :]
                    expansionRow(M1, MAT, B1, B2, Thres)
                    e2 = error(M1,B1,B2)

                    if e1 > e2:
                        B1_use = B1
                        B2_use = B2
                        e1 = e2

                    B1 = np.zeros(np.shape(M1)[0])
                    B2 = np.zeros(np.shape(M1)[1])

        #weak signal detection algorithm 在中位数行列expansion失效时执行
        # 这里我记不清是True还是其他条件了，啧啧啧，其实可以改为flag，如果上面的e1>e2，就执行，不然蛮浪费时间的其实
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
            print("无法误差下降啦")
            break
        else:#确实更新了，所以这里进行修正矩阵
            M1 = M1 - np.outer(B1_use,B2_use) #减去subMatrix
            M1[M1<0] = 0 #减法可能会造成-1，那么置零
            B1_use=B1_use.reshape(B1_use.shape[0],1)
            B2_use=B2_use.reshape(1,B2_use.shape[0])
            MAT_B = np.concatenate((MAT_B, B1_use), axis=1)#矩阵的拼接 所以前面是empty（0）就可以接受了
            MAT_C = np.concatenate((MAT_C, B2_use), axis=0)

            # print("本轮误差是："+str(e2))

    return MAT_B,MAT_C


