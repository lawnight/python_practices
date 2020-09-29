

input = [1 ,1, 1, 1, 2, 2, 3, 3, 5, 6, 7, 7, 8, 9]
remain = []

dock = [0]*9
for i in range(9):
    for j in range(4):        
        dock[i] = dock[i] + 1



parent = {}
def DFS_visit(input,cur,visited):
    #lefts = removeHead(input)
    # 先找出三个
    result = find(input,vistied)
    for i in result:
        DFS_visit(input,cur,visited.append(i))

def find(data,visited):
    r = [] # 所有可能remove data的方法 2维数组
    r.append(findTri(data))
    r.append(findSeq(data))
    return r


def findSeq(data,visited):
    last = 0
    count = 0
    result = []
    for k,v in enumerate(data):
        if visited[k]:
            continue

def findTri(data,visited):
    d = 0
    count = 0
    result= []    
    for k,i in enumerate(data):
        if visited[k]:
            continue
        if i>d:
            d = i
            count = 0
        count = count +1
        if count>=3:
            result.append([k-2,k-1,k])
            count = 0
    return result

visited = [0]*len(input)

print(findTri(input,visited))
    
# m中选n个
def getCombination(data,m,n):
    result = []
    for i in m:
        for j in range(n,m):
            result.append()


def removeHead(d):
    pass

def removeStructure(left):
    pass

#only can take another

# if has pair ,添加顺子或者三个。都可以组成和牌。
# 回溯法