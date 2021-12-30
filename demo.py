'''
date: 21.12.08
author: pmy
func: 用于运行spComponents下的跑py
      主要用于非作者使用指导

note：运行demo文件尽量不要放在spComponents在同一目录下，便于维护

      需要创建的数据路径为 ： data/原始网络们/
      该路径中放入gexf文件
'''

from spComponents import sample
from spComponents import ksvd
from spComponents import atomGen
from spComponents import atom2nodes
from spComponents import atomSortByError
from spComponents import runMBF


if __name__=="__main__":
    # 挨个运行，每次单独运行一个，防止中间有方法出错
    sample.sampleAll(size=20) # 采样
    # ksvd.runKsvd(dictNum=200) # ksvd进行矩阵分解
    runMBF.runAll()

    atomGen.run() # 生成原子，重构网络
    atom2nodes.runAtom2nodesAll() # 生成原子与真实节点的映射关系
    atomSortByError.runAll() # 按照误差进行原子的排序  beta 测试中



