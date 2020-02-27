import requests
import re

# "https://item.jd.com/100011551632.html" 100011551632
url = ["https://item.jd.com/100011551632.html"]

headers= {
    "User-Agent":"Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
    "Referer": "https://item.jd.com/7348369.html",
}
skuid_t=""
for url_a in url:  
    response = requests.get(url_a, headers=headers)
    response.encoding = 'utf-8'
    skuid_re = re.compile(r"skuid: '(.*?)',")
    try:
        skuid = re.findall(skuid_re, response.text)[0]
        print("url:",url_a,".skuid["+skuid+"]")
        skuid_t+=skuid+","
    except:
        print("ERROR:",url_a)
    
print(skuid_t)
    
