'''
date:22.02.18
author:pmy
description: 用于对网络稀疏表征所得到的原子，真实率进行计算
            计算的是 每个原子的真实率的平均、原子真实个数
'''
from spComponents.tools import getFileName
from spComponents.sparseRepresentation import atomGen,atom2nodes,calcAtomMatch

def run():
    fileList = getFileName.showDir("data/")
    # atom2nodes
    # for file in fileList:
    #     atom2nodes.Atom2Nodes(file).getAllnodes()
    print("====atom2nodes done====")
    # atomMatch
    for file in fileList:
        matchRes = atomMatch(file)
        print("####"+file+"####")
        handle(matchRes)

    print("====atomMatch done====")


def atomMatch(filename):
    '''
    对每个网络进行原子匹配情况统计
    :param filename: 文件名
    :return:
    '''
    matchRes = {} # {atom:匹配率}
    cam = calcAtomMatch.CalcAtomMathc(filename, 10)

    for atomNum in cam.nodes.keys():
        cnt = 0
        nodes = cam.nodes[atomNum]
        g = cam.loadNetwork("data/" + cam.name + "/Atom_" + atomNum + ".gexf")
        for node in nodes:
            if len(node) < cam.size: continue
            if cam.match(node, g): cnt += 1
        matchRes[atomNum] = cnt / len(nodes)

    return matchRes  # 匹配率

def handle(matchRes):
    '''
    处理原子匹配的结果
    打印原子真实率（平均）
    打印原子匹配率
    :param matchRes:
    :return:
    '''
    n = len(matchRes)
    totalMatch = 0
    cnt = 0
    for k,v in matchRes.items():
        totalMatch += v
        cnt += 1 if v!=0 else 0

    print("num of atoms: ",n)
    print("average atom match: ",totalMatch/n)
    print("atom match: ",cnt/n)



if __name__=="__main__":
    run()