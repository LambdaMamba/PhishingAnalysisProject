import os
import subprocess
fd = open("ip_whois.txt", "r")
serverlist = []
while True:
    line = fd.readline()
    if not line:
        break
    serverlist.append(line)

        
for ip in serverlist:
    response = os.system("whois " + ip)