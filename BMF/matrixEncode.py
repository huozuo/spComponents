'''
date: 22.02.04
author: pmy
description: 对矩阵的列向量编码、去重
'''
import numpy as np
from ..tools.dictTools import *
from ..tools.vecType import VecType
from ..tools.numpyTools import *

class MatrixEncode:
    '''
    对矩阵的列向量编码、去重
    '''
    def __init__(self,matrix):
        self.matrix = matrix
        # col
        self.col2Code = self._colsEncode(self.matrix)
        self.code2Col = self._codeVec(self.col2Code)
        # row
        self.row2Code = self._rowsEncode(self.matrix)
        self.code2Row = self._codeVec(self.row2Code)

    def unique(self,vecs,vecType):
        '''
        将重复编码的列索引去重
        :param vecs: 列索引 并不是列表
        :return: 列表
        '''
        vecs = reshapeVec(vecs)
        vec2code = self.col2Code if vecType==VecType.col else self.row2Code
        codeSet = set()
        res = []
        for vec in vecs:
            code = vec2code[vec]
            if code not in codeSet:
                codeSet.add(code)
                res.append(vec)
        return res


    def _vec2code(self,vec):
        '''
        对向量进行编码 (支持列向量、行向量)
        np的非零函数，将相差为1的合并
        :param vec: numpy矩阵中向量
        :return:
        '''
        code = ""
        indexs = np.nonzero(vec)[0]
        n = len(indexs)
        l = 0
        for r in range(n):
            if r==n-1 or indexs[r+1]-indexs[r] >1 :
                if r>l: code += str(indexs[l]) + "-" + str(indexs[r])
                else: code += str(indexs[r])
                if r!=n-1: code += " "
                l = r+1
        return code

    def _colsEncode(self,matrix):
        '''
        对矩阵的所有列向量进行编码
        :param matrix:
        :return:{索引：编码}
        '''
        res = {}
        m,n = np.shape(matrix)
        for j in range(n):
            res[j] = self._vec2code(matrix[:,j])
        return res

    def _rowsEncode(self,matrix):
        '''
        对矩阵的所有列向量进行编码
        :param matrix:
        :return:{索引：编码}
        '''
        res = {}
        m,n = np.shape(matrix)
        for i in range(m):
            res[i] = self._vec2code(matrix[i,:])
        return res

    def _codeVec(self,vec2code):
        '''
        编码与vec的映射
        直接将vec2code字典翻转即可
        :param vec2code: col2code or row2code均可
        :return:
        '''
        return reverse(vec2code)



if __name__=="__main__":
    matrix = np.zeros((10,10))
    matrix[1][0] = 1
    matrix[2][0] = 1
    matrix[3][0] = 1
    matrix[4][0] = 1
    matrix[5][0] = 1
    matrix[6][0] = 1
    matrix[7][0] = 1
    matrix[8][0] = 1
    matrix[2][1] = 1
    matrix[3][1] = 1
    matrix[5][1] = 1
    matrix[6][1] = 1
    matrix[8][1] = 1
    matrix[9][1] = 0

    mve = MatrixEncode(matrix)
    print(mve.col2Code)
    print(mve.code2Col)
    print("=====")
    print(mve.row2Code)
    print(mve.code2Row)
    print(mve.unique([0,1],VecType.col))
