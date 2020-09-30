n = int(input())

while n > 0:
    m = int(input())
    res = 1
    d = {}
    for i in range(m):
        l = list(map(int , input().split()))
        k = l[0]
        tmp_d = {}
        for j in range(k):
            index = l[2 * j + 1] * 1000000000 + l[2 * j + 2]
            if index in d:
                tmp_d[index] = d[index] + 1
                res = max(res, tmp_d[index])
            else:
                tmp_d[index] = 1
        d = tmp_d
    print(res)
    n -= 1