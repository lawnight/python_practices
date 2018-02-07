# -*- coding: UTF-8 -*-
# a = str('已')
# b = str('已')
# import json
# import re
# json_string = json.dumps("解决", ensure_ascii=False).encode('utf8')

# print(json_string)
# print(ord('解'))

# print('\u89e3\u51b3')

# print(re.findall('[0-9]+', 'fff11fff'))


# te = "['x','y']"
# te = exec('temp = ' + te)
# print(temp[0])


l = '2,7,5,1,3,14,41,38,66,47,36,40'.split(',')
c= 0
for i in l:
    count = int(i)
    c= c+count

print str(c)









