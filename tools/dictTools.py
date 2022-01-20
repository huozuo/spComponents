'''
date:22.01.20
author:pmy
description: 适用于dict的tools
'''


def reverseDict(dict):
    '''
    将Dict的key value交换，返回仍是Dict
    return {v:k for k,v in dict.items()} # 只能解决value为单个变量的情况
    :param dict: Dict形式{k:[v1,v2,v3]}
    :return: {v1:[k],v2:[k],v3:[k]}
    '''
    newDict = {}
    for k,vs in dict.items():
        if isinstance(vs,list): # 列表时
            for v in vs:
                if v in newDict.keys():
                    newDict[v].append(k)
                else:
                    newDict[v] = [k]
        else:
            newDict[vs] = [k]

    return newDict
                    