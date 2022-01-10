'''
date:22.01.04
author: pmy
description: tools for save
'''

import numpy as np

def save(name,dict,coef,add=""):
    '''
    将传入dict矩阵和coef矩阵按照name来进行存储
    存储的路径在data下
    :param name:
    :param dict:
    :param coef:
    :return:
    '''
    dic_name = "data/"+name+"/dic_Sample"+add+".txt"
    coef_name = "data/"+name+"/coef_Sample"+add+".txt"
    np.savetxt(dic_name, dict, fmt="%d")
    np.savetxt(coef_name, coef, fmt="%d")