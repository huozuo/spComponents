'''
date:22.02.04
author:pmy
description: numpy处理相关工具
'''
import numpy as np

def reshapeVec(vec):
    '''
    将矩阵转换成向量
    :param vec:
    :return:
    '''
    return vec.reshape(-1,)


if __name__=="__main__":
    m = np.zeros((3,3))
    m[0][1] = 1
    m[1][0] = 1
    m[2][2] = 1
    print(m)

    m = reshapeVec(m)
    print(m)
    print(m[0])

