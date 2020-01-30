import os
import re
import sys
import time
import platform
import requests

if platform.system() == 'Windows':
    os.system('cls')
elif platform.system() == 'Linux':
    os.system('clear')

hackerapi = {
    1: 'https://api.hackertarget.com/mtr/?q=',
    2: 'https://api.hackertarget.com/nping/?q=',
    3: 'https://api.hackertarget.com/dnslookup/?q=',
    4: 'https://api.hackertarget.com/hostsearch/?q=',
    5: 'https://api.hackertarget.com/reversedns/?q=',
    6: 'https://api.hackertarget.com/findshareddns/?q=',
    7: 'https://api.hackertarget.com/zonetransfer/?q=',
    8: 'https://api.hackertarget.com/whois/?q=',
    9: 'https://api.hackertarget.com/geoip/?q=',
    10: 'https://api.hackertarget.com/reverseiplookup/?q=',
    11: 'https://api.hackertarget.com/nmap/?q=',
    12: 'https://api.hackertarget.com/subnetcalc/?q=',
    13: 'https://api.hackertarget.com/httpheaders/?q=',
    14: 'https://api.hackertarget.com/pagelinks/?q=',
    15: 'https://api.hackertarget.com/aslookup/?q=',
    16: 'https://api.hackertarget.com/bannerlookup/?q=',
}

print(
    '''
    ---------------------------------
    |      Hacker Target Tools      |
    |        Created by Void        |
    ---------------------------------

[0]. Exit
[1]. Traceroute
[2]. Test Ping
[3]. DNS Lookup
[4]. Find (A) Records
[5]. Reverse DNS
[6]. Find Shared DNS Servers
[7]. Zone Transfer
[8]. Whois Lookup
[9]. GeoIP Lookup
[10]. Reverse IP
[11]. TCP Port Scan
[12]. Subnet Lookup Online
[13]. HTTP Headers
[14]. Page Links
[15]. AS Lookup
[16]. Banner Grabbing (Search)\n'''
)

try:
    choose = int(input('Choose : '))
except Exception as e:
    print(e)
    exit(0)

url = input('\nTarget : ')
if url.startswith('http'):
    if not '/' in url[-1]:
        url += '/'
    url = re.findall(r'http[s]?://(.+?)/', url, re.M)[0]

for key, value in hackerapi.items():
    if key == choose:
        try:
            r = requests.get(value + url)
        except Exception as e:
            print(e)
            exit(0)
        else:
            print(r.text)
