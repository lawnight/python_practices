
# import math
# N = [1,3,4,5,6,8,9,10]
# D = 2
# mem = {}
# def f(N,D):
#     a = f(N[1::],D) + con(f[0],f[1::])



# def con(p,pList,d):
#     # find 和p满足条件的点
#     stati = []
#     for i in pList:
#         if abs(i-p) >= d:
#             stati.append(i)

# 满足条件的点 之间。
# 矩阵连乘法,矩阵M[i] = shape(arr[i],arr[i+1]),  A[0] 到 A[n-1] n个矩阵的连乘
import sys
#  arr，是矩阵从左到右的维度
def solution(arr):
    # mem[0,n]    
    DP = {}    
    matrix_count = len(arr) -1
    for i in matrix_count:
        DP[(i,i+1)] = 0
    for dis in range(2,matrix_count): #提高subSequence 的长度
        for i in matrix_count: # 构造i，j
            j = i + dis
            min = sys.maxsize
            for k in range(i,j):
                    temp = DP[(i,k)]+DP[(k,j)] + cost(arr,i,k,j)
                    if temp < min:
                        min = temp
                        DP[(i,j)] = min    
def cost(arr,i,k,j):
    return arr[i]*arr[k]*arr[j]




