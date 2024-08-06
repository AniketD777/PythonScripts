import dns.resolver
import socket
import argparse

def args():
    parser = argparse.ArgumentParser(description="DNS Subdomain Explorer", usage="python3 DNSExplorer.py -d <domain> -f <wordlist>")
    parser.add_argument("-d", dest="domain", help="Target domain.", required=True)
    parser.add_argument("-f", dest="wordlist", help="Subdomains wordlist.", required=True)
    args = parser.parse_args()
    return args

def revDNS(IP): # Reverse DNS Search
    try:
        answerRD=socket.gethostbyaddr(IP)
        return [answerRD[0]]+answerRD[1] # Return both hostname and alias from the response
    except socket.herror:
        return []

def forwDNS(domain,domains): # Forward DNS Search
    reso=dns.resolver.Resolver()
    reso.nameservers=['8.8.8.8']
    reso.port=53
    try:
        answerFD=reso.resolve(domain,'A') # Forward Search Response
        if answerFD:
            IPList=[str(rdata) for rdata in answerFD]
            if domain in domains: # If we already have domain in domains dictionary, append newly found IPs to the corresponding domain.
                domains[domain]=list(set(domains[domain]+IPList))
            else: # Else add a new entry to domains dictionary
                domains[domain]=IPList
            
            for IP in IPList:
                answerRD=revDNS(IP) # Reverse Search Response
                for dom in answerRD:
                    if dom not in domains:
                        domains[dom]=[IP]
                        forwDNS(dom,domains) #Recursively call forwDNS to take care of newly found domains.
                    else:
                        domains[dom]=[IP]
    except:
        pass

def find(domain,subdoms,domains):
    for subdom in subdoms:
        forwDNS(f'{subdom}.{domain}',domains)
        for i in range(0,10): # To include all combinations like www1, mail2, ns5 etc. for the subdomains in wordlist.
            forwDNS(f'{subdom}{i}.{domain}',domains)

def main():
    domains={}
    subdoms=[]
    domain=args().domain
    file=args().wordlist
    try:
        with open(file,'r') as wordlist:
            for word in wordlist:
                subdoms.append(word.rstrip())
        
        find(domain,subdoms,domains)

        for domain in domains:
            print(f'{domain}: {domains[domain]}')

    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
        exit()

if __name__=='__main__':
    main()
