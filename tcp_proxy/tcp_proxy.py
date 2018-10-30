# -*- coding: utf-8 -*-
#通过tcp代理，修改游戏发送到服务器的协议，包括协议的解码，编码
import sys
import socket
import threading
import os
rand_key = '00'
#from modify import request_handler
# this is a pretty hex dumping function directly taken from
# http://code.activestate.com/recipes/142812-hex-dumper/

def receive_from(connection):
    buffer = ""
    # We set a 2 second time out depending on your
    # target this may need to be adjusted
    connection.settimeout(0.1)
    try:
        # keep reading into the buffer until there's no more data
        # or we time out
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    # connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # receive data from the remote end if necessary
    if receive_first:

        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        # send it to our response handler
        remote_buffer = response_handler(remote_buffer)

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

            print ("[==>] Received %d bytes from localhost." % llen)
            #包足够了再发
            if llen != 21:
                #hexdump(local_buffer)
                pass

            # send it to our request handler
            # reload(modify)
            # local_buffer = modify.request_handler(local_buffer)

            # send off the data to the remote host
            remote_socket.send(local_buffer)
            print ("[==>] Sent to remote.")

        # receive back the response
        remote_buffer = receive_from(remote_socket)
        rlen = len(remote_buffer)
        if rlen:

            print ("[<==] Received %d bytes from remote." % rlen)

            if rlen != 21:
                #hexdump(remote_buffer)
                pass

            # send to our response handler
            # remote_buffer = modify.response_handler(remote_buffer)

            # send the response to the local socket
            client_socket.send(remote_buffer)

            print("[<==] Sent to localhost.")

        # # if no more data on either side close the connections
        # if not len(local_buffer) or not len(remote_buffer):
        # 	client_socket.close()
        # 	remote_socket.close()
        # 	print "[*] No more data. Closing connections."

        # 	break


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        print ("[==>] Received incoming connection from %s:%d" % (addr[0], addr[1]))

        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler, args=(
            client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()


def main():

    # no fancy command line parsing here
    #     if len(sys.argv[1:]) != 3:
    #         print "Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]"
    #         print "Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
    #         sys.exit(0)

    # setup local listening parameters
    local_host = '0.0.0.0'  # sys.argv[1]
    local_port = 9998  # int(sys.argv[2])

    # setup remote target
#     remote_host = sys.argv[1]
#     remote_port = int(sys.argv[2])

    remote_host = '192.168.20.97'
    remote_port = 10001

    # this tells our proxy to connect and receive data
    # before sending to the remote host
    # #receive_first = sys.argv[5]

    receive_first = 'False'

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # now spin up our listening socket
    server_loop(local_host, local_port, remote_host,
                remote_port, receive_first)


# print str("%x" % 11).decode('hex')
if __name__ == '__main__':
    main()