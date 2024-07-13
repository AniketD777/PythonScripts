from socket import *
import threading
import argparse
import sys

banners=[]
lock = threading.Lock()

def getArguments():
    try:
        getArgs = argparse.ArgumentParser(description='[-] Usage: script.py -t <target> -p <port>')
        getArgs.add_argument('-t', dest='target', help='Specify target IP/Domain.', required=True)
        getArgs.add_argument('-p', dest='port', help='Specify target Port or Ports(Comma separated or hyphen separated for range).', required=True)
        options = getArgs.parse_args()
        return options
    except argparse.ArgumentError as err:
        print(f"[-] Error: {err}")
        sys.exit(1)

def portscan(host,port):
    sock=socket(AF_INET,SOCK_STREAM)
    sock.settimeout(5)  
    try:
        sock.connect((host,int(port)))
        banner=sock.recv(1024).decode().strip("\n")
        with lock:
            banners.append((port, banner, "Active"))  
    except timeout:
        with lock:
            banners.append((port, "", "Not Active"))  
    except Exception as e:
        with lock:
            banners.append((port, "", f"Not Active"))   
    finally:
        sock.close()

def scan():
    options=getArguments()
    if ',' in str(options.port):
        ports=str(options.port).split(',')
    elif '-' in str(options.port):
        ports=list(range(int((options.port).split('-')[0]),int((options.port).split('-')[1]) + 1))
        
    host=gethostbyname(options.target)
    threads=[]
    
    for port in ports:
        thread=threading.Thread(target=portscan,args=(host,port))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def main():
    scan()
    for banner in banners:
        if banner[2] == "Active":
            print('[+] Port '+str(banner[0])+': '+str(banner[1]))
        
if __name__=='__main__':
    main()
