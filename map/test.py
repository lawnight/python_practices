a = str('已')
b = str('已')
import json
import re
json_string = json.dumps("解决", ensure_ascii=False).encode('utf8')

print(json_string)
print(ord('解'))

print('\u89e3\u51b3')

print(re.findall('[0-9]+', 'fff11fff'))


te = "['x','y']"
te = exec('temp = ' + te)
print(temp[0])
