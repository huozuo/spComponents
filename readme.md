# spComponents
- date: 11-10
- author: pmy
- aim: 存储与管理稀疏表征常用工具
- 内容：
    - atom2nodes： 根据原子，稀疏矩阵，字典矩阵确定原子节点与原始网络实际节点的映射
    - atom：生成原子
    - sample： 进行采样
        - transformNetwork：对自我中心网络进行重排序
    - getFileName：获取当前路径下所有文件名并返回
    - MEBF：布尔矩阵分解
        - expansion：布尔矩阵分解时基向量进行扩展的具体方式
- note:
    - 当原子规模过大时，atom2nodes中因为调用了networkx的同构映射方法，会很慢，所以可以考虑将这些很慢的原子丢掉，如此，就比较快了

        
## 11-05更新1
- 更新py：MEBF
- 更新版本：v1
- 更新内容：
```text
将1+1=2的思想加入布尔矩阵分解
当前expansion分别与残差矩阵和原始矩阵进行相似度对比，当分别超过50%和Thres时，即算匹配
```

## 11-05更新2
- 更新py：sample
- 更新版本：v1
- 更新内容：
```text
考虑到向量不相似，但网络同构的问题
将一阶邻居和二阶邻居分别排序
按照度大到度小
从而实现能量的集中
使得1尽可能形成矩形
```

## 11-10更新1
- 更新py：atom2nodes
- 更新版本：v1
- 更新内容：
```text
之前的atom生成与dict2vnodes并不相同
atom生成是只考虑了矩阵一半
而dict2vnodes考虑了整个矩阵
所以进行了改动
将atom改成了考虑整个矩阵
同时都添加了if==j:continue 的跳过对角线的情况，防止错误出现
```

## 11-10更新2
- 更新py：atom2nodes
- 更新版本：v2
- 更新内容：
```text
加上了self.curNum表示当前的原子号
加上了self.atoms表示所有的原子nx
加上了正则来自动读取有多少个原子
修改了方法dict2vnodes，逻辑为：
    先按照当前原子来确定vnodes
    然后获取当前dict和当前的atoms的同构映射关系
    根据这个映射关系来替换掉vnodes
    从而保证顺序
```
## 11-11更新1
- 更新py：calcAtomMatch
- 更新版本：v0
- 更新内容：
```text
计算稀疏表征的原子匹配率
首先读取原始网络，作为边的判别
然后读取原子网络，读取原子对应的实际节点
遍历所有的原子边，将其翻译成实际节点的边，判断实际节点便是否在原网络中存在
如果存在，则cnt++
最终打印出cnt/总的原子数
```

## 11-12更新1
- 更新py：matrixTools
- 更新版本：v0
- 更新内容：
```text
增加矩阵的tools的py
包含功能有
    进行sample - dict*coef的误差计算，非零的统计，除以sample中1的个数
    载入txt矩阵到np中
    保存dict矩阵和coef矩阵到txt中
```



## 11-19更新1
- 更新py：runMBF
- 更新版本：v0
- 更新内容：
```text
运行布尔矩阵分解的py
直接调用其中的run方法，就可以直接运行
```


## 11-24更新1
- 更新py：MEBF
- 更新版本：v1
- 更新内容：
```text
注释每轮的误差print，从而一定程度上较少运行时间
```

## 11-25更新1
- 更新py：atomGen
- 更新版本：v2
- 更新内容：
```text
每次都将邻接矩阵的数值给放到label中去
```

## 11-25更新2
- 更新py：runDemo
- 更新版本：v0
- 更新内容：
```text
写了一个可以run atomGen、atom2nodes的demo，以后直接调这个demo就可以了
```

## 11-26更新1
- 更新py：ksvd
- 更新版本：v0
- 更新内容：
```text
新增一个ksvd的py，用于进行浮点矩阵分解
```

## 11-29更新2
- 更新py：sample
- 更新版本：v1
- 更新内容：
```text
删除采样二阶邻居这一个操作
```

## 12-03更新1
- 更新py：atomSortByError
- 更新版本：v0
- 更新内容：
```text
按照原子生成给sample矩阵带来的误差下降进行排序
返回原子排序，并打印出50%，80%，90%的原子序号
```

## 12-03更新2
- 更新py：ksvd
- 更新版本：v1
- 更新内容：
```text
将其中的误差给修改，以此来看看有没有什么问题
```


## 12-04更新1
- 更新py：ksvd
- 更新版本：v2
- 更新内容：
```text
修改误差计算方式
```

## 12-04更新2
- 更新py：matrix
- 更新版本：v2
- 更新内容：
```text
修改absError中的误差计算方式
对于布尔型无所谓，不变
对于浮点型，>=0.5为1，<0.5为0，这样准确多了，与atomGen中的网络重构逻辑相符
```


## 12-06更新1
- 更新py：atomGen
- 更新版本：v3
- 更新内容：
```text
增加了异质原子的生成
异质原子生成，只是将其中的同质同构给换成了异质同构
异质主要体现在边的属性label上
之前虽然能生成异质原子，但是去同构那里还是采用的同质，所以效果不佳
现在是考虑边属性
本py仍适用与同质的生成，不影响使用，采用label默认值来避免报错
```

## 12-08更新1
- 更新py：demo
- 更新版本：v0
- 更新内容：
```text
为非作者提供demo，进行简单的稀疏表征代码使用
```
## 12-08更新2
- 更新py：runDemo
- 更新版本：v0
- 更新内容：
```text
删除该py
```

## 12-08更新3
- 更新py：atom2nodes
- 更新版本：v3
- 更新内容：
```text
遍历当前路径下的文件名时跳过 ==原始文件==
```
## 12-08更新4
- 更新py：atomSortByError
- 更新版本：v1
- 更新内容：
```text
提供runAll方法，不用手动输入文件名
```

## 12-08更新5
- 更新py：atomSortByError
- 更新版本：v2
- 更新内容：
```text
之前的误差排序有问题，排序的标准是，按照误差排序
而我想要的是按照误差下降排序
所以将 新排序值 = 1 - 原始排序值
这里可能出现负数，是很正常的，尤其是浮点数分解过程中，很容易有负数边来进行拟合误差 
```

## 12-08更新6
- 更新py：atomSortByUses
- 更新版本：v0
- 更新内容：
```text
将原子序号按照原子的使用次数进行排序
也就是直接统计稀疏码即可
```


## 12-10更新1
- 更新py：atom2nodes
- 更新版本：v4
- 更新内容：
```text
因为出现同构映射非常慢的情况在于原子规模很大，很复杂
那么在这种情况下时，基本就只有一种情况，就是一个原子只对应一个字典向量
那么此时，我又何必判断同构呢，此时，一定是按顺序一一对应的
由此，修改逻辑为：当原子和字典唯一对应时，则直接跳过同构映射，从而节省时间
修改了dict2vnodes，添加了原子映射字典 的数目的判断
```

## 12-10更新2
- 更新py：ksvd
- 更新版本：v3
- 更新内容：
```text
针对原子出现规模为0的情况，其原因是负数过多，字典向量与稀疏码向量都是负数
针对此，添加transformPos方法，逻辑为当 当前字典向量中有效正数小于有效负数的数目时，对字典向量和稀疏码向量都取反
以此解决ksvd中负数过多的问题
```

## 12-16更新1
- 更新py：atomSortByError
- 更新版本：v2
- 更新内容：
```text
使用时发现，没有的原子也会被打印出来，所以此处修改，将它们删掉
```

## 12-23更新1
- 更新py：list2txtTools
- 更新版本：v0
- 更新内容：
```text
规范化实现 list2txt 以及 str2list的功能
工具供后序使用
```

## 12-24更新1
- 更新py：list2txtTools
- 更新版本：v1
- 更新内容：
```text
增加了对str中的引号的处理
```


## 12-24更新2
- 更新py：getFileName
- 更新版本：v1
- 更新内容：
```text
增加了对特定文件名称的数目统计
index_123.txt 诸如此类
```

## 12-24更新3
- 更新py：getFileName
- 更新版本：v2
- 更新内容：
```text
增加了对特定文件名称统计
index_123.txt 诸如此类
按需返回
```