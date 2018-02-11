# -*- coding: UTF-8 -*-
import socket
import struct
import pyshark

capture = pyshark.LiveCapture(interface='en0',display_filter=False)
capture.set_debug()
capture.sniff(timeout=10)
print capture


