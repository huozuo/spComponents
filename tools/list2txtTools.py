'''
date: 21.12.23
author: pmy
func: 标准化的将list转换到txt中，主要用于int类型元素
        可能含有多级列表，需要输入保证正确
version: v1
'''

def writeList2txt(file,data):
    '''
    将list写入txt
    :param data:
    :return:
    '''
    file.write(str(data))
    file.write("\n")

def readListFromStr(str):
    '''
    str -> List
    除去冗余的方法调用
    :param str:
    :return:
    '''
    res,pos = help(str,1)
    return res

def help(str,startIndex):
    '''
    单行字符串的读取，形成list
    :param str:
    :return:
    '''
    str = str.replace(" ","").replace("\'","") # 将所有空格删去, 以及引号
    res = []
    i = startIndex
    pre = startIndex
    while i <len(str):
        if str[i] == '[':
            # 将pre-i-2的字符都切片，切split
            if i-2>=pre:
                slice = str[pre:i-1].split(',')
                for element in slice:
                    res.append(int(element))
            # 递归调用 加入子list
            child,pos = help(str,i+1)
            res.append(child)
            i = pos # i移动到pos位置，也就是递归的最后一个右括号
            pre = pos + 2 # 右括号之后是, [ 有三个字符，所以要+2至少
        elif str[i] == ']':
            # 将前面的全部放入列表
            if i-1>=pre:
                slice = str[pre:i].split(',')
                for element in slice:
                    res.append(int(element))
            return res,i
        i = i + 1

    return res,i


if __name__=="__main__":
    str = "[[4], [3, 2, 5], [2, [1,100002,3,4],1, 4]]"
    list = readListFromStr(str)
    print(list)












