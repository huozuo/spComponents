'''
date: 22.03.07
author: pmy
description: 原子平均度分布数据输出
'''
from spComponents.sparseRepresentation import networkInfo
from spComponents.tools import getFileName
import os
import pandas as pd
from spComponents.statistics.atom import *



# 读取所有原子

def getAtoms(name):
    '''
    获取原子网络
    :param name:
    :return:
    '''
    gInfo = networkInfo.NetworkInfo(name)
    atoms = Atoms(gInfo)
    return atoms

def averageDeg(atom):
    '''
    平均度
    :param atom:
    :return:
    '''
    return atom.number_of_edges() * 2 / atom.number_of_nodes()

def calc(atoms):
    '''
    计算当前网络原子平均度情况
    :param atoms:
    :return:
    '''
    res = {}
    for atom in atoms.atoms:
        try:
            ad = int(averageDeg(atom))
        except:
            continue
        if ad not in res.keys():
            res[ad] = 0
        res[ad] += 1
    return res

def runOne(name):
    atoms = getAtoms(name)
    res = calc(atoms)
    print(res)
    # 概率
    for k,v in res.items():
        # res[k] = round(v/atoms.num,3)
        res[k] = v/atoms.num
    # print(res)
    #从高到低来进行排序
    ##最大值
    maxDeg = max(res.keys())
    totalProb = 1
    for i in range(maxDeg+1):
        curProb = res[i] if i in res.keys() else 0
        totalProb -= curProb
        res[i] = totalProb

    # save(name,sorted(res.values(),reverse=True),"KSVD")
    #按照key值进行排序
    res = sorted(res.items(), key=lambda kv: (kv[0], kv[1]))
    # res = sorted(res.items(), key=lambda kv: kv[0])
    res = [v for k,v in res]
    return res


def run():
    '''
    获取所有的结果
    :param plotArrange:
    :return:
    '''
    basePath = "data/"
    files = getFileName.showDir(basePath)
    for file in files:
        print("####" + file + "####")
        print(runOne(file))
        print("")



def save(name,data,label):
    '''
    保存到对应的csv中
    （暂不能用）
    :param name:
    :param label:
    :return:
    '''
    data = [str(i) for i in data]
    data = {label:data}
    # 如果文件不存在，则创建
    path = "data/"+name+".xls"
    if not os.path.exists(path):
        open(path,'a')
    df = pd.DataFrame(data)
    writer = pd.ExcelWriter(path)
    df.to_excel(writer,index=False,sheet_name='Sheet1')
    print("save done")
