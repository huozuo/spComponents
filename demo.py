'''
date: 21.12.08
author: pmy
func: 用于运行spComponents下的跑py
      主要用于非作者使用指导
'''

import spComponents

if __name__=="__main__":
    spComponents.sparseRepresentation.sample.run(10)
    spComponents.MBF.runMBF.run()
    spComponents.sparseRepresentation.atomGen.run()
    spComponents.sparseRepresentation.atom2nodes.run()
    spComponents.sparseRepresentation.plotAtoms.run() # 绘制原子图像



