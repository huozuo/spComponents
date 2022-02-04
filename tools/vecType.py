'''
date: 22.02.04
author:pmy
description: 向量类型枚举
'''
from enum import Enum

class VecType(Enum):
    '''
    向量类型
    '''
    row = 0
    col = 1