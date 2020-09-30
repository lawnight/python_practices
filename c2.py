def solution(n,d,data):
    dp = {}
    dp[n-1] = 0
    dp[n-2] = 0
    for i in reversed(range(0,n-2)):
        dp[i] = dp[i+1] + calcu(data,d,i,n)
    return dp[0]

def recursiveFind(data,l,r,v):
    while l <=r:
        i = (l+r)//2
        if data[i] == v:
            return i
        elif data[i] < v:
            l = i+1            
        else:
            r = i-1            
    return r

def calcu(data,d,i,n):    
    outPoint = data[i]    
    l = i+1
    right = n-1
    v = outPoint+d # target smaller than v    
    c  = recursiveFind(data,l,right,v)
    count = c - i
    return (count*(count-1))//2

n, dist = map(int, input().split())
nums = list(map(int, input().split()))
print(solution(n,dist,nums)%99997867)


# n,dist = 5 ,19
# nums = [1,10 ,20 ,30,50]
# print(solution(n,dist,nums))
