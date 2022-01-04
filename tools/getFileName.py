'''
date: 21.11.08
author: pmy
function: 获取当前目录下的所有文件名
location: spComponents
version: v2
'''
import os
import re


def getSpecPaths(basePath,name):
    '''
    获取 basePath目录下，name_xx.txt的 所有路径
    :param basePath:
    :param name:
    :return:
    '''
    num = specFilesCnt(basePath, name)
    paths = []
    for i in range(num):
        path = basePath + name + "_" + str(i + 1) + ".txt"
        paths.append(path)

    return paths


def specFilesCnt(basePath,name):
    '''
    获取 basePath目录下，name_xx.txt的文件数目
    :param basePath:
    :param name:
    :return:
    '''
    fileList = get_filename(basePath)
    cnt = calcFileNums(fileList, name + '_\w+.txt')

    return cnt


def get_filename(base_filename):
    '''
    获取当前目录下的所有文件
    :param base_filename:
    :return:
    '''
    list = os.listdir(base_filename)
    try:
        list.remove("原始网络们")
    except:
        pass
    return list


def calcFileNums(ss,pattern):
    '''
    输入正则式，进行匹配，返回匹配到的文件数目
    :param regx: 正则式
    :return:
    '''
    cnt = 0
    for s in ss:
        if re.match(pattern,s) != None:
            cnt += 1

    return cnt

