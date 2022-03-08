'''
date: 22.03.07
author: pmy
description: 原子个数，最大尺寸，平均尺寸（节点数），平均度均值
'''
from spComponents.sparseRepresentation import networkInfo
from spComponents.tools import getFileName
from spComponents.statistics.atom import *


def runOne(name):
    print("####"+name+"####")
    gInfo = networkInfo.NetworkInfo(name)
    atoms = Atoms(gInfo)
    maxSize,avgSize = size(atoms)
    avgDeg = getAvgDeg(atoms)
    print("原子个数：",atoms.num)
    print("最大尺寸：",maxSize)
    print("平均尺寸：",avgSize)
    print("平均度均值：",avgDeg)

def run():
    '''
    获取所有的结果
    :param plotArrange:
    :return:
    '''
    basePath = "data/"
    files = getFileName.showDir(basePath)
    for file in files:
        if ".xls" in file: continue
        runOne(file)



def size(atoms):
    '''
    原子尺寸统计
    :param atoms:
    :return: 最大尺寸，平均尺寸
    '''
    sum = 0
    max = 0
    for atom in atoms.atoms:
        num = atom.number_of_nodes()
        max = max if max>= num else num
        sum += num
    return max,sum/atoms.num


def getAvgDeg(atoms):
    cnt = 0
    sum = 0
    for atom in atoms.atoms:
        try:
            sum += atom.number_of_edges() * 2 / atom.number_of_nodes()
            cnt += 1
        except:
            pass
    return sum/cnt