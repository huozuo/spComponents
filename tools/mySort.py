'''
date: 22.01.04
author: pmy
description: 按照自定义方式对列表进行排序
'''
import re
def sortStr(strs):
    '''
    按照字符串进行排序
    如果其中有数字，则按照真实数字大小，从低往高进行排序
    只能处理第一个数字
    :param strs:
    :return:
    '''
    numStr = {}
    res = []
    for s in strs:
        num = findFirstDigit(s)
        if num not in numStr.keys(): numStr[num] = []
        numStr[num].append(s)
    # 分别进行排序
    keys = sorted(numStr.keys())
    for key in keys:
        numStr[key].sort() # 先进行排序
        # 按照第一个数字进行排序
        res = res + sortByFirstDigit(numStr[key])
    return res


def sortByFirstDigit(strs):
    '''
    按照出现的第一个数字进行排序
    :param strs:
    :return:
    '''
    numStr = {}
    res = []
    for s in strs:
        num = re.findall(r'\d+',s)
        num = -1 if len(num)==0 else int(num[0])
        if num not in numStr.keys(): numStr[num] = []
        numStr[num].append(s)
    keys = sorted(numStr.keys())
    for key in keys:
        res = res + numStr[key]
    return res

def findFirstDigit(str):
    '''
    找到第一个数字字符的位置
    没有则返回-1
    :param str:
    :return:
    '''
    for i in range(len(str)):
        if str[i].isdigit(): return i
    return -1

if __name__=="__main__":
    a = ['Atom_13.gexf13', 'Atom_10.gexfs', 'A11tom_.gexfs', 'Atom_12.gexfs', 'Atom_1.gexfs', 'Atom_14.gexfs','Atom']
    print(sortStr(a))
