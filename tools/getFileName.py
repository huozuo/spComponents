'''
date: 21.11.08
author: pmy
function: 获取当前目录下的所有文件名
location: spComponents
version: v2
'''
import os
import re
import mySort

def getSpecPaths(basePath,name):
    '''
    获取 basePath目录下，name_xx.txt的 所有路径
    :param basePath:
    :param name:
    :return:
    '''
    fileList = showDir(basePath)
    paths = filterPath(fileList,name)
    paths = [basePath+path for path in paths]
    return paths


def specFilesCnt(basePath,name):
    '''
    获取 basePath目录下，name开头的文件数目
    :param basePath:
    :param name:
    :return:
    '''
    fileList = dir(basePath)
    cnt = calcFileNums(fileList, name)

    return cnt


def showDir(basePath):
    '''
    获取当前目录下的所有文件
    :param basePath:
    :return:
    '''
    list = os.listdir(basePath)
    if "原始网络们" in list: list.remove("原始网络们")
    if "原始网络们" in list: list.remove("原始网络们")
    return list


def calcFileNums(ss,pattern):
    '''
    输入正则式，进行匹配，返回匹配到的文件数目
    :param regx: 正则式
    :return:
    '''
    return len(filterPath(ss,pattern))

def filterPath(ss,pattern):
    '''
    从str列表中找出符合pattern的str
    :param ss:
    :param pattern:
    :return:
    '''
    res = []
    for s in ss:
        if re.match(pattern,s) != None:
            res.append(s)
    res = mySort.sortStr(res) # 进行排序
    return res
