'''
统计最终原子数目
'''
from spComponents.tools import getFileName
from spComponents.sparseRepresentation import networkInfo
import networkx as nx

def run():
    '''
    获取所有的结果
    :param plotArrange:
    :return:
    '''
    basePath = "data/"
    files = getFileName.showDir(basePath)
    atoms = []
    for file in files:
        if "gexfs" in file: continue
        ni = networkInfo.NetworkInfo(file)
        atoms += ni.atoms

    # 去重
    res = rmRepeated(atoms)
    print(len(res))

def rmRepeated(atoms):
    res = []

    for atom in atoms:
        In_F = False
        for other in res:
            GM = nx.isomorphism.GraphMatcher(atom, other,
                                             edge_match=nx.isomorphism.categorical_edge_match(['label'], [-1]))
            if GM.is_isomorphic():
                In_F = True
        if not In_F:
            res.append(atom)
    return res



if __name__=="__main__":
    run()