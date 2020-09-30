n = int(input())

while n > 0:
    word = input()
    n -= 1
    p = 0
    count = 0
    count_2 = 0
    new_word = []
    bool pairs = 
    for c in word:
        if c == p:
            if count_2 > 0:
                count_2 += 1
            else:
                count += 1
                if count == 2:

        else:
            p = c
            if count >= 2:
                count_2 +=1
            else:
                count = 1
                    
        if count>=3:
            continue
        new_word.append(c)
