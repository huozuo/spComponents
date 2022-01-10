'''
date: 21.12.08
author: pmy
func: 用于运行spComponents下的跑py
      主要用于非作者使用指导
'''

import spComponents

if __name__=="__main__":
    spComponents.sparseRepresentation.sample.run(10)    #采样
    spComponents.sparseRepresentation.ksvd.run() #浮点矩阵分解 ksvd （与布尔矩阵二选一）
    # spComponents.MBF.runMBF.run()     #布尔矩阵分解
    spComponents.sparseRepresentation.atomGen.run()     #原子生成，恢复网络
    # spComponents.sparseRepresentation.atom2nodes.run()    #原子--实际节点
    spComponents.sparseRepresentation.plotAtoms.run() # 绘制原子图像



