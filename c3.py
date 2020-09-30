count=0
def solution(input,visited):
    result = []
    global count
    for i in range(1,10):
        copyInput = input.copy()
        if(attempAdd(copyInput,i)):
            for head in getHead(copyInput):
                for j in range(0,len(visited)):
                    visited[j] = 0
                for h in head:
                    visited[h] = 1  
                count = 0                  
                if DFS_visit(copyInput,{},visited) == True:
                    result.append(i)
                    break
    return result
def getHead(input):
    result = []
    last = 0
    count =1 
    for k,i in enumerate( input):
        if i>last:
            last = i
            count =1
        elif i==last:
            count = count +1
            if count ==2:
                result.append([k-1,k])
    return result


def attempAdd(input,i):
    count =0
    for index,j in enumerate( input):
        if j==i:
            count = count +1
        if j>i: 
            if count==4:
                return False
            else:
                input.insert(index,i)
                return True
    
    input.append(i)
    return True


def DFS_visit(input,cur,visitied):
    #lefts = removeHead(input)
    # 先找出三个
    global count
    if count == 12:  
        #print('success',visited)     
        return True
    result = find(input,visitied)
    for i in result:
        for k in i:          
            visitied[k] = 1
        count = count +3
        if count == 12:
            #print('success',visited)
            return True
        DFS_visit(input,cur,visitied)    
        if count ==12:
            return True
        for k in i:
            visitied[k] = 0
        count = count -3
    #if len(result)==0 and count == 9:
        #print('failed',visited)
    return False

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


data = [3 ,3 ,3 ,4 ,4, 4 ,6 ,6 ,6 ,8, 8, 9 ,9]

#data = list(map(int, input().split()))
visited = [0]*14

data.sort()
result = solution(data,visited)
for x in result:
    print(x,end=" ")    