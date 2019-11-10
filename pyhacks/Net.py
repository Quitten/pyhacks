import socket
import whois
import dns.resolver
from ping3 import ping, verbose_ping

class Net:
    def __init__(self):
        self.resolver = dns.resolver.Resolver()
        self.records = [
                'NONE',
                'A',
                'NS',
                'MD',
                'MF',
                'CNAME',
                'SOA',
                'MB',
                'MG',
                'MR',
                'NULL',
                'WKS',
                'PTR',
                'HINFO',
                'MINFO',
                'MX',
                'TXT',
                'RP',
                'AFSDB',
                'X25',
                'ISDN',
                'RT',
                'NSAP',
                'NSAP-PTR',
                'SIG',
                'KEY',
                'PX',
                'GPOS',
                'AAAA',
                'LOC',
                'NXT',
                'SRV',
                'NAPTR',
                'KX',
                'CERT',
                'A6',
                'DNAME',
                'OPT',
                'APL',
                'DS',
                'SSHFP',
                'IPSECKEY',
                'RRSIG',
                'NSEC',
                'DNSKEY',
                'DHCID',
                'NSEC3',
                'NSEC3PARAM',
                'TLSA',
                'HIP',
                'CDS',
                'CDNSKEY',
                'CSYNC',
                'SPF',
                'UNSPEC',
                'EUI48',
                'EUI64',
                'TKEY',
                'TSIG',
                'IXFR',
                'AXFR',
                'MAILB',
                'MAILA',
                'ANY',
                'URI',
                'CAA',
                'TA',
                'DLV',
        ]
    
    def reply_to_ping(self, host_or_ip):
        return ping(host_or_ip) != None
    
    def resolve(self, hostname):
        return socket.gethostbyname(hostname)

    def _query_dns(self, domain, record):
        res = []
        try:
            for rdata in self.resolver.query(domain, record):
                res.append(str(rdata))
        except:
            pass
        return res
    
    def dig(self, domain, record='all', namserver='8.8.8.8'):
        self.resolver.nameservers=[socket.gethostbyname(namserver)]
        res = {}
        if record == 'all':
            for record in self.records:
                dnsRes = self._query_dns(domain, record)
                if dnsRes != []:
                    res[record] = self._query_dns(domain, record)
        else:
            dnsRes = self._query_dns(domain, record)
            if dnsRes != []:
                res[record] = self._query_dns(domain, record)
        return res
    
    def whois(self, domain):
        # returnObject.name, returnObject.registrar
        return whois.query(domain)
    
    #TODO: Implement the following functions
    # def ssh to server run command and get result
    # def shodan / censys
    # def portScan
    # def passiveDNS
    # def reverselookup
    