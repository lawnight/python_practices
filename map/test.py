# -*- coding: UTF-8 -*-
import socket
import struct
import pyshark

# capture = pyshark.LiveCapture(interface='en0',display_filter=False)
# capture.set_debug()
# capture.sniff(timeout=10)
# print capture

lst = [1,2,3,4,5,6,6,7,8,9]

for i in range(0, len(lst), 3):
    print lst[i:i + 3]

# print u'哈哈哈'
