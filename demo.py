'''
date: 21.12.08
author: pmy
func: 用于运行spComponents下的跑py
      主要用于非作者使用指导
'''
from spComponents.sparseRepresentation import sample
from spComponents.sparseRepresentation import ksvd
from spComponents.BMF import runBMF
from spComponents.sparseRepresentation import atomGen
from spComponents.sparseRepresentation import atom2nodes
from spComponents.sparseRepresentation import plotAtoms


if __name__=="__main__":
    sample.run(10)    #采样
    ksvd.run() #浮点矩阵分解 ksvd （与布尔矩阵二选一）
    runBMF.run()     #布尔矩阵分解
    atomGen.run()     #原子生成，恢复网络
    atom2nodes.run()    #原子--实际节点
    plotAtoms.run() # 绘制原子图像



