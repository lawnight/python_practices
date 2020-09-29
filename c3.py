# Created with Python AI



input = [ 1, 1, 2, 2, 3, 3, 5, 6, 7, 7, 8, 9]
remain = []

dock = [0]*9
for i in range(9):
    for j in range(4):        
        dock[i] = dock[i] + 1



parent = {}
count = 0
def DFS_visit(input,cur,visitied):
    #lefts = removeHead(input)
    # 先找出三个
    global count
    if count == 12:
        print('success',visited)
        return
    result = find(input,visitied)
    for i in result:
        for k in i:          
            visitied[k] = 1
        count = count +3
        DFS_visit(input,cur,visitied)       
        for k in i:
            visitied[k] = 0
        count = count -3
    if len(result)==0 and count == 9:
        print('failed',visited)

def find(data,visited):
    r = [] # 所有可能remove data的方法 2维数组
    r.extend(findTri(data,visited))
    r.extend(findSeq(data,visited))
    return r


def findSeq(data,visited):
    last = -1
    count = 1
    result = []
    temp = []
    for k,v in enumerate(data):
        if visited[k]:
            continue
        if v==last:
            continue
        if v==last+1:
            if count ==3:
                temp = temp[1:]
                temp.append(k)                
            else:
                count = count +1
                temp.append(k)
        else:
            temp = []
            count =1
            temp.append(k)
        last=v
        if count == 3:            
            result.append(temp)
    return result
            
           
                      
        
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
print(findSeq(input,visited))
print('find:',find(input,visited))

DFS_visit(input,{},visited)
    
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
# 回溯法n