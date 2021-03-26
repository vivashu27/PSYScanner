#!/usr/bin/env python2.7

import socket
import sys
import getopt
import threading
from queue import Queue
from termcolor import colored
threading.Lock()
q=Queue()
portopen=list()
socket.setdefaulttimeout(5)
def usage():
    print colored("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n","red")
    print colored("\n\t\t\tPSYSCANNER !!! v1.1\n\n","red")
    print colored("\t\t\tby @luffy27\n\n","red")
    print colored("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n\n","red")
    print colored("-t --target for host\n","red")
    print colored("-r --range 0 100 for port range\n","red")
    print colored("-b --banner to grap services on ports\n","red")
    print colored("-h --help\n","red")
    print colored("Use ./scannme.py -t 127.0.0.1 -r 80 2000 -h\n","red")
    
    
def main():
    global host
    global port1
    global port2
    global opt
    ban=False
    opt=""
    host=""
    port1=0
    port2=0
    if not len(sys.argv[1:]):
        usage()
    try:
        opt,arg=getopt.getopt(sys.argv[1:],'t:r:b,h',["target","range","banner","help"])
    except:
        print("some thing occured")

    for o,a in opt:
        if o in ("-h","--help"):
            usage()
        elif o in ("-t","--target"):
            host=a
        elif o in ("-r","--range"):
            port1=int(a)
            port2=int(sys.argv[-1])
        elif o in ("-b","--banner"):
            ban=True
            
    for j in range(port1,port2+1):
        q.put(j)
        
    if host!="":
        print colored("Host Scan for","red"),colored(host,"red"),"\n"
    
    for i in range(100):
        thread=threading.Thread(target=scan,args=(host,port1))
        thread.daemon=True
        thread.start()
    if ban:
        banner(host)

def scan(host,p1):
    while not q.empty():
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        port=q.get()
        res=sock.connect_ex((host,port))
        if res==0:
            portopen.append(int(port))
            print colored("OPEN: ","green"),colored(str(port)+"\n","green")
        if q.empty():
            break

def banner(host):
    print(portopen)
    for ports in portopen:
        try:
            socks=socket.socket()
            socks.connect((host,ports))
            socks.send("hello\n\t")
            banner=socks.recv(95)
            print colored("Port: ","green"),colored(str(ports),"green"),colored("banner: "+banner+"\n","green") 
        except Exception as e:
            print colored("Port: ","green"),colored(str(ports),"green")
        
        
        
main()
