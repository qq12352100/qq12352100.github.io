#!/usr/bin/python
# encoding:utf-8

import socket
import sys
import threading
import queue

def scan():
    while not q.empty():
        port = q.get()
        c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        if c.connect_ex((host,port))==0:
            print (port)
        c.close()

if __name__=="__main__":
    host = '101.43.7.199'
    thread_num = 5
    q = queue.Queue()
    for port in range(1,65535):
        q.put(port)
   
    for i in range(int(thread_num)):
        t = threading.Thread(target=scan)
        t.start()
        #t.join()#子线程全部运行完了结束进程，以免线程卡死