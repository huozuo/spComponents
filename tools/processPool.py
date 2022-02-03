from concurrent.futures import ProcessPoolExecutor
import os

class ProcessPool:
    # 任务数超过cpu核心数时，会把cpu跑到 2/3
    def __init__(self,proNum=1000):
        '''
        init
        :param proNum: 指定进程数
        '''
        self.proCnt = min(int(os.cpu_count()/3),proNum) # 读取的线程数，/2 即是物理核心数
        self.pool = ProcessPoolExecutor(self.proCnt)
        print("max process:",self.proCnt)

    def run(self,func,args):
        res = list(self.pool.map(func, args))
        return res

