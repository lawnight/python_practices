# -*- coding: utf-8 -*-
#通过tcp代理，修改游戏发送到服务器的协议，包括协议的解码，编码
import sys
import socket
import threading
import os
import hexdump
import sys
import sniff.si as si
import re
#from modify import request_handler
# this is a pretty hex dumping function directly taken from
# http://code.activestate.com/recipes/142812-hex-dumper/

def receive_from(connection):
    buffer = b""
    # We set a 2 second time out depending on your
    # target this may need to be adjusted
    connection.settimeout(0.4)
    try:
        # keep reading into the buffer until there's no more data
        # or we time out
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as ex:
        if str(ex)!='timed out':
            print('receive:',ex)
    return buffer


def proxy_handler(client_socket,addr, remote_host, remote_port, receive_first):
    client_socket
    # connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    print('链接远端{}'.format(remote_port))

    cIp,cPort = addr
    # receive data from the remote end if necessary
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        # send it to our response handler
        # remote_buffer = response_handler(remote_buffer)

        # if we have data to send to our local client send it
        if len(remote_buffer):
            print ("[<==] Sending %d bytes to localhost." % len(remote_buffer))
            client_socket.send(remote_buffer)

    # now let's loop and reading from local, send to remote, send to local
    # rinse wash repeat
    while True:
        # read from local host
        local_buffer = receive_from(client_socket)
        llen = len(local_buffer)
        if llen:            
            print ("[==>] send %d bytes to remote." % llen)
            local_buffer = request_handler(cIp,cPort,remote_host, remote_port,local_buffer) 
            if local_buffer:           
                remote_socket.send(local_buffer)
        # receive back the response
        remote_buffer = receive_from(remote_socket)
        rlen = len(remote_buffer)
        if rlen:
            print ("[<==] Received %d bytes from remote." % rlen)
            remote_buffer = response_handler(remote_host, remote_port,cIp,cPort,remote_buffer)
            client_socket.send(remote_buffer)
            # print("[<==] Sent to localhost.")
        # # if no more data on either side close the connections
        # if not len(local_buffer) or not len(remote_buffer):
        # 	client_socket.close()
        # 	remote_socket.close()
        # 	print "[*] No more data. Closing connections."
        # 	break

def main():
    # setup local listening parameters
    local_host = '0.0.0.0'  # sys.argv[1]
    
    remote_host = '114.116.11.81'
    # remote_host = '192.168.2.207'
    port = 20011
    remote_port = local_port= port

    proxy_thread = threading.Thread(target=proxy,args=(local_host,local_port,remote_host,remote_port))
    proxy_thread.start()

def proxy(local_host,local_port,remote_host,remote_port):
    receive_first = 'False'
    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False
    # now spin up our listening socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((local_host, local_port))
    except Exception as ex:
        print (ex)
        print ("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print ("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)

    print ("[*] Listening on %s:%d" % (local_host, local_port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        # print out the local connection information
        print ("%d [==>] Received incoming connection from %s:%d" % (local_port,addr[0], addr[1]))
        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler, args=(
            client_socket,addr, remote_host, remote_port, receive_first))
        proxy_thread.start()


# python3 修改茜色
def request_handler(cIp,cPort,dIp, dPort,buffer):
    se,pkts = si.receive(cIp,cPort,dIp,dPort,buffer)   
    result = b'' 
    if pkts:
        for pkt in pkts:
            data = processBR(pkt,se.randKey)
            result = result + data
    return result

# 陆百购买协议的修改
def processBR(pkt,randKey):
    if pkt.msgId == 3902:
        o_data = si.decode_buf(pkt.buf,randKey)
        temp = bytearray(o_data)
        key = b'\x51\x01'                
        # print('find',re.findall(key,temp))
        pos = temp.rfind(key)
        # 1变成-1
        temp =temp[:pos] + temp[pos:].replace(key,b'\x5f\xff\xff\xff\xff')
        si.show_si(temp)                
        to_send = si.encode_buf(bytes(temp), randKey)
        # 修正包头的长度
        head = to_send[0:21]
        head = bytearray(head)
        head[4:8] = (len(to_send).to_bytes(4,'little'))                
        data = head + to_send[21::]
        return data
    return pkt.buf

def response_handler(cIp,cPort,dIp, dPort,buffer):
    si.receive(cIp,cPort,dIp,dPort,buffer)
    return buffer

if __name__ == '__main__':
    main()